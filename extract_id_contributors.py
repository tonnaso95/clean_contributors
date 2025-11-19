#!/usr/bin/env python3
"""
Script to extract only 'id' and 'contributors' fields from the JSON dataset.
"""

import json

def extract_fields(input_file, output_file):
    """
    Read the input JSON file and create a new JSON file with only 'id' and 'contributors' fields.

    Args:
        input_file: Path to the input JSON file
        output_file: Path to the output JSON file
    """
    print(f"Reading {input_file}...")

    # Read the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Processing {len(data)} records...")

    # Extract only 'id' and 'contributors' fields
    cleaned_data = [
        {
            'id': item.get('id'),
            'contributors': item.get('contributors')
        }
        for item in data
    ]

    # Write the cleaned data to the output file
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"Done! Created {output_file} with {len(cleaned_data)} records.")

if __name__ == "__main__":
    input_file = "DIRTY_dataset_dottori_di_ricerca.json"
    output_file = "clean_dataset_contributors.json"

    extract_fields(input_file, output_file)
