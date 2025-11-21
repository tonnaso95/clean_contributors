import csv
from collections import defaultdict

def merge_role_dictionaries(file1, file2, output_file, log_file):
    """
    Merge two role dictionary CSV files into one, removing duplicates.
    Log conflicts when the same role has different normalized values.

    Args:
        file1: Path to first CSV file
        file2: Path to second CSV file
        output_file: Path to output merged CSV file
        log_file: Path to log file for conflicts
    """
    # Dictionary to store role mappings: role -> list of normalized_role values
    role_mappings = defaultdict(list)

    # Read both CSV files
    for csv_file in [file1, file2]:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                role = row['role'].strip()
                normalized_role = row['normalized_role'].strip()
                role_mappings[role].append(normalized_role)

    # Identify conflicts and prepare final mappings
    final_mappings = {}
    conflicts = []

    for role, normalized_values in role_mappings.items():
        # Get unique normalized values for this role
        unique_values = list(set(normalized_values))

        if len(unique_values) > 1:
            # Conflict: same role has different normalized values
            conflicts.append({
                'role': role,
                'variations': unique_values,
                'occurrences': len(normalized_values)
            })
            # For now, use the first unique value (user will decide later)
            final_mappings[role] = unique_values[0]
        else:
            # No conflict, use the single normalized value
            final_mappings[role] = unique_values[0]

    # Write conflicts to log file
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("ROLE NORMALIZATION CONFLICTS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Found {len(conflicts)} roles with conflicting normalized values.\n")
        f.write("Please review and decide which variation to keep.\n\n")

        for i, conflict in enumerate(conflicts, 1):
            f.write(f"{i}. Role: '{conflict['role']}'\n")
            f.write(f"   Occurrences: {conflict['occurrences']}\n")
            f.write(f"   Variations:\n")
            for variation in conflict['variations']:
                f.write(f"     - {variation}\n")
            f.write("\n")

    # Write merged output (sorted by role for easier reading)
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['role', 'normalized_role'])

        for role in sorted(final_mappings.keys()):
            writer.writerow([role, final_mappings[role]])

    # Print summary
    print(f"✓ Merged {len(final_mappings)} unique roles")
    print(f"✓ Found {len(conflicts)} conflicts (logged to {log_file})")
    print(f"✓ Output written to {output_file}")

    return len(final_mappings), len(conflicts)

if __name__ == "__main__":
    # File paths
    file1 = "dictionary/role_mappings.csv"
    file2 = "dictionary/roles.csv"
    output_file = "dictionary/roles_merged_full.csv"
    log_file = "dictionary/conflicts.log"

    # Run the merge
    merge_role_dictionaries(file1, file2, output_file, log_file)
