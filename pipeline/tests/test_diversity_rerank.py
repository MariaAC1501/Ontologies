from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pipeline.diversity_rerank import (  # noqa: E402
    DEFAULT_WEIGHTS,
    build_taxonomy_index,
    load_taxonomy_tree,
    normalize_text,
    normalize_token,
    normalize_weights,
    parse_float,
    parse_weights,
    process_file,
    read_csv_rows,
    rerank_mmr,
    solution_signature,
    solution_similarity,
    split_multi,
    taxonomy_similarity,
)


MODEL_ONLY_WEIGHTS = (0.0, 0.0, 1.0, 0.0)
MMR_ROWS = [
    {"Reference": "A", "Sim": "0.90", "Models": "aaaa"},
    {"Reference": "B", "Sim": "0.89", "Models": "aaaa"},
    {"Reference": "C", "Sim": "0.80", "Models": "zzzz"},
]


class DiversityRerankTests(unittest.TestCase):
    def test_normalization_and_parsing_helpers(self) -> None:
        self.assertEqual(normalize_text("  A\ufeff  B\n"), "a b")
        self.assertEqual(normalize_token("Random-Forest++"), "random forest")
        self.assertEqual(parse_float("0,75"), 0.75)
        self.assertEqual(parse_float("bad", default=-1), -1)
        self.assertEqual(split_multi("A, B,, C"), ["A", "B", "C"])

    def test_load_taxonomy_tree_reads_ast_without_importing_module(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            submodule = Path(tmpdir)
            (submodule / "Methods2.py").write_text(
                'raise RuntimeError("must not import")\n'
                'Similarity.TaxonomyTree = [["SVM", "Random Forest"], ["ARIMA"], ["CNN"]]\n',
                encoding="utf-8",
            )

            tree = load_taxonomy_tree(submodule)

        self.assertEqual(tree, [["SVM", "Random Forest"], ["ARIMA"], ["CNN"]])
        index = build_taxonomy_index(tree)
        self.assertEqual(index["svm"], 0)
        self.assertEqual(index["random forest"], 0)
        self.assertEqual(index["arima"], 1)
        self.assertEqual(taxonomy_similarity("SVM", "Random Forest", index), 1.0)
        self.assertEqual(taxonomy_similarity("SVM", "ARIMA", index), 0.8)
        self.assertIsNone(taxonomy_similarity("SVM", "Unknown", index))

    def test_solution_signature_uses_row_values_before_casebase_fallback(self) -> None:
        casebase = {
            "A": {
                "Model Approach": "Single model",
                "Model Type": "Classifier",
                "Models": "Random Forest",
                "Data Pre-processing": "yes",
            }
        }

        fallback_signature = solution_signature({"Reference": "A"}, casebase)
        row_signature = solution_signature({"Reference": "A", "Models": "SVM"}, casebase)

        self.assertEqual(fallback_signature["models"], "Random Forest")
        self.assertEqual(fallback_signature["model_type"], "Classifier")
        self.assertEqual(row_signature["models"], "SVM")
        self.assertEqual(row_signature["model_type"], "Classifier")

    def test_normalize_weights_and_parse_weights(self) -> None:
        self.assertEqual(normalize_weights([2, 2, 4, 2]), (0.2, 0.2, 0.4, 0.2))
        self.assertEqual(parse_weights("2,2,4,2"), (0.2, 0.2, 0.4, 0.2))
        self.assertEqual(normalize_weights([0, 0, 0, 0]), DEFAULT_WEIGHTS)
        with self.assertRaises(ValueError):
            normalize_weights([1, 2, 3])

    def test_solution_similarity_model_only_exact_and_different(self) -> None:
        same = solution_similarity(
            {"Models": "aaaa"},
            {"Models": "aaaa"},
            {},
            {},
            MODEL_ONLY_WEIGHTS,
        )
        different = solution_similarity(
            {"Models": "aaaa"},
            {"Models": "zzzz"},
            {},
            {},
            MODEL_ONLY_WEIGHTS,
        )

        self.assertEqual(same, 1.0)
        self.assertEqual(different, 0.0)

    def test_rerank_mmr_keep_top1_selects_diverse_candidate(self) -> None:
        ranked = rerank_mmr(
            MMR_ROWS,
            top_k=3,
            lambda_relevance=0.5,
            casebase_by_ref={},
            taxonomy_index={},
            weights=MODEL_ONLY_WEIGHTS,
            keep_top1=True,
            pool_size=None,
        )

        self.assertEqual([row["Reference"] for row, _ in ranked], ["A", "C", "B"])
        self.assertEqual(ranked[0][1].cbr_rank, 1)
        self.assertEqual(ranked[0][1].diversity_penalty, 0.0)
        self.assertEqual(ranked[0][1].rerank_score, 0.9)
        self.assertEqual(ranked[1][1].cbr_rank, 3)
        self.assertEqual(ranked[1][1].diversity_penalty, 0.0)
        self.assertEqual(ranked[1][1].rerank_score, 0.4)
        self.assertEqual(ranked[2][1].cbr_rank, 2)
        self.assertEqual(ranked[2][1].diversity_penalty, 1.0)
        self.assertAlmostEqual(ranked[2][1].rerank_score, -0.055)

    def test_rerank_mmr_pool_size_limits_candidates(self) -> None:
        ranked = rerank_mmr(
            MMR_ROWS,
            top_k=3,
            lambda_relevance=0.5,
            casebase_by_ref={},
            taxonomy_index={},
            weights=MODEL_ONLY_WEIGHTS,
            keep_top1=True,
            pool_size=2,
        )

        self.assertEqual([row["Reference"] for row, _ in ranked], ["A", "B"])

    def test_rerank_mmr_top_k_zero_returns_empty(self) -> None:
        ranked = rerank_mmr(
            MMR_ROWS,
            top_k=0,
            lambda_relevance=0.5,
            casebase_by_ref={},
            taxonomy_index={},
            weights=MODEL_ONLY_WEIGHTS,
            keep_top1=True,
            pool_size=None,
        )

        self.assertEqual(ranked, [])

    def test_rerank_mmr_tie_breaks_by_original_rank(self) -> None:
        ranked = rerank_mmr(
            [
                {"Reference": "A", "Sim": "0.50", "Models": "aaaa"},
                {"Reference": "B", "Sim": "0.50", "Models": "zzzz"},
            ],
            top_k=1,
            lambda_relevance=0.5,
            casebase_by_ref={},
            taxonomy_index={},
            weights=MODEL_ONLY_WEIGHTS,
            keep_top1=False,
            pool_size=None,
        )

        self.assertEqual([row["Reference"] for row, _ in ranked], ["A"])

    def test_process_file_writes_augmented_csv_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            input_csv = tmp_path / "results.csv"
            output_dir = tmp_path / "out"
            input_csv.write_text(
                "Reference;Sim;Models\n"
                "A;0.90;aaaa\n"
                "B;0.89;aaaa\n"
                "C;0.80;zzzz\n",
                encoding="utf-8",
            )

            summary = process_file(
                input_csv,
                output_dir=output_dir,
                suffix=".diverse.csv",
                top_k=2,
                lambda_relevance=0.5,
                casebase_by_ref={},
                taxonomy_index={},
                weights=MODEL_ONLY_WEIGHTS,
                keep_top1=True,
                pool_size=None,
            )
            output_csv = output_dir / "results.diverse.csv"
            output_exists = output_csv.exists()
            fieldnames, rows = read_csv_rows(output_csv)

        self.assertTrue(output_exists)
        self.assertIn("cbr_rank", fieldnames)
        self.assertIn("rerank_method", fieldnames)
        self.assertEqual([row["Reference"] for row in rows], ["A", "C"])
        self.assertEqual(rows[0]["cbr_rank"], "1")
        self.assertEqual(rows[0]["cbr_score"], "0.900000")
        self.assertEqual(rows[1]["cbr_rank"], "3")
        self.assertEqual(rows[1]["rerank_score"], "0.400000")
        self.assertEqual(summary["input_rows"], 3)
        self.assertEqual(summary["output_rows"], 2)
        self.assertEqual(summary["original_top_refs"], ["A", "B"])
        self.assertEqual(summary["reranked_refs"], ["A", "C"])
        self.assertTrue(summary["changed_top_k_order"])
        self.assertEqual(summary["unique_models"], 2)


if __name__ == "__main__":
    unittest.main()
