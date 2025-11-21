import pandas as pd
from pathlib import Path


def load_role_mapping(csv_path):
    """
    Load the role mapping dictionary from CSV file.

    Args:
        csv_path: Path to the CSV file containing role mappings

    Returns:
        dict: Dictionary mapping original roles (lowercase) to normalized roles
    """
    df = pd.read_csv(csv_path)
    # Create dictionary with lowercase keys for case-insensitive matching
    role_mapping = {str(row['role']).lower().strip(): str(row['normalized_role']).strip()
                    for _, row in df.iterrows()}
    return role_mapping


def normalize_contributors(contributors_text, role_mapping):
    """
    Normalize the contributors field according to the normalization rules.

    Args:
        contributors_text: The original contributors text
        role_mapping: Dictionary mapping roles to normalized roles

    Returns:
        str: Normalized contributors text
    """
    # Handle NaN or empty values
    if pd.isna(contributors_text) or str(contributors_text).strip() == '':
        return contributors_text

    contributors_text = str(contributors_text)

    # Preprocessing: replace square brackets with spaces
    contributors_text = contributors_text.replace('[', ' ').replace(']', ' ')

    # Split by semicolon to get individual contributor entries
    entries = contributors_text.split(';')

    normalized_entries = []

    for entry in entries:
        entry = entry.strip()

        if not entry:
            continue

        # Check if the entry contains a colon (role: name format)
        if ':' in entry:
            # Split by first colon only
            parts = entry.split(':', 1)
            if len(parts) == 2:
                role = parts[0].strip()
                name = parts[1].strip()

                # Normalize the role
                role_lower = role.lower()
                normalized_role = role_mapping.get(role_lower, "[RUOLO NON TROVATO]")

                # Check if there are multiple comma-separated names
                names = name.split(',')
                for individual_name in names:
                    individual_name = individual_name.strip()
                    if individual_name:  # Only add non-empty names
                        normalized_entries.append(f"{normalized_role}: {individual_name}")
            else:
                # Edge case: colon but can't split properly
                normalized_entries.append(entry)
        else:
            # No colon found, split by comma and assign default role "contributor" to each name
            names = entry.split(',')
            for name in names:
                name = name.strip()
                if name:  # Only add non-empty names
                    normalized_entries.append(f"contributor: {name}")

    # Join back with semicolons
    return '; '.join(normalized_entries)


def process_dataframe(df, role_mapping, keep_original=False):
    """
    Process the dataframe and normalize the contributors column.

    Args:
        df: Input dataframe
        role_mapping: Dictionary mapping roles to normalized roles
        keep_original: If True, keep original contributors as 'contributors_original'
                      and create new 'contributors' with normalized values.
                      If False, replace 'contributors' with normalized values.

    Returns:
        pd.DataFrame: Dataframe with normalized contributors column
    """
    # Check if 'contributors' column exists
    if 'contributors' not in df.columns:
        print("Warning: 'contributors' column not found in dataframe")
        print(f"Available columns: {df.columns.tolist()}")
        return df

    # Create a copy to avoid modifying the original dataframe
    df = df.copy()

    if keep_original:
        # Rename original column to contributors_original
        df['contributors_original'] = df['contributors']

    # Apply normalization to create the new contributors column
    df['contributors'] = df['contributors'].apply(
        lambda x: normalize_contributors(x, role_mapping)
    )

    return df


def main():
    """Main function to execute the normalization script."""

    # Define paths
    input_path = Path('input/DIRTY_dataset_dottori_di_ricerca.xlsx')
    output_path = Path('output/CLEAN_dataset_dottori_di_ricerca.xlsx')
    dictionary_path = Path('dictionary/roles.csv')

    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Loading role mapping dictionary...")
    role_mapping = load_role_mapping(dictionary_path)
    print(f"Loaded {len(role_mapping)} role mappings")

    print(f"\nReading input file: {input_path}")
    df = pd.read_excel(input_path)
    print(f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns")

    print("\nNormalizing contributors column...")
    df_normalized = process_dataframe(df, role_mapping, keep_original=True)

    print(f"\nSaving normalized data to: {output_path}")
    df_normalized.to_excel(output_path, index=False)

    print("✓ Normalization complete!")

    # Print some statistics
    if 'contributors' in df.columns:
        original_nulls = df['contributors'].isna().sum()
        normalized_nulls = df_normalized['contributors'].isna().sum()
        print(f"\nStatistics:")
        print(f"  - Total rows: {len(df)}")
        print(f"  - Null contributors (before): {original_nulls}")
        print(f"  - Null contributors (after): {normalized_nulls}")


if __name__ == "__main__":
    main()
