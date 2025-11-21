#!/usr/bin/env python3
"""
Script to convert all entries in dictionary/roles.csv to lowercase.
"""

import csv

def convert_roles_to_lowercase(input_file, output_file):
    """
    Read the CSV file and convert all entries to lowercase.

    Args:
        input_file: Path to the input CSV file
        output_file: Path to the output CSV file
    """
    rows = []

    # Read the CSV file
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Read header
        rows.append(header)  # Keep header as is (or convert if needed)

        # Convert all data rows to lowercase
        for row in reader:
            lowercase_row = [cell.lower() if cell else cell for cell in row]
            rows.append(lowercase_row)

    # Write the converted data back
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"Converted {len(rows)-1} rows to lowercase")
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    input_file = "dictionary/role_mappings.csv"
    output_file = "dictionary/role_mappings.csv"  # Overwrites the original file

    convert_roles_to_lowercase(input_file, output_file)
