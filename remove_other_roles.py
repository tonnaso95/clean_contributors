#!/usr/bin/env python3
"""
Script to remove rows with 'other' as normalized_role from mapped_roles_full.csv
"""

import csv
import sys

def remove_other_roles(input_file, output_file=None):
    """
    Remove rows where normalized_role is 'other' from the CSV file.

    Args:
        input_file: Path to the input CSV file
        output_file: Path to the output CSV file (optional, defaults to input_file)
    """
    if output_file is None:
        output_file = input_file

    rows_to_keep = []
    removed_count = 0
    total_count = 0

    # Read the CSV file
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for row in reader:
            total_count += 1
            if row['normalized_role'].strip().lower() != 'other':
                rows_to_keep.append(row)
            else:
                removed_count += 1

    # Write the filtered data back
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_to_keep)

    print(f"Processing complete!")
    print(f"Total rows (excluding header): {total_count}")
    print(f"Rows removed: {removed_count}")
    print(f"Rows kept: {len(rows_to_keep)}")
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    input_file = "dictionary/mapped_roles_full.csv"

    # Optional: provide output file as command line argument
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        output_file = input_file  # Overwrite the original file

    remove_other_roles(input_file, output_file)
