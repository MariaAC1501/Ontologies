import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileReader;
import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.util.SimpleIRIMapper;

import CBR.Recommender;
import User.AppConfiguration;
import User.CSVtoOntologyExec;
import User.myCBRSetting;
import de.dfki.mycbr.core.casebase.Instance;
import de.dfki.mycbr.core.similarity.Similarity;
import de.dfki.mycbr.util.Pair;

public class HeadlessCBR {
    @FunctionalInterface
    private interface ThrowingSupplier<T> {
        T get() throws Exception;
    }

    private static final String DEFAULT_DATA_DIR = "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data";

    public static void main(String[] args) throws Exception {
        System.setProperty("java.awt.headless", "true");

        Map<String, String> options = new HashMap<>();
        List<String> positional = new ArrayList<>();
        parseArgs(args, options, positional);

        String command = positional.isEmpty() ? "help" : positional.get(0);
        String dataDir = options.getOrDefault("data-dir", DEFAULT_DATA_DIR);
        String csv = options.getOrDefault("csv", "CleanedDATA V12-05-2021.csv");
        String baseOnt = options.getOrDefault("base-ont", "OPMAD.owl");
        String ont = options.getOrDefault("ont", "OPMADdatabase.owl");
        String project = options.getOrDefault("project", "PredictMaint_myCBR.prj");

        bootstrapAppConfiguration(dataDir, csv, baseOnt, ont, project);

        switch (command) {
            case "csv-to-ontology":
                CSVtoOntologyExec.main(new String[0]);
                System.out.println("Wrote ontology: " + new File(AppConfiguration.data_path, AppConfiguration.ont_file_name));
                break;
            case "prepare-project":
                myCBRSetting.main(new String[0]);
                System.out.println("Prepared myCBR project: " + new File(AppConfiguration.data_path, AppConfiguration.projectName));
                break;
            case "rebuild":
                CSVtoOntologyExec.main(new String[0]);
                myCBRSetting.main(new String[0]);
                System.out.println("Rebuilt ontology and myCBR project in: " + AppConfiguration.data_path);
                break;
            case "query-batch":
                if (positional.size() < 3) {
                    usageAndExit("query-batch requires <input.csv> <output-prefix>");
                }
                runBatchQuery(positional.get(1), positional.get(2));
                break;
            case "query-one":
                runSingleQuery(options);
                break;
            case "help":
            default:
                usageAndExit(null);
        }
    }

    private static void runBatchQuery(String inputCsv, String outputPrefix) throws Exception {
        Recommender recommender = new Recommender();
        recommender.loadengine();

        List<List<String>> records = readSemicolonCsv(resolveInDataDir(inputCsv).toString());
        if (records.isEmpty()) {
            throw new IllegalArgumentException("Input CSV is empty: " + inputCsv);
        }

        Map<String, String> entry = new HashMap<>();
        int queryCount = 0;
        for (int row = 1; row < records.size(); row++) {
            List<String> headers = records.get(0);
            List<String> values = records.get(row);
            entry.clear();
            for (int col = 0; col < headers.size() && col < values.size(); col++) {
                entry.put(headers.get(col), values.get(col));
            }

            final int iteration = row;
            withSuppressedStdout(() -> {
                recommender.Export(recommender.solveOuery(
                        entry.getOrDefault("Task", ""),
                        entry.getOrDefault("Case study type", ""),
                        entry.getOrDefault("Case study", ""),
                        entry.getOrDefault("Online/Offline", ""),
                        entry.getOrDefault("Input for the model", ""),
                        entry.getOrDefault("Input type", ""),
                        entry.getOrDefault("Number of cases to retrieve", ""),
                        entry.getOrDefault("Amalgamation function", "euclidean"),
                        LocalDateTime.now().getYear(),
                        entry.getOrDefault("w1", "1"),
                        entry.getOrDefault("w2", "1"),
                        entry.getOrDefault("w3", "1"),
                        entry.getOrDefault("w4", "1"),
                        entry.getOrDefault("w5", "1"),
                        entry.getOrDefault("w6", "1")),
                        entry.getOrDefault("Number of cases to retrieve", ""),
                        stripCsvSuffix(outputPrefix),
                        iteration);
                return null;
            });
            queryCount++;
        }

        System.out.println("Processed " + queryCount + " queries from " + inputCsv + " into " + stripCsvSuffix(outputPrefix) + "*.csv");
    }

