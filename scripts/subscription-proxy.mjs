#!/usr/bin/env node
/*
# OntoCast subscription proxy

A small, localhost-only Chat Completions proxy. It calls Pi's model runtime
without an agent, coding prompts, tools, or conversation storage. Pi handles
subscription credentials and OAuth refresh. Embeddings stay local in OntoCast.

## Run

Requirements: Node.js 22.19+, Pi 1.5+ installed globally through npm, and
OntoCast installed with its `server`, `openai`, and `doc-processing` extras.
No extra Node packages are needed.

Sign in with `/login openai-codex` inside Pi if you have not already done so.
Then run these commands from the repository root in separate terminals:

```sh
# Terminal 1: start the proxy.
node --env-file=scripts/ontocast-subscription.env scripts/subscription-proxy.mjs
```

```sh
# Terminal 2: run OntoCast through the proxy.
ontocast --env-file scripts/ontocast-subscription.env process \
  --input-path ./papers --output-dir ./out

# Or start its HTTP service instead.
ontocast --env-file scripts/ontocast-subscription.env serve
```

`local-placeholder` is a dummy local key, not an OpenAI API key. The proxy
requires that value in the Bearer header. Real credentials stay in Pi's usual
agent directory (`~/.pi/agent`, or `PI_CODING_AGENT_DIR`). It uses only the
`openai-codex` subscription provider and never falls back to paid API auth.

## Settings and limits

- Change `LLM_MODEL_NAME` in `ontocast-subscription.env` to another model listed
  under `openai-codex` by `pi --list-models`. Restart both processes afterward.
- The proxy serves one model on `127.0.0.1:8787`. To change the port, set
  `PROXY_PORT` and update the port in `LLM_BASE_URL` to match.
- It supports non-streaming text messages, `reasoning_effort`, and
  `prompt_cache_key`, and returns token usage including cached and reasoning
  tokens. Temperature is ignored because subscription reasoning models may
  reject it. Other sampling controls and explicit output-token limits are not
  supported. Leave `LLM_JSON_MODE` off (the default); OntoCast still asks for
  JSON and parses it normally.
- Streaming, images, tool calls, and constrained JSON output are not supported.
  Requests are limited to 8 MiB. `LLM_REQUEST_TIMEOUT_SECONDS` sets the model-call
  timeout for both OntoCast and this proxy (default 180 seconds; the project env
  file sets 600). Restart both processes after changing it. Disconnecting the
  client cancels its upstream call.
- Requests consume your ChatGPT subscription quota. Keep the proxy on
  localhost. The dummy key is not a security boundary against other local
  processes. Prompts and credentials are not logged by the script.

Stop the proxy with Ctrl+C. No embedding settings are changed by the env file.
*/
import { execFileSync } from "node:child_process";
import { randomUUID } from "node:crypto";
import { createServer } from "node:http";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

const PROVIDER = "openai-codex";
const LOCAL_KEY = "local-placeholder";
const MAX_BODY_BYTES = 8 * 1024 * 1024;
const REASONING_EFFORTS = ["none", "minimal", "low", "medium", "high", "xhigh", "max"];

function fail(status, message) {
  throw Object.assign(new Error(message), { status });
}

function json(response, status, body, headers = {}) {
  if (response.destroyed) return;
  response.writeHead(status, {
    "Content-Type": "application/json",
    "Cache-Control": "no-store",
    ...headers,
  });
  response.end(JSON.stringify(body));
}

async function readBody(request) {
  let size = 0;
  const chunks = [];
  for await (const chunk of request) {
    size += chunk.length;
    if (size > MAX_BODY_BYTES) fail(413, "Request body exceeds 8 MiB.");
    chunks.push(chunk);
  }
  try {
    const body = JSON.parse(Buffer.concat(chunks).toString("utf8"));
    if (!body || typeof body !== "object" || Array.isArray(body)) {
      fail(400, "Expected a JSON object.");
    }
    return body;
  } catch (error) {
    if (error.status) throw error;
    fail(400, "Invalid JSON request body.");
  }
}

function messageText(content) {
  if (typeof content === "string") return content;
  if (Array.isArray(content) && content.every(part => part?.type === "text" && typeof part.text === "string")) {
    return content.map(part => part.text).join("");
  }
  fail(400, "Only text messages are supported.");
}

function context(messages, model) {
  if (!Array.isArray(messages) || messages.length === 0) fail(400, "messages must be a non-empty array.");
  return {
    messages: messages.map(message => {
      if (!message || !["system", "developer", "user", "assistant"].includes(message.role)
          || message.tool_calls || message.function_call) {
        fail(400, "Only system, developer, user, and assistant text messages are supported.");
      }
      const role = message.role === "developer" ? "system" : message.role;
      const content = messageText(message.content);
      const timestamp = Date.now();
      if (role !== "assistant") return { role, content, timestamp };
      return {
        role, content: [{ type: "text", text: content }], timestamp,
        api: model.api, provider: model.provider, model: model.id, stopReason: "stop",
        usage: {
          input: 0, output: 0, cacheRead: 0, cacheWrite: 0, totalTokens: 0,
          cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, total: 0 },
        },
      };
    }),
  };
}

