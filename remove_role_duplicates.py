#!/usr/bin/env python3
"""
Script to remove duplicate roles from roles.txt file.
Each line is considered a single element. Comparison is done case-insensitively,
and all entries are converted to lowercase in the output.
"""

# ============================================================================
# IMPORTS
# ============================================================================
from pathlib import Path


# ============================================================================
# CONFIGURATION
# ============================================================================

# Input/output file path
ROLES_FILE = "roles/roles.txt"


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def remove_role_duplicates(file_path):
    """
    Remove duplicate roles from the file.

    Process:
    - Each line is a separate element
    - Convert to lowercase for comparison and output
    - Preserve order of first appearance
    - Write unique roles back to the same file

    Args:
        file_path: Path to the roles file
    """
    roles_path = Path(file_path)

    if not roles_path.exists():
        print(f"ERROR: File not found at {roles_path}")
        return

    seen = set()
    unique_roles = []

    # Read the file and collect unique roles
    print(f"Reading {roles_path}...")
    with open(roles_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            # Strip whitespace and convert to lowercase
            cleaned = line.strip().lower()

            # Skip empty lines
            if not cleaned:
                continue

            # Keep the role if we haven't seen it before
            if cleaned not in seen:
                seen.add(cleaned)
                unique_roles.append(cleaned)
            else:
                print(f"  Duplicate found at line {line_number}: '{cleaned}'")

    # Write back to the same file
    print(f"\nWriting unique roles back to {roles_path}...")
    with open(roles_path, 'w', encoding='utf-8') as f:
        for role in unique_roles:
            f.write(role + '\n')

    # Print summary
    print(f"\n{'=' * 60}")
    print(f"SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total lines processed: {line_number}")
    print(f"Unique roles: {len(unique_roles)}")
    print(f"Duplicates removed: {line_number - len(unique_roles)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    remove_role_duplicates(ROLES_FILE)