    private static void runSingleQuery(Map<String, String> options) throws Exception {
        Recommender recommender = new Recommender();
        recommender.loadengine();

        List<Pair<Instance, Similarity>> result = withSuppressedStdout(() -> recommender.solveOuery(
                options.getOrDefault("task", ""),
                options.getOrDefault("case-study-type", ""),
                options.getOrDefault("case-study", ""),
                options.getOrDefault("online-offline", ""),
                options.getOrDefault("input-for-model", ""),
                options.getOrDefault("input-type", ""),
                options.getOrDefault("number-of-cases", "5"),
                options.getOrDefault("amalgamation", "euclidean"),
                LocalDateTime.now().getYear(),
                options.getOrDefault("w1", "1"),
                options.getOrDefault("w2", "1"),
                options.getOrDefault("w3", "1"),
                options.getOrDefault("w4", "1"),
                options.getOrDefault("w5", "1"),
                options.getOrDefault("w6", "1")));

        if (result == null || result.isEmpty()) {
            System.out.println("No results.");
            return;
        }

        int requested = Integer.parseInt(options.getOrDefault("number-of-cases", "5"));
        int limit = Math.min(requested, result.size());
        List<String> headers = new ArrayList<>(Arrays.asList(
                "Reference",
                "Sim",
                "Task",
                "Case study type",
                "Case study",
                "Online/Off-line",
                "Input for the model",
                "Model Approach",
                "Models",
                "Input type",
                "Number of input variables",
                "Performance indicator",
                "Performance",
                "Complementary notes",
                "Publication Year",
                "Publication identifier"));

        System.out.println(String.join(";", headers));
        for (int i = 0; i < limit; i++) {
            Hashtable<String, String> attrs = Recommender.getAttributes(result.get(i), recommender.myConcept);
            List<String> row = new ArrayList<>();
            for (String header : headers) {
                row.add(csvEscape(attrs.getOrDefault(header, "")));
            }
            System.out.println(String.join(";", row));
        }
    }

    private static String csvEscape(String value) {
        return value.replace(";", ",");
    }

