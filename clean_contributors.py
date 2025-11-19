"""
Script to extract and identify non-name words from contributors column in Excel file.
"""

# ============================================================================
# IMPORTS
# ============================================================================
import pandas as pd
import re
import csv
from pathlib import Path


# ============================================================================
# GLOBAL CONFIGURATION VARIABLES - DATASET PATHS
# ============================================================================

# Input Excel file
EXCEL_FILE = 'DIRTY_dataset_dottori_di_ricerca.xlsx'

# Names dataset folder (includes .txt files and name_dataset/data/*.csv)
NAMES_FOLDER = 'names'

# Names CSV files configuration
# Option 1: Use all CSV files in name_dataset/data/ folder
NAMES_CSV_FILES = None
# Option 2: Use only specific country CSV files
# NAMES_CSV_FILES = ['US', 'IT', 'ES', 'FR', 'DE']

# Cities dataset folder
CITIES_FOLDER = 'cities'

# Roles dataset file
ROLES_FILE = 'roles/roles.txt'

# Words to exclude dataset file
TO_EXCLUDE_FILE = 'to_exclude/to_exclude.txt'

# Output files
OUTPUT_FILE = 'output.txt'
ALL_WORDS_FILE = 'all_unique_words.txt'
ALL_CITIES_FILE = 'all_city_names.txt'


# ============================================================================
# DATASET LOADING FUNCTIONS
# ============================================================================

