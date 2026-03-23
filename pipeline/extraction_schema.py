from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, field_validator


OPMAD = "http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#"
CCO = "http://www.ontologyrepository.com/CommonCoreOntologies/"
OBO = "http://purl.obolibrary.org/obo/"


TASK_CLASS_IRIS: dict[str, str] = {
    "Fault detection": f"{OPMAD}Fault_detection",
    "Fault feature extraction": f"{OPMAD}Fault_feature_extraction",
    "Fault identification": f"{OPMAD}Fault_identification",
    "Health assessment": f"{OPMAD}Health_assessment",
    "Health modelling": f"{OPMAD}Health_modelling",
    "Multiple steps future state forecast": f"{OPMAD}Multiple_steps_future_state_forecast",
    "One step future state forecast": f"{OPMAD}One_step_future_state_forecast",
    "Remaining useful life estimation": f"{OPMAD}Remaining_useful_life_estimation",
}

MODEL_APPROACH_VALUES = ("Single model", "Multi model")
MODULE_SYNCHRONIZATION_VALUES = ("Online", "Off-line", "Both", "Unknown synchronization")


class PredictiveMaintenanceCase(BaseModel):
    """Structured extraction target for one 19-column CBR CSV row.

    The model mirrors the source CSV while documenting the intended OPMAD target
    classes and properties used by the original Java loader and by the planned
    OntoCast extraction pipeline.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    CSV_HEADERS: ClassVar[dict[str, str]] = {
        "reference": "Reference",
        "publication_year": "Publication Year",
        "task": "Task",
        "case_study": "Case study",
        "case_study_type": "Case study type",
        "input_for_model": "Input for the model",
        "number_of_input_variables": "Number of input variables",
        "input_types": "Input type",
        "data_preprocessing": "Data Pre-processing",
        "model_approach": "Model Approach",
        "model_types": "Model Type",
        "models": "Models",
        "module_synchronization": "Online/Off-line",
        "number_of_failure_modes": "Number of failure modes",
        "performance_indicator": "Performance indicator",
        "performance": "Performance",
        "complementary_notes": "Complementary notes",
        "study_title": "Study title",
        "publication_identifier": "Publication identifier",
    }

    reference: PositiveInt = Field(
        description=(
            f"CSV col 0. Case index. Maps to instances of {OPMAD}Predictive_maintenance_case "
            f"with lexical value carried via {OPMAD}has_text_value; CSVtoOntologyExec also links the case "
            f"to the module through {CCO}designates."
        ),
        json_schema_extra={
            "csv_column": 0,
            "csv_header": "Reference",
            "opmad_class_iri": f"{OPMAD}Predictive_maintenance_case",
            "data_property_iri": f"{OPMAD}has_text_value",
            "related_object_property_iri": f"{CCO}designates",
        },
    )
    publication_year: int = Field(
        ge=1900,
        le=2100,
        description=(
            f"CSV col 1. Maps to {OPMAD}Publication_year, linked from the article with "
            f"{OPMAD}has_publication_year and carrying the integer through {OPMAD}has_interger_value."
        ),
        json_schema_extra={
            "csv_column": 1,
            "csv_header": "Publication Year",
            "opmad_class_iri": f"{OPMAD}Publication_year",
            "object_property_iri": f"{OPMAD}has_publication_year",
            "data_property_iri": f"{OPMAD}has_interger_value",
        },
    )
    task: str = Field(
        description=(
            f"CSV col 2. Must be one of the concrete subclasses of {OPMAD}Predictive_maintenance_module_function; "
            f"the module is linked to the task via {OPMAD}has_predictive_maintenance_function."
        ),
        json_schema_extra={
            "csv_column": 2,
            "csv_header": "Task",
            "opmad_parent_class_iri": f"{OPMAD}Predictive_maintenance_module_function",
            "object_property_iri": f"{OPMAD}has_predictive_maintenance_function",
            "allowed_task_class_iris": TASK_CLASS_IRIS,
        },
    )
    case_study: str = Field(
        min_length=1,
        description=(
            f"CSV col 3. Value becomes a row-specific subclass of {OPMAD}Maintainable_item. In the Java loader the "
            f"module bears the maintainable item through {OBO}BFO_0000051."
        ),
        json_schema_extra={
            "csv_column": 3,
            "csv_header": "Case study",
            "opmad_parent_class_iri": f"{OPMAD}Maintainable_item",
            "object_property_iri": f"{OBO}BFO_0000051",
        },
    )
    case_study_type: str = Field(
        min_length=1,
        description=(
            f"CSV col 4. Maps to {OPMAD}item_type, which describes the maintainable item via {CCO}describes."
        ),
        json_schema_extra={
            "csv_column": 4,
            "csv_header": "Case study type",
            "opmad_class_iri": f"{OPMAD}item_type",
            "object_property_iri": f"{CCO}describes",
        },
    )
    input_for_model: str = Field(
        min_length=1,
        description=(
            f"CSV col 5. Value becomes a row-specific subclass of {OPMAD}maintainable_item_record; the module is "
            f"linked to the record via {OBO}BFO_0000051."
        ),
        json_schema_extra={
            "csv_column": 5,
            "csv_header": "Input for the model",
            "opmad_parent_class_iri": f"{OPMAD}maintainable_item_record",
            "object_property_iri": f"{OBO}BFO_0000051",
        },
    )
    number_of_input_variables: int = Field(
        ge=0,
        description=(
            f"CSV col 6. Intended to map to the quality class {OPMAD}number_if_input_variables with numeric value "
            f"stored via {OPMAD}has_interger_value. This field is not materialized by CSVtoOntologyExec, but the "
            f"class and datatype property exist in OPMAD.owl."
        ),
        json_schema_extra={
            "csv_column": 6,
            "csv_header": "Number of input variables",
            "opmad_class_iri": f"{OPMAD}number_if_input_variables",
            "data_property_iri": f"{OPMAD}has_interger_value",
            "implementation_status": "planned-not-in-csvtoontologyexec",
        },
    )
    input_types: list[str] = Field(
        min_length=1,
        description=(
            f"CSV col 7. Comma-separated list of {OPMAD}Data_variable instances. CSVtoOntologyExec links each "
            f"maintainable item record to its variables through {OBO}RO_0010002."
        ),
        json_schema_extra={
            "csv_column": 7,
            "csv_header": "Input type",
            "opmad_class_iri": f"{OPMAD}Data_variable",
            "object_property_iri": f"{OBO}RO_0010002",
            "multi_value": True,
        },
    )
    data_preprocessing: bool = Field(
        description=(
            f"CSV col 8. Proposed extraction mapping: represent preprocessing as a {OPMAD}Design_detail attached to the "
            f"module through {OPMAD}has_design_detail. This is an extraction-time normalization; CSVtoOntologyExec does "
            f"not currently materialize the column."
        ),
        json_schema_extra={
            "csv_column": 8,
            "csv_header": "Data Pre-processing",
            "opmad_class_iri": f"{OPMAD}Design_detail",
            "object_property_iri": f"{OPMAD}has_design_detail",
            "implementation_status": "planned-not-in-csvtoontologyexec",
        },
    )
    model_approach: Literal["Single model", "Multi model"] = Field(
        description=(
            f"CSV col 9. Proposed extraction mapping: {OPMAD}Model_configuration, linked to the predictive maintenance "
            f"model via {OPMAD}describes_configuration and lexicalized with {OPMAD}has_text_value."
        ),
        json_schema_extra={
            "csv_column": 9,
            "csv_header": "Model Approach",
            "opmad_class_iri": f"{OPMAD}Model_configuration",
            "object_property_iri": f"{OPMAD}describes_configuration",
            "data_property_iri": f"{OPMAD}has_text_value",
            "allowed_values": list(MODEL_APPROACH_VALUES),
            "implementation_status": "planned-not-in-csvtoontologyexec",
        },
    )
    model_types: list[str] = Field(
        min_length=1,
        description=(
            f"CSV col 10. Comma-separated list of {OPMAD}Model_type instances, each linked to the corresponding model "
            f"through {CCO}describes."
        ),
        json_schema_extra={
            "csv_column": 10,
            "csv_header": "Model Type",
            "opmad_class_iri": f"{OPMAD}Model_type",
            "object_property_iri": f"{CCO}describes",
            "multi_value": True,
        },
    )
    models: list[str] = Field(
        min_length=1,
        description=(
            f"CSV col 11. Comma-separated list of row-specific subclasses of {OPMAD}Predictive_maintenance_model. "
            f"CSVtoOntologyExec links them from the module and article with {OBO}RO_0010002."
        ),
        json_schema_extra={
            "csv_column": 11,
            "csv_header": "Models",
            "opmad_parent_class_iri": f"{OPMAD}Predictive_maintenance_model",
            "object_property_iri": f"{OBO}RO_0010002",
            "multi_value": True,
        },
    )
    module_synchronization: Literal["Online", "Off-line", "Both", "Unknown synchronization"] = Field(
        description=(
            f"CSV col 12. Maps to {OPMAD}Module_synchronization and is attached to the module through "
            f"{OPMAD}has_synchronization."
        ),
        json_schema_extra={
            "csv_column": 12,
            "csv_header": "Online/Off-line",
            "opmad_class_iri": f"{OPMAD}Module_synchronization",
            "object_property_iri": f"{OPMAD}has_synchronization",
            "allowed_values": list(MODULE_SYNCHRONIZATION_VALUES),
        },
    )
    number_of_failure_modes: int = Field(
        ge=0,
        description=(
            f"CSV col 13. Intended to map to {OPMAD}Number_of_failure_modes with integer lexical value via "
            f"{OPMAD}has_interger_value. CSVtoOntologyExec does not currently materialize the column."
        ),
        json_schema_extra={
            "csv_column": 13,
            "csv_header": "Number of failure modes",
            "opmad_class_iri": f"{OPMAD}Number_of_failure_modes",
            "data_property_iri": f"{OPMAD}has_interger_value",
            "implementation_status": "planned-not-in-csvtoontologyexec",
        },
    )
    performance_indicator: str = Field(
        min_length=1,
        description=(
            f"CSV col 14. Maps to {OPMAD}Performance_indicator, which describes the module via {CCO}describes."
        ),
        json_schema_extra={
            "csv_column": 14,
            "csv_header": "Performance indicator",
            "opmad_class_iri": f"{OPMAD}Performance_indicator",
            "object_property_iri": f"{CCO}describes",
            "implementation_status": "planned-not-in-csvtoontologyexec",
        },
    )
    performance: str = Field(
        min_length=1,
        description=(
            f"CSV col 15. Maps to {OPMAD}Performance_value, which is about the performance indicator via "
            f"{CCO}is_about."
        ),
        json_schema_extra={
            "csv_column": 15,
            "csv_header": "Performance",
            "opmad_class_iri": f"{OPMAD}Performance_value",
            "object_property_iri": f"{CCO}is_about",
            "implementation_status": "planned-not-in-csvtoontologyexec",
        },
    )
    complementary_notes: str = Field(
        min_length=1,
        description=(
            f"CSV col 16. Proposed extraction mapping: additional free-text {OPMAD}Design_detail linked to the module via "
            f"{OPMAD}has_design_detail. CSVtoOntologyExec does not currently materialize the column."
        ),
        json_schema_extra={
            "csv_column": 16,
            "csv_header": "Complementary notes",
            "opmad_class_iri": f"{OPMAD}Design_detail",
            "object_property_iri": f"{OPMAD}has_design_detail",
            "implementation_status": "planned-not-in-csvtoontologyexec",
        },
    )
    study_title: str = Field(
        min_length=1,
        description=(
            f"CSV col 17. Maps to {OPMAD}Article_title, linked from the article with {OPMAD}has_title and lexicalized "
            f"with {OPMAD}has_text_value."
        ),
        json_schema_extra={
            "csv_column": 17,
            "csv_header": "Study title",
            "opmad_class_iri": f"{OPMAD}Article_title",
            "object_property_iri": f"{OPMAD}has_title",
            "data_property_iri": f"{OPMAD}has_text_value",
        },
    )
    publication_identifier: str = Field(
        min_length=1,
        description=(
            f"CSV col 18. Maps to {OPMAD}Article_identifier, linked from the article with {OPMAD}has_identifier and "
            f"lexicalized with {OPMAD}has_text_value."
        ),
        json_schema_extra={
            "csv_column": 18,
            "csv_header": "Publication identifier",
            "opmad_class_iri": f"{OPMAD}Article_identifier",
            "object_property_iri": f"{OPMAD}has_identifier",
            "data_property_iri": f"{OPMAD}has_text_value",
        },
    )

    @field_validator("task")
    @classmethod
    def validate_task(cls, value: str) -> str:
        if value not in TASK_CLASS_IRIS:
            raise ValueError(f"Unsupported task {value!r}. Expected one of: {', '.join(TASK_CLASS_IRIS)}")
        return value

    @field_validator("input_types", "model_types", "models")
    @classmethod
    def validate_non_empty_lists(cls, value: list[str]) -> list[str]:
        cleaned = [item.strip() for item in value if item and item.strip()]
        if not cleaned:
            raise ValueError("List must contain at least one non-empty value")
        return cleaned

    @field_validator("performance_indicator", "performance", "complementary_notes", "study_title", "publication_identifier")
    @classmethod
    def validate_non_empty_strings(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Value must not be empty")
        return value.strip()

    @staticmethod
    def _split_multi_value(raw_value: str) -> list[str]:
        return [part.strip() for part in raw_value.split(",") if part.strip()]

    @staticmethod
    def _parse_bool(raw_value: str) -> bool:
        normalized = raw_value.strip().lower()
        if normalized in {"yes", "y", "true", "1"}:
            return True
        if normalized in {"no", "n", "false", "0"}:
            return False
        raise ValueError(f"Unsupported boolean value: {raw_value!r}")

    @classmethod
    def from_csv_row(cls, row: dict) -> "PredictiveMaintenanceCase":
        """Parse a row produced by csv.DictReader(..., delimiter=';')."""

        return cls(
            reference=int(row[cls.CSV_HEADERS["reference"]]),
            publication_year=int(row[cls.CSV_HEADERS["publication_year"]]),
            task=row[cls.CSV_HEADERS["task"]],
            case_study=row[cls.CSV_HEADERS["case_study"]],
            case_study_type=row[cls.CSV_HEADERS["case_study_type"]],
            input_for_model=row[cls.CSV_HEADERS["input_for_model"]],
            number_of_input_variables=int(row[cls.CSV_HEADERS["number_of_input_variables"]]),
            input_types=cls._split_multi_value(row[cls.CSV_HEADERS["input_types"]]),
            data_preprocessing=cls._parse_bool(row[cls.CSV_HEADERS["data_preprocessing"]]),
            model_approach=row[cls.CSV_HEADERS["model_approach"]],
            model_types=cls._split_multi_value(row[cls.CSV_HEADERS["model_types"]]),
            models=cls._split_multi_value(row[cls.CSV_HEADERS["models"]]),
            module_synchronization=row[cls.CSV_HEADERS["module_synchronization"]],
            number_of_failure_modes=int(row[cls.CSV_HEADERS["number_of_failure_modes"]]),
            performance_indicator=row[cls.CSV_HEADERS["performance_indicator"]],
            performance=row[cls.CSV_HEADERS["performance"]],
            complementary_notes=row[cls.CSV_HEADERS["complementary_notes"]],
            study_title=row[cls.CSV_HEADERS["study_title"]],
            publication_identifier=row[cls.CSV_HEADERS["publication_identifier"]],
        )


__all__ = ["PredictiveMaintenanceCase", "TASK_CLASS_IRIS", "OPMAD", "CCO", "OBO"]
