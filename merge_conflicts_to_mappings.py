import csv
import os

def merge_conflicts_to_mappings():
    """
    Merges conflicts.csv into role_mappings.csv.
    For each role in conflicts.csv, adds an entry to role_mappings.csv
    using variation1 as the normalized_role.
    """

    conflicts_file = 'dictionary/conflicts.csv'
    mappings_file = 'dictionary/roles_merged_full.csv'

    # Read existing mappings to avoid duplicates
    existing_mappings = {}
    try:
        with open(mappings_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                role = row['role'].strip().lower()
                existing_mappings[role] = row['normalized_role'].strip()
    except FileNotFoundError:
        print(f"Warning: {mappings_file} not found. Will create new file.")
        existing_mappings = {}

    # Read conflicts and prepare new mappings
    new_mappings = []
    conflicts_count = 0

    with open(conflicts_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            role = row['role'].strip()
            variation1 = row['variation1'].strip()

            # Skip empty rows
            if not role or not variation1:
                continue

            # Check if role already exists in mappings
            if role.lower() not in existing_mappings:
                new_mappings.append({
                    'role': role,
                    'normalized_role': variation1
                })
                conflicts_count += 1
            else:
                print(f"Skipping '{role}' - already exists in mappings with normalized_role '{existing_mappings[role.lower()]}'")

    # Append new mappings to role_mappings.csv
    if new_mappings:
        with open(mappings_file, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['role', 'normalized_role'])
            for mapping in new_mappings:
                writer.writerow(mapping)

        print(f"\nSuccessfully added {len(new_mappings)} new mappings from conflicts.csv to role_mappings.csv")
    else:
        print("\nNo new mappings to add. All conflict roles already exist in role_mappings.csv")

    return len(new_mappings)

if __name__ == '__main__':
    merge_conflicts_to_mappings()
