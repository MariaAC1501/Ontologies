#!/usr/bin/env python3
"""
Convert OntoCast JSON output to CBR-compatible CSV.

This version extracts directly from the JSON response instead of parsing RDF.
"""

import argparse
import json
import re
from pathlib import Path
import pandas as pd

CBR_COLUMNS = [
    'Reference', 'Publication year', 'Task', 'Case study', 'Case study type',
    'Input for the model', 'Number of input variables', 'Input type',
    'Data Pre-processing', 'Model Approach', 'Model Type', 'Models',
    'Online/Off-line', 'Number of failure modes', 'Performance indicator',
    'Performance', 'Complementary notes', 'Study title', 'Publication identifier'
]


def extract_from_facts(facts_text: str) -> dict:
    """Extract case information from facts text using regex patterns."""
    case_data = {col: '' for col in CBR_COLUMNS}
    
    # Extract publication year
    year_match = re.search(r'(\d{4})', facts_text)
    if year_match:
        case_data['Publication year'] = year_match.group(1)
    
    # Extract DOI
    doi_match = re.search(r'(doi\.org/[^\s\"]+)', facts_text)
    if doi_match:
        case_data['Publication identifier'] = doi_match.group(1)
    
    # Extract title
    title_match = re.search(r'[Tt]itle[:\s]+([^\n]+)', facts_text)
    if title_match:
        case_data['Study title'] = title_match.group(1).strip()
    
    # Look for equipment/machinery mentions
    equipment_patterns = [
        r'([A-Z][a-zA-Z\s]+[Mm]achine)',
        r'([A-Z][a-zA-Z\s]+[Ee]quipment)',
        r'([A-Z][a-zA-Z\s]+[Bb]earing)',
        r'(Slitting Machine)',
        r'(Jet engine)',
        r'(Battery)',
    ]
    for pattern in equipment_patterns:
        match = re.search(pattern, facts_text)
        if match:
            case_data['Case study'] = match.group(1).strip()
            break
    
    # Look for task/function mentions
    task_patterns = [
        r'([Hh]ealth [Mm]odelling?)',
        r'([Rr]emaining [Uu]seful [Ll]ife)',
        r'([Ff]ault [Dd]etection)',
        r'([Ff]orecast)',
    ]
    for pattern in task_patterns:
        match = re.search(pattern, facts_text)
        if match:
            case_data['Task'] = match.group(1).strip().title()
            break
    
    # Look for model/algorithm mentions
    model_patterns = [
        r'(ARIMA)',
        r'(LSTM)',
        r'(Random Forest)',
        r'(Neural Network)',
        r'(Logistic Regression)',
    ]
    models_found = []
    for pattern in model_patterns:
        if re.search(pattern, facts_text):
            models_found.append(pattern.replace('(', '').replace(')', ''))
    if models_found:
        case_data['Models'] = ', '.join(models_found)
        case_data['Model Type'] = 'Data-driven'
    
    # Look for input/sensor mentions
    sensor_patterns = [
        r'[Tt]emperature',
        r'[Vv]ibration',
        r'[Pp]ressure',
        r'[Cc]urrent',
        r'[Vv]oltage',
    ]
    sensors_found = []
    for pattern in sensor_patterns:
        if re.search(pattern, facts_text):
            sensors_found.append(pattern.title())
    if sensors_found:
        case_data['Input type'] = ', '.join(sensors_found)
        case_data['Input for the model'] = 'Time series'
    
    # Look for online/offline
    if re.search(r'[Oo]ff[-\s]?line', facts_text):
        case_data['Online/Off-line'] = 'Off-line'
    elif re.search(r'[Oo]nline', facts_text):
        case_data['Online/Off-line'] = 'Online'
    
    return case_data


def main():
    parser = argparse.ArgumentParser(description='Convert OntoCast JSON to CBR CSV')
    parser.add_argument('--input', '-i', type=Path, required=True, help='Input JSON file')
    parser.add_argument('--output', '-o', type=Path, required=True, help='Output CSV file')
    parser.add_argument('--start-id', '-s', type=int, default=439, help='Starting reference ID')
    args = parser.parse_args()
    
    # Load JSON
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if data.get('status') != 'success':
        print(f"Error: {data.get('error', 'Unknown error')}")
        return 1
    
    # Extract from facts
    facts = data.get('data', {}).get('facts', '')
    case_data = extract_from_facts(facts)
    case_data['Reference'] = args.start_id
    
    # Create CSV
    df = pd.DataFrame([case_data], columns=CBR_COLUMNS)
    df.to_csv(args.output, sep=';', index=False, encoding='utf-8')
    
    print(f"Extracted 1 case to {args.output}")
    print(f"\nExtracted data:")
    for col in ['Publication year', 'Task', 'Case study', 'Models', 'Online/Off-line']:
        if case_data[col]:
            print(f"  {col}: {case_data[col]}")
    
    return 0


if __name__ == '__main__':
    exit(main())