def load_names_datasets(names_folder):
    """
    Load all names and surnames from the datasets in the names folder.

    This includes:
    - All .txt files in the names folder
    - All .csv files in names/name_dataset/data/ folder

    Returns:
        set: A set of all unique names/surnames (normalized to lowercase)
    """
    names_path = Path(names_folder)
    all_names = set()

    # Load all text files in the names folder
    for file_path in names_path.glob('*.txt'):
        print(f"Loading {file_path.name}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Clean and normalize each name/surname
                name = line.strip().lower()
                if name:
                    all_names.add(name)

    # Load CSV files from name_dataset/data folder
    csv_folder = names_path / 'name_dataset' / 'data'

    if csv_folder.exists():
        # Determine which CSV files to load
        if NAMES_CSV_FILES is None:
            # Load all CSV files in the folder
            csv_files = sorted(csv_folder.glob('*.csv'))
            print(f"Loading ALL CSV files: Found {len(csv_files)} CSV files in {csv_folder}")
        else:
            # Load only specified CSV files
            csv_files = [csv_folder / f"{country}.csv" for country in NAMES_CSV_FILES]
            # Filter out files that don't exist
            csv_files = [f for f in csv_files if f.exists()]
            print(f"Loading SPECIFIC CSV files: {', '.join(NAMES_CSV_FILES)}")
            print(f"Found {len(csv_files)} CSV files in {csv_folder}")

        for csv_path in csv_files:
            print(f"Loading {csv_path.name}...")
            with open(csv_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    if len(row) >= 2:
                        # Extract first name (column 0) and last name (column 1)
                        first_name = row[0].strip()
                        last_name = row[1].strip()

                        # Split multi-word names and add each word
                        # Replace hyphens and periods with spaces to split hyphenated/abbreviated names
                        first_name = first_name.replace('-', ' ').replace('.', ' ')
                        last_name = last_name.replace('-', ' ').replace('.', ' ')

                        for name_part in first_name.split():
                            cleaned = name_part.lower()
                            if cleaned:
                                all_names.add(cleaned)

                        for name_part in last_name.split():
                            cleaned = name_part.lower()
                            if cleaned:
                                all_names.add(cleaned)
    else:
        print(f"Warning: CSV folder not found at {csv_folder}")

    print(f"Loaded {len(all_names)} unique names/surnames from datasets")
    return all_names


def load_cities_datasets(cities_folder):
    """
    Load all city names from the cities dataset, preserving order of first appearance.

    Returns:
        list: A list of all unique city name words (normalized to lowercase)
    """
    cities_path = Path(cities_folder)
    all_cities = {}  # Use dict to preserve insertion order

    # Load cities.csv file
    csv_path = cities_path / 'cities.csv'

    if csv_path.exists():
        print(f"Loading cities from {csv_path.name}...")
        with open(csv_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            # Skip header row
            next(csv_reader, None)

            for row in csv_reader:
                if len(row) >= 2:
                    # Extract city name (column 1) - CSV reader handles quoted fields automatically
                    city_name = row[1].strip()

                    # Split multi-word city names and add each word
                    # First replace hyphens and periods with spaces to split hyphenated/abbreviated names
                    city_name = city_name.replace('-', ' ').replace('.', ' ')
                    for city_part in city_name.split():
                        # Replace punctuation with spaces
                        cleaned = re.sub(r'[^\w\s]', ' ', city_part).strip().lower()
                        # Split again in case punctuation created new spaces
                        for word_part in cleaned.split():
                            if word_part and word_part not in all_cities:
                                all_cities[word_part] = None  # Use dict to track order
    else:
        print(f"Warning: cities.csv not found at {csv_path}")

    print(f"Loaded {len(all_cities)} unique city name words from dataset")
    return list(all_cities.keys())  # Return as list preserving order


def load_roles(roles_file):
    """
    Load all roles from the roles file.

    Returns:
        set: A set of all unique roles (normalized to lowercase)
    """
    all_roles = set()
    roles_path = Path(roles_file)

    if roles_path.exists():
        print(f"Loading roles from {roles_path.name}...")
        with open(roles_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Clean and normalize each role
                role = line.strip().lower()
                if role:
                    all_roles.add(role)
    else:
        print(f"Warning: roles file not found at {roles_path}")

    print(f"Loaded {len(all_roles)} unique roles from file")
    return all_roles


def load_to_exclude(to_exclude_file):
    """
    Load all words to exclude from the to_exclude file.

    Returns:
        set: A set of all words to exclude (normalized to lowercase)
    """
    to_exclude = set()
    to_exclude_path = Path(to_exclude_file)

    if to_exclude_path.exists():
        print(f"Loading words to exclude from {to_exclude_path.name}...")
        with open(to_exclude_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Clean and normalize each word
                word = line.strip().lower()
                if word:
                    to_exclude.add(word)
    else:
        print(f"Warning: to_exclude file not found at {to_exclude_path}")

    print(f"Loaded {len(to_exclude)} words to exclude from file")
    return to_exclude


# ============================================================================
# DATA PROCESSING FUNCTIONS
# ============================================================================

def remove_duplicates(file_path):
    """
    Remove duplicate lines from a file while preserving order of first appearance.

    Args:
        file_path: Path to the file to clean

    Returns:
        int: Number of unique lines after removing duplicates
    """
    seen = set()
    unique_lines = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Strip whitespace for comparison
            cleaned = line.strip()

            # Keep the line if we haven't seen it before (case-insensitive)
            if cleaned and cleaned.lower() not in seen:
                seen.add(cleaned.lower())
                unique_lines.append(cleaned)

    # Write back to the same file
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in unique_lines:
            f.write(line + '\n')

    print(f"Removed duplicates from {Path(file_path).name}")
    print(f"Unique entries: {len(unique_lines)}")
    return len(unique_lines)


def clean_and_extract_words(contributors_series):
    """
    Extract unique words from contributors column after cleaning, preserving order of first appearance.

    Args:
        contributors_series: A pandas Series containing contributor data

    Returns:
        list: A list of unique words in order of first appearance
    """
    all_words = {}  # Use dict to preserve insertion order (Python 3.7+)

    for value in contributors_series:
        if pd.isna(value):
            continue

        # Convert to string and replace common delimiters with spaces
        text = str(value)
        # Replace various delimiters with spaces (including hyphens and periods)
        delimiters = [':', ';', ',', '|', '/', '\\', '(', ')', '[', ']', '{', '}', '\t', '\n', '\r', '-', '.']
        for delimiter in delimiters:
            text = text.replace(delimiter, ' ')

        # Split into words and normalize
        words = text.split()
        for word in words:
            # Replace any remaining punctuation with spaces and normalize to lowercase
            cleaned_word = re.sub(r'[^\w\s]', ' ', word).strip().lower()
            # Split again in case punctuation created new spaces (e.g., "d'annunzio" -> "d annunzio" -> ["d", "annunzio"])
            for word_part in cleaned_word.split():
                if word_part and word_part not in all_words:
                    all_words[word_part] = None  # Use dict to track order

    print(f"Extracted {len(all_words)} unique words from contributors column")
    return list(all_words.keys())  # Return as list preserving order


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main function to process the Excel file and identify non-name words."""

    print("=" * 80)
    print("STEP 1: READING INPUT DATA")
    print("=" * 80)

    # Read the Excel file
    print(f"Reading Excel file: {EXCEL_FILE}...")
    df = pd.read_excel(EXCEL_FILE)

    print(f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns")
    print(f"Columns: {df.columns.tolist()}")

    # Check if contributors column exists
    if 'contributors' not in df.columns:
        print("ERROR: 'contributors' column not found in the Excel file!")
        print(f"Available columns: {df.columns.tolist()}")
        return

    # Extract and clean unique words from contributors column
    print("\nExtracting and cleaning words from contributors column...")
    unique_words = clean_and_extract_words(df['contributors'])

    # Output all unique words to intermediate file
    print(f"\nWriting all unique words to {ALL_WORDS_FILE}...")
    with open(ALL_WORDS_FILE, 'w', encoding='utf-8') as f:
        # Write words in order of first appearance
        for word in unique_words:
            f.write(word + '\n')
    print(f"Done! All unique words saved to {ALL_WORDS_FILE}")

    print("\n" + "=" * 80)
    print("STEP 2: CLEANING AND LOADING FILTERING DATASETS")
    print("=" * 80)

    # Clean the to_exclude file by removing duplicates
    print(f"\n[0/4] Cleaning duplicates from: {TO_EXCLUDE_FILE}")
    remove_duplicates(TO_EXCLUDE_FILE)

    # Load roles dataset
    print(f"\n[1/4] Loading roles dataset from: {ROLES_FILE}")
    known_roles = load_roles(ROLES_FILE)

    # Load all names and surnames datasets
    print(f"\n[2/4] Loading names and surnames datasets from: {NAMES_FOLDER}")
    known_names = load_names_datasets(NAMES_FOLDER)

    # Load city names dataset
    print(f"\n[3/4] Loading city names dataset from: {CITIES_FOLDER}")
    known_cities = load_cities_datasets(CITIES_FOLDER)

    # Output all city names to intermediate file
    print(f"\nWriting all city names to {ALL_CITIES_FILE}...")
    with open(ALL_CITIES_FILE, 'w', encoding='utf-8') as f:
        # Write cities in order of first appearance
        for city in known_cities:
            f.write(city + '\n')
    print(f"Done! All city names saved to {ALL_CITIES_FILE}")

    # Load words to exclude (already cleaned)
    print(f"\n[4/4] Loading words to exclude dataset from: {TO_EXCLUDE_FILE}")
    to_exclude = load_to_exclude(TO_EXCLUDE_FILE)

    print("\n" + "=" * 80)
    print("STEP 3: FILTERING AND GENERATING OUTPUT")
    print("=" * 80)

    print("\nComparing words against names/surnames/cities/roles/to_exclude datasets...")
    output = [word for word in unique_words if word not in known_names and word not in known_cities and word not in known_roles and word not in to_exclude]

    # Output to text file
    print(f"\nWriting results to {OUTPUT_FILE}...")

    words_written = 0
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for word in output:
            if not any(char.isdigit() for char in word):
                f.write(word + '\n')
                words_written += 1

    print(f"Found {words_written} words that could be roles")

    print(f"Done! Results saved to {OUTPUT_FILE}")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"  - Total unique words extracted: {len(unique_words)}")
    print(f"  - Known names/surnames in datasets: {len(known_names)}")
    print(f"  - Known city names in dataset: {len(known_cities)}")
    print(f"  - Known roles in dataset: {len(known_roles)}")
    print(f"  - Words to exclude in dataset: {len(to_exclude)}")
    print(f"  - Words that are NOT names/surnames/cities/roles/to_exclude: {len(output)}")
    print(f"  - Words written to output (excluding roles and numbers): {words_written}")
    print(f"\nOutput files:")
    print(f"  - All unique words: {ALL_WORDS_FILE}")
    print(f"  - All city names: {ALL_CITIES_FILE}")
    print(f"  - Filtered results: {OUTPUT_FILE}")
    print("=" * 80)


if __name__ == '__main__':
    main()