    private static List<List<String>> readSemicolonCsv(String path) throws Exception {
        List<List<String>> records = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            String line;
            while ((line = br.readLine()) != null) {
                records.add(Arrays.asList(line.split(";", -1)));
            }
        }
        return records;
    }

    private static Path resolveInDataDir(String filename) {
        Path candidate = Paths.get(filename);
        if (candidate.isAbsolute()) {
            return candidate;
        }
        return Paths.get(AppConfiguration.data_path).resolve(filename);
    }

    private static String stripCsvSuffix(String value) {
        return value.endsWith(".csv") ? value.substring(0, value.length() - 4) : value;
    }

    private static void bootstrapAppConfiguration(String dataDir, String csv, String baseOnt, String ont, String project) throws Exception {
        Path normalized = Paths.get(dataDir).toAbsolutePath().normalize();
        if (!Files.isDirectory(normalized)) {
            throw new IllegalArgumentException("Data directory does not exist: " + normalized);
        }

        String path = normalized.toString() + File.separator;
        AppConfiguration.data_path = path;
        AppConfiguration.csv = csv;
        AppConfiguration.base_ont_file_name = baseOnt;
        AppConfiguration.ont_file_name = ont;
        AppConfiguration.projectName = project;

        AppConfiguration.ont_file = new File(path + ont);
        AppConfiguration.base_ont_file = new File(path + baseOnt);
        AppConfiguration.documentIRI = IRI.create(AppConfiguration.ont_file);

        AppConfiguration.artifact_file = new File(path + "ArtifactOntology.ttl");
        AppConfiguration.artifact_file_iri = IRI.create(AppConfiguration.artifact_file);
        AppConfiguration.artifact_mapper = new SimpleIRIMapper(AppConfiguration.artifact_iri, AppConfiguration.artifact_file_iri);

        AppConfiguration.ICE_file = new File(path + "InformationEntityOntology.ttl");
        AppConfiguration.ICE_file_iri = IRI.create(AppConfiguration.ICE_file);
        AppConfiguration.ICE_mapper = new SimpleIRIMapper(AppConfiguration.ICE_iri, AppConfiguration.ICE_file_iri);

        AppConfiguration.ICEM_file = new File(path + "InformationEntityOntology.ttl");
        AppConfiguration.ICEM_file_iri = IRI.create(AppConfiguration.ICEM_file);
        AppConfiguration.ICEM_mapper = new SimpleIRIMapper(AppConfiguration.ICEM_iri, AppConfiguration.ICEM_file_iri);

        AppConfiguration.event_file = new File(path + "EventOntology.ttl");
        AppConfiguration.event_file_iri = IRI.create(AppConfiguration.event_file);
        AppConfiguration.event_mapper = new SimpleIRIMapper(AppConfiguration.event_iri, AppConfiguration.event_file_iri);

        AppConfiguration.geo_file = new File(path + "GeospatialOntology.ttl");
        AppConfiguration.geo_file_iri = IRI.create(AppConfiguration.geo_file);
        AppConfiguration.geo_mapper = new SimpleIRIMapper(AppConfiguration.geo_iri, AppConfiguration.geo_file_iri);

        AppConfiguration.relation_m_file = new File(path + "ExtendedRelationOntology.ttl");
        AppConfiguration.relation_m_file_iri = IRI.create(AppConfiguration.relation_m_file);
        AppConfiguration.relation_m_mapper = new SimpleIRIMapper(AppConfiguration.relation_m_iri, AppConfiguration.relation_m_file_iri);

        AppConfiguration.relation_file = new File(path + "ExtendedRelationOntology.ttl");
        AppConfiguration.relation_file_iri = IRI.create(AppConfiguration.relation_file);
        AppConfiguration.relation_mapper = new SimpleIRIMapper(AppConfiguration.relation_iri, AppConfiguration.relation_file_iri);

        AppConfiguration.ro_file = new File(path + "ro-import.ttl");
        AppConfiguration.ro_file_iri = IRI.create(AppConfiguration.ro_file);
        AppConfiguration.ro_mapper = new SimpleIRIMapper(AppConfiguration.ro_iri, AppConfiguration.ro_file_iri);

        AppConfiguration.time_file = new File(path + "TimeOntology.ttl");
        AppConfiguration.time_file_iri = IRI.create(AppConfiguration.time_file);
        AppConfiguration.time_mapper = new SimpleIRIMapper(AppConfiguration.time_iri, AppConfiguration.time_file_iri);
    }

    private static <T> T withSuppressedStdout(ThrowingSupplier<T> supplier) throws Exception {
        PrintStream originalOut = System.out;
        ByteArrayOutputStream sink = new ByteArrayOutputStream();
        try (PrintStream muted = new PrintStream(sink)) {
            System.setOut(muted);
            return supplier.get();
        } finally {
            System.setOut(originalOut);
        }
    }

    private static void parseArgs(String[] args, Map<String, String> options, List<String> positional) {
        for (int i = 0; i < args.length; i++) {
            String arg = args[i];
            if (arg.startsWith("--")) {
                String key = arg.substring(2);
                if (i + 1 >= args.length) {
                    throw new IllegalArgumentException("Missing value for option: " + arg);
                }
                options.put(key, args[++i]);
            } else {
                positional.add(arg);
            }
        }
    }

    private static void usageAndExit(String error) {
        if (error != null) {
            System.err.println("Error: " + error);
            System.err.println();
        }
        System.out.println("Usage:");
        System.out.println("  HeadlessCBR [--data-dir DIR] [--csv FILE] [--base-ont FILE] [--ont FILE] [--project FILE] csv-to-ontology");
        System.out.println("  HeadlessCBR [--data-dir DIR] [--csv FILE] [--base-ont FILE] [--ont FILE] [--project FILE] prepare-project");
        System.out.println("  HeadlessCBR [--data-dir DIR] [--csv FILE] [--base-ont FILE] [--ont FILE] [--project FILE] rebuild");
        System.out.println("  HeadlessCBR [--data-dir DIR] [--project FILE] query-batch <input.csv> <output-prefix>");
        System.out.println("  HeadlessCBR [--data-dir DIR] [--project FILE] query-one [--task VALUE] [--case-study-type VALUE] [--case-study VALUE] [--online-offline VALUE] [--input-for-model VALUE] [--input-type VALUE] [--number-of-cases N] [--amalgamation VALUE] [--w1 N] [--w2 N] [--w3 N] [--w4 N] [--w5 N] [--w6 N]");
        System.exit(error == null ? 0 : 1);
    }
}
