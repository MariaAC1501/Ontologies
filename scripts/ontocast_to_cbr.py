#!/usr/bin/env python3
"""
Convert OntoCast RDF/Turtle output to CBR-compatible CSV format.

Maps OntoCast-extracted instances to the OMSSA CBR case structure.

Usage:
    python ontocast_to_cbr.py --input extracted.ttl --output cbr_cases.csv --start-id 439
"""

import argparse
import re
from pathlib import Path
from typing import Optional

import rdflib
from rdflib import Namespace, URIRef, Literal
import pandas as pd

# OMSSA namespace
OMSSA = Namespace("http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#")

# Expected CBR CSV columns (19 columns, semicolon-separated)
CBR_COLUMNS = [
    'Reference',
    'Publication year',
    'Task',
    'Case study',
    'Case study type',
    'Input for the model',
    'Number of input variables',
    'Input type',
    'Data Pre-processing',
    'Model Approach',
    'Model Type',
    'Models',
    'Online/Off-line',
    'Number of failure modes',
    'Performance indicator',
    'Performance',
    'Complementary notes',
    'Study title',
    'Publication identifier'
]


class CBRConverter:
    """Convert OntoCast RDF to CBR CSV format."""
    
    def __init__(self, start_id: int = 439):
        """
        Initialize converter.
        
        Args:
            start_id: Starting reference ID for new cases (current max is 438)
        """
        self.next_id = start_id
        self.graph = rdflib.Graph()
        
    def load_ontology(self, ttl_file: Path) -> None:
        """Load OntoCast Turtle output."""
        self.graph.parse(ttl_file, format="turtle")
        print(f"Loaded {len(self.graph)} triples from {ttl_file}")
        
    def _extract_literal(self, subject: URIRef, predicate: URIRef, default: str = "") -> str:
        """Extract literal value from graph."""
        for obj in self.graph.objects(subject, predicate):
            if isinstance(obj, Literal):
                return str(obj)
        return default
    
    def _extract_object(self, subject: URIRef, predicate: URIRef) -> Optional[URIRef]:
        """Extract object URI from graph."""
        for obj in self.graph.objects(subject, predicate):
            if isinstance(obj, URIRef):
                return obj
        return None
    
    def _uri_to_label(self, uri: URIRef) -> str:
        """Convert URI to human-readable label."""
        # Extract local name from URI
        label = uri.split('#')[-1] if '#' in str(uri) else str(uri).split('/')[-1]
        # Replace underscores with spaces
        label = label.replace('_', ' ')
        # Remove ID suffixes (e.g., "Case_439" → "Case")
        label = re.sub(r'\s+\d+$', '', label)
        return label.strip()
    
    def _to_sparql_safe(self, text: str) -> str:
        """Convert to SPARQL-safe format (spaces → -, - → --, / → ---)."""
        if not text:
            return ""
        text = text.replace(" ", "-")
        text = text.replace("-", "--")
        text = text.replace("/", "---")
        return text
    
    def _format_input_type(self, values: list) -> str:
        """Format Input type: capitalize each word, comma+space separated."""
        if not values:
            return ""
        formatted = []
        for val in values:
            val = str(val).strip()
            if val:
                # Capitalize each word
                val = val.title()
                formatted.append(val)
        return ", ".join(formatted)
    
    def find_cases(self) -> list[dict]:
        """Extract case instances from RDF graph."""
        cases = []
        
        # Query for Predictive_maintenance_case instances
        query = """
        SELECT ?case
        WHERE {
            ?case rdf:type ?caseType .
            FILTER (
                CONTAINS(STR(?caseType), "Predictive_maintenance_case") ||
                CONTAINS(STR(?caseType), "Case") && EXISTS { ?case ?p ?o }
            )
        }
        """
        
        results = self.graph.query(query, initNs={"rdf": rdflib.RDF, "def": OMSSA})
        
        for row in results:
            case_uri = row.case
            case_data = self._extract_case_data(case_uri)
            # Only include cases with at least a title or year
            if case_data and (case_data.get('Study title') or case_data.get('Publication year')):
                cases.append(case_data)
                
        return cases
    
    def _extract_case_data(self, case_uri: URIRef) -> Optional[dict]:
        """Extract case data from a case URI."""
        case_data = {
            'Reference': self.next_id,
            'Publication year': '',
            'Task': '',
            'Case study': '',
            'Case study type': '',
            'Input for the model': '',
            'Number of input variables': '',
            'Input type': '',
            'Data Pre-processing': '',
            'Model Approach': '',
            'Model Type': '',
            'Models': '',
            'Online/Off-line': '',
            'Number of failure modes': '',
            'Performance indicator': '',
            'Performance': '',
            'Complementary notes': '',
            'Study title': '',
            'Publication identifier': ''
        }
        
        # Extract properties - map from OMSSA ontology to CBR columns
        # Try different property patterns based on OMSSA structure
        
        # Publication year
        for pred in [OMSSA.has_publication_year, OMSSA.publicationYear, 
                     OMSSA.year, OMSSA.hasYear]:
            val = self._extract_literal(case_uri, pred)
            if val:
                case_data['Publication year'] = val
                break
        
        # Task (Predictive_maintenance_module_function)
        for pred in [OMSSA.has_predictive_maintenance_function, 
                     OMSSA.hasTask, OMSSA.task]:
            obj = self._extract_object(case_uri, pred)
            if obj:
                case_data['Task'] = self._uri_to_label(obj)
                break
        
        # Case study (Maintainable_item)
        for pred in [OMSSA.has_part, OMSSA.hasMaintainableItem, 
                     OMSSA.caseStudy, OMSSA.hasCaseStudy]:
            obj = self._extract_object(case_uri, pred)
            if obj:
                case_data['Case study'] = self._uri_to_label(obj)
                break
        
        # Case study type
        case_study = self._extract_object(case_uri, OMSSA.has_part)
        if case_study:
            for type_pred in [rdflib.RDF.type, OMSSA.hasItemType]:
                type_obj = self._extract_object(case_study, type_pred)
                if type_obj:
                    case_data['Case study type'] = self._uri_to_label(type_obj)
                    break
        
        # Input for the model (maintainable_item_record)
        for pred in [OMSSA.has_input, OMSSA.inputForModel, 
                     OMSSA.hasMaintainableItemRecord]:
            obj = self._extract_object(case_uri, pred)
            if obj:
                case_data['Input for the model'] = self._uri_to_label(obj)
                break
        
        # Input type (Data_variable) - collect all
        input_types = []
        for pred in [OMSSA.is_carrier_of, OMSSA.hasDataVariable, OMSSA.hasInputType]:
            for obj in self.graph.objects(case_uri, pred):
                input_types.append(self._uri_to_label(obj))
        if input_types:
            case_data['Input type'] = self._format_input_type(input_types)
        
        # Model Type
        for pred in [OMSSA.has_model_type, OMSSA.modelType, OMSSA.hasModelType]:
            obj = self._extract_object(case_uri, pred)
            if obj:
                case_data['Model Type'] = self._uri_to_label(obj)
                break
        
        # Models (Predictive_maintenance_model)
        models = []
        for pred in [OMSSA.function_uses_model, OMSSA.usesModel, OMSSA.hasModel]:
            for obj in self.graph.objects(case_uri, pred):
                models.append(self._uri_to_label(obj))
        if models:
            case_data['Models'] = ', '.join(models)
        
        # Online/Offline (Module_synchronization)
        for pred in [OMSSA.has_synchronization, OMSSA.synchronization,
                     OMSSA.moduleSynchronization]:
            obj = self._extract_object(case_uri, pred)
            if obj:
                label = self._uri_to_label(obj)
                if 'online' in label.lower():
                    case_data['Online/Off-line'] = 'Online'
                elif 'offline' in label.lower() or 'off-line' in label.lower():
                    case_data['Online/Off-line'] = 'Off-line'
                else:
                    case_data['Online/Off-line'] = label
                break
        
        # Study title
        for pred in [OMSSA.has_title, OMSSA.title, OMSSA.articleTitle]:
            val = self._extract_literal(case_uri, pred)
            if val:
                case_data['Study title'] = val
                break
        
        # Publication identifier (DOI)
        for pred in [OMSSA.has_identifier, OMSSA.identifier, OMSSA.doi]:
            val = self._extract_literal(case_uri, pred)
            if val:
                case_data['Publication identifier'] = val
                break
        
        self.next_id += 1
        return case_data
    
    def convert(self, output_file: Path) -> int:
        """Convert RDF to CBR CSV and save."""
        cases = self.find_cases()
        
        if not cases:
            print("Warning: No cases found in RDF graph")
            return 0
        
        # Create DataFrame with exact column order
        df = pd.DataFrame(cases, columns=CBR_COLUMNS)
        
        # Save with semicolon separator (CRITICAL for CBR import!)
        df.to_csv(output_file, sep=';', index=False, encoding='utf-8')
        
        print(f"Converted {len(cases)} cases to {output_file}")
        return len(cases)


