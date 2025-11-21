import json
from pathlib import Path
from collections import Counter


def extract_names_from_entry(entry):
    """
    Extract the names part from a contributor entry (after the colon).

    Args:
        entry: A single contributor entry like "role: Name1, Name2"

    Returns:
        str: The names part (everything after the colon), or empty string if no colon
    """
    if ':' in entry:
        parts = entry.split(':', 1)
        if len(parts) == 2:
            return parts[1].strip()
    return entry.strip()


def find_unmapped_roles(json_path):
    """
    Find all roles that were mapped to [RUOLO NON TROVATO].

    Args:
        json_path: Path to the CLEAN_contributors.json file

    Returns:
        Counter: Counter object with unmapped roles and their frequencies
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    unmapped_roles = []

    for entry in data:
        contributors = entry.get('contributors', '')
        contributors_original = entry.get('contributors_original', '')

        # Skip if either field is empty or None
        if not contributors or not contributors_original:
            continue

        # Check if this entry contains [RUOLO NON TROVATO]
        if '[RUOLO NON TROVATO]' not in contributors:
            continue

        # Split both fields by semicolon
        normalized_entries = [e.strip() for e in contributors.split(';')]
        original_entries = [e.strip() for e in contributors_original.split(';')]

        # Find entries with [RUOLO NON TROVATO] and match them to originals
        for norm_entry in normalized_entries:
            if '[RUOLO NON TROVATO]' in norm_entry:
                # Extract the names from the normalized entry
                norm_names = extract_names_from_entry(norm_entry)

                # Find the corresponding original entry by matching names
                for orig_entry in original_entries:
                    orig_names = extract_names_from_entry(orig_entry)

                    # If names match, extract the original role
                    if norm_names == orig_names:
                        # Extract the role (part before the colon)
                        if ':' in orig_entry:
                            original_role = orig_entry.split(':', 1)[0].strip()
                            unmapped_roles.append(original_role)
                        else:
                            # If there's no colon in original, it means the whole entry is a name
                            # This shouldn't happen for [RUOLO NON TROVATO] cases, but handle it
                            unmapped_roles.append("[NO ROLE IN ORIGINAL]")
                        break

    return Counter(unmapped_roles)


def main():
    """Main function to extract and display unmapped roles."""

    # Define paths
    input_path = Path('output/CLEAN_contributors.json')
    output_path = Path('output/unmapped_roles.txt')

    print(f"Reading file: {input_path}")

    if not input_path.exists():
        print(f"Error: File not found at {input_path}")
        return

    print("Extracting unmapped roles...")
    unmapped_roles = find_unmapped_roles(input_path)

    if not unmapped_roles:
        print("\nNo unmapped roles found!")
        return

    print(f"\nFound {len(unmapped_roles)} unique unmapped roles")
    print(f"Total occurrences: {sum(unmapped_roles.values())}")
    print("\n" + "="*60)
    print("UNMAPPED ROLES (sorted by frequency):")
    print("="*60)

    # Sort by frequency (descending)
    for role, count in unmapped_roles.most_common():
        print(f"{count:4d}x  {role}")

    # Save to file
    print(f"\nSaving results to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("UNMAPPED ROLES\n")
        f.write("="*60 + "\n")
        f.write(f"Total unique roles: {len(unmapped_roles)}\n")
        f.write(f"Total occurrences: {sum(unmapped_roles.values())}\n\n")
        f.write("Roles sorted by frequency:\n")
        f.write("-"*60 + "\n")
        for role, count in unmapped_roles.most_common():
            f.write(f"{count:4d}x  {role}\n")

        f.write("\n\nRoles sorted alphabetically:\n")
        f.write("-"*60 + "\n")
        for role in sorted(unmapped_roles.keys()):
            f.write(f"{unmapped_roles[role]:4d}x  {role}\n")

    print("✓ Done!")


if __name__ == "__main__":
    main()
