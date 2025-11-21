#!/usr/bin/env python3
"""
Script to convert dictionary/conflicts.log to a CSV file.
Extracts roles and their conflicting variations.
"""

import csv
import re

def parse_conflicts_log(input_file, output_file):
    """
    Parse conflicts.log and convert to CSV format.

    Args:
        input_file: Path to the conflicts.log file
        output_file: Path to the output CSV file
    """
    conflicts = []
    current_role = None
    current_variations = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()

            # Match role line (starts with number followed by period)
            role_match = re.match(r'^\d+\.\s+Role:\s+[\'"](.+)[\'"]', line)
            if role_match:
                # Save previous role if exists
                if current_role:
                    conflicts.append([current_role] + current_variations)

                # Start new role
                current_role = role_match.group(1)
                current_variations = []
                continue

            # Match variation line (starts with "     - ")
            variation_match = re.match(r'^\s+-\s+(.+)', line)
            if variation_match:
                current_variations.append(variation_match.group(1))

    # Don't forget the last role
    if current_role:
        conflicts.append([current_role] + current_variations)

    # Pad variations to ensure we have 3 columns
    max_variations = max(len(row) - 1 for row in conflicts) if conflicts else 3
    for row in conflicts:
        while len(row) < max_variations + 1:
            row.append('')

    # Write to CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        # Write header
        header = ['role'] + [f'variation{i+1}' for i in range(max_variations)]
        writer.writerow(header)

        # Write data
        writer.writerows(conflicts)

    print(f"Parsed {len(conflicts)} conflicting roles")
    print(f"Maximum variations found: {max_variations}")
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    input_file = "dictionary/conflicts.log"
    output_file = "dictionary/conflicts.csv"

    parse_conflicts_log(input_file, output_file)