def main():
    parser = argparse.ArgumentParser(
        description='Convert OntoCast RDF to CBR CSV format'
    )
    parser.add_argument('--input', '-i', type=Path, required=True,
                        help='Input Turtle file from OntoCast')
    parser.add_argument('--output', '-o', type=Path, required=True,
                        help='Output CSV file for CBR import')
    parser.add_argument('--start-id', '-s', type=int, default=439,
                        help='Starting reference ID (default: 439)')
    parser.add_argument('--append', '-a', action='store_true',
                        help='Append to existing CSV instead of overwriting')
    
    args = parser.parse_args()
    
    # Validate input
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1
    
    converter = CBRConverter(start_id=args.start_id)
    converter.load_ontology(args.input)
    
    # Convert
    count = converter.convert(args.output)
    
    if count > 0:
        print(f"\nNext available ID: {converter.next_id}")
        print(f"\nTo import into CBR:")
        print(f"  1. Copy {args.output} to CBR-Ontology/CBRproject/data/")
        print(f"  2. Update AppConfiguration.java data_path")
        print(f"  3. Run CSVtoOntologyExec.java in Eclipse")
        print(f"  4. Run myCBRSetting.java")
        print(f"  5. Run GUI2.java or GUI3.java")
    
    return 0


if __name__ == "__main__":
    exit(main())
