You are an expert researcher. Write or update the protocol for a systematic literature review.

Research topic requested by the user: $@

## Goal

Produce a robust systematic literature review protocol for the research topic requested by the user.

## Review directory
Choose or reuse `{{topic-slug}}/`.
Treat this directory as the source of truth for the review state.

Key artifacts:
- `protocol.md`

## Workflow
Create or update `protocol.md` with:
- PICOC-style concept breakdown
- 1-5 focused research questions
- databases to search: Scopus, Semantic Scholar, arXiv, and Google Scholar are available, but not all have to be used
- inclusion/exclusion criteria
- quality checklist
- extraction fields for later synthesis

If you do not have enough information to define the review unambiguously, **stop** and ask the user the open questions. It is better to pause than to run searches against a vague topic.

If the user provides research questions directly, first perform the PICOC breakdown, and then discuss any potential question refinements with the user. Once you and the user agree on the PICOC breakdown and questions list, proceed. Not all PICOC fields have to be used, some can be left blank. PICOC fields can contain more than one item, for example to study the same intervention on two different populations, or to include synonyms.

Furthermore, make sure to agree with the user on the database selection and inclusion/exclusion criteria before moving on.

Use this minimal template for `protocol.md`:

```markdown
# Review Protocol

## PICOC
| Population | Intervention | Comparison | Outcome | Context | Related Research Question(s) |
|--|--|--|--|--|--|

## Research questions
1.
2.

## Databases to search
- Scopus
- Semantic Scholar
- arXiv
- Google Scholar

## Inclusion/Exclusion criteria
| Criterion | Applicable to Question(s) |
|--|--|

## Quality checklist
Both questions use the scale:
- No = 0
- Insufficiently = 0.5
- Yes = 1

- Was the research published in a credible venue?
- Do the researchers discuss any problems (limitations, threats) with the validity of their results?

## Extraction fields
- Bibliographic metadata
- Research question(s) addressed (list) and level of relevance (none, partial, high)
- Key findings
- Limitations / gaps
- other fields that can help answer the research questions...
```

## Stopping rule
Stop when you and the user agree on the research questions, when the inclusion/exclusion criteria are sufficient, when the quality checklist is complete, and when the extraction fields are defined in a way that will generate enough information to answer all research questions, with consistent extraction across papers.

Iterate and reflect on your work: are you confident that you are delivering a high-quality result?