async function main() {
  // Node does not search global npm packages. Load the SDK shipped with Pi.
  const npmRoot = execFileSync("npm", ["root", "-g"], { encoding: "utf8" }).trim();
  const sdk = join(npmRoot, "@earendil-works/pi-coding-agent/dist/index.js");
  const { ModelRuntime } = await import(pathToFileURL(sdk).href);
  const runtime = await ModelRuntime.create();
  const modelId = process.env.LLM_MODEL_NAME || "gpt-6.1-sol";
  const port = Number(process.env.PROXY_PORT || 8787);
  if (!Number.isInteger(port) || port < 1 || port > 65535) fail(400, "Invalid PROXY_PORT.");
  const timeoutSeconds = Number(process.env.LLM_REQUEST_TIMEOUT_SECONDS ?? 180);
  const timeoutMs = timeoutSeconds * 1000;
  if (!Number.isFinite(timeoutMs) || timeoutMs <= 0 || timeoutMs > 2_147_483_647) {
    fail(400, "LLM_REQUEST_TIMEOUT_SECONDS must be positive and within Node's timer limit.");
  }
  if (!runtime.isUsingSubscription(PROVIDER)) {
    fail(401, "Sign in to your ChatGPT subscription with /login openai-codex inside Pi first.");
  }
  const model = runtime.getModel(PROVIDER, modelId);
  if (!model) fail(400, `Pi does not know ${PROVIDER}/${modelId}. Choose a model from pi --list-models.`);

  const server = createServer(async (request, response) => {
    const controller = new AbortController();
    response.on("close", () => controller.abort());
    let timer;
    let upstreamStatus = 502;
    let retryAfter;
    try {
      // No browser access: this endpoint spends the local user's subscription quota.
      if (request.headers.origin) fail(403, "Browser requests are not supported.");
      if (request.headers.authorization !== `Bearer ${LOCAL_KEY}`) fail(401, `Use Bearer ${LOCAL_KEY}.`);
      if (request.method === "GET" && request.url === "/v1/models") {
        return json(response, 200, {
          object: "list",
          data: [{ id: modelId, object: "model", created: 0, owned_by: PROVIDER }],
        });
      }
      if (request.method !== "POST" || request.url !== "/v1/chat/completions") fail(404, "Unknown endpoint.");
      const body = await readBody(request);
      if (body.model !== undefined && body.model !== modelId) fail(404, `This proxy serves only ${modelId}.`);
      if (body.stream) fail(400, "Streaming is not supported.");
      if (body.n !== undefined && body.n !== 1) fail(400, "Only n=1 is supported.");
      if (body.response_format && body.response_format.type !== "text") {
        fail(400, "Constrained JSON output is not supported. Keep LLM_JSON_MODE=false.");
      }
      for (const field of ["tools", "functions", "stop", "max_tokens", "max_completion_tokens", "top_p", "logprobs"]) {
        if (body[field] != null) fail(400, `${field} is not supported by this proxy.`);
      }
      if (body.reasoning_effort != null && !REASONING_EFFORTS.includes(body.reasoning_effort)) {
        fail(400, "Invalid reasoning_effort.");
      }
      if (body.prompt_cache_key != null && typeof body.prompt_cache_key !== "string") {
        fail(400, "prompt_cache_key must be a string.");
      }
      const input = context(body.messages, model);
      timer = setTimeout(() => controller.abort(), timeoutMs);
      const result = await runtime.complete(model, input, {
        signal: controller.signal,
        transport: "sse",
        toolChoice: "none",
        reasoningEffort: body.reasoning_effort ?? undefined,
        sessionId: body.prompt_cache_key ?? undefined,
        // Do not forward temperature: subscription reasoning models may reject it.
        onResponse: ({ status, headers }) => {
          upstreamStatus = status;
          retryAfter = headers["retry-after"];
        },
      });
      if (controller.signal.aborted) fail(504, "Subscription request timed out or was cancelled.");
      if (result.stopReason === "error" || result.stopReason === "aborted") {
        fail(upstreamStatus >= 400 ? upstreamStatus : 502, result.errorMessage || "Subscription request failed.");
      }
      if (!["stop", "length"].includes(result.stopReason)) fail(502, `Unexpected stop reason: ${result.stopReason}.`);
      const content = result.content.filter(part => part.type === "text").map(part => part.text).join("");
      const usage = result.usage;
      // Pi separates cached input from fresh input; OpenAI includes it in prompt_tokens.
      const promptTokens = usage.input + usage.cacheRead + usage.cacheWrite;
      json(response, 200, {
        id: `chatcmpl-${randomUUID()}`,
        object: "chat.completion",
        created: Math.floor(Date.now() / 1000),
        model: modelId,
        choices: [{
          index: 0,
          message: { role: "assistant", content },
          finish_reason: result.stopReason,
        }],
        usage: {
          prompt_tokens: promptTokens,
          completion_tokens: usage.output,
          total_tokens: promptTokens + usage.output,
          prompt_tokens_details: { cached_tokens: usage.cacheRead },
          completion_tokens_details: { reasoning_tokens: usage.reasoning ?? 0 },
        },
      });
    } catch (error) {
      const status = error.status || 502;
      json(response, status, {
        error: { message: error.message, type: status >= 500 ? "server_error" : "invalid_request_error", code: null },
      }, retryAfter ? { "Retry-After": retryAfter } : {});
    } finally {
      clearTimeout(timer);
    }
  });
  server.on("error", error => {
    console.error(error.message);
    process.exitCode = 1;
  });
  server.listen(port, "127.0.0.1", () => {
    console.log(`Subscription proxy: http://127.0.0.1:${port}/v1 (${PROVIDER}/${modelId}; timeout ${timeoutSeconds}s)`);
  });
}

main().catch(error => {
  console.error(error.message);
  process.exitCode = 1;
});
