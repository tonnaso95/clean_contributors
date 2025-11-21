#!/usr/bin/env python3
"""
Extract all unique normalized roles from roles_completed.csv
"""
import csv
from pathlib import Path

def extract_unique_roles():
    # Define paths
    input_file = Path(__file__).parent / "dictionary" / "roles.csv"
    output_file = Path(__file__).parent / "output" / "unique_normalized_roles.txt"

    # Read CSV and extract unique normalized roles
    unique_roles = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            normalized_role = row['normalized_role'].strip()
            if normalized_role:  # Only add non-empty values
                unique_roles.add(normalized_role)

    # Sort roles alphabetically for better readability
    sorted_roles = sorted(unique_roles)

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for role in sorted_roles:
            f.write(f"{role}\n")

    print(f"Extracted {len(sorted_roles)} unique normalized roles")
    print(f"Output written to: {output_file}")

    return sorted_roles

if __name__ == "__main__":
    roles = extract_unique_roles()
    print("\nUnique normalized roles:")
    for role in roles:
        print(f"  - {role}")
