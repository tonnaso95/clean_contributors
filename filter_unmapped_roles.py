#!/usr/bin/env python3
"""
Script to filter entries from CLEAN_contributors.json that contain
at least one "[RUOLO NON TROVATO]" in the contributors field.
"""

import json

def filter_unmapped_roles(input_file, output_file):
    """
    Filter entries that contain "[RUOLO NON TROVATO]" in contributors field.

    Args:
        input_file: Path to the input JSON file
        output_file: Path to the output JSON file
    """
    # Read the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Filter entries with "[RUOLO NON TROVATO]"
    filtered_data = []
    for entry in data:
        if entry and isinstance(entry, dict):
            contributors = entry.get("contributors", "")
            if contributors and "[RUOLO NON TROVATO]" in contributors:
                filtered_data.append(entry)

    # Write filtered data to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)

    print(f"Total entries in input: {len(data)}")
    print(f"Entries with [RUOLO NON TROVATO]: {len(filtered_data)}")
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    input_file = "output/CLEAN_contributors.json"
    output_file = "output/CLEAN_unmapped_roles.json"

    filter_unmapped_roles(input_file, output_file)
