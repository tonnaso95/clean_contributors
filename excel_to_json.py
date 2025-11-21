import pandas as pd
from pathlib import Path


def convert_excel_to_json(input_path, output_path, orient='records', indent=2):
    """
    Convert an Excel file to JSON format.

    Args:
        input_path: Path to the input Excel file
        output_path: Path to the output JSON file
        orient: Format of JSON string (default: 'records')
                - 'records': list of rows as dict objects [{col -> value}, ...]
                - 'index': dict like {index -> {column -> value}}
                - 'columns': dict like {column -> {index -> value}}
                - 'values': just the values array
                - 'table': dict like {'schema': {schema}, 'data': {data}}
        indent: Number of spaces for JSON indentation (default: 2)

    Returns:
        pd.DataFrame: The loaded dataframe
    """
    print(f"Reading Excel file: {input_path}")
    df = pd.read_excel(input_path)
    print(f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns")

    # Clean unusual line terminators from all string columns
    print("\nCleaning unusual line terminators...")
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(
            lambda x: x.replace('\u2028', ' ').replace('\u2029', ' ') if isinstance(x, str) else x
        )

    print(f"\nConverting to JSON format (orient='{orient}')...")
    print(f"Writing to: {output_path}")

    # Convert to JSON and save
    df.to_json(output_path, orient=orient, indent=indent, force_ascii=False)

    print("✓ Conversion complete!")

    return df


def main():
    """Main function to execute the Excel to JSON conversion."""

    # Define paths
    input_path = Path('output/CLEAN_dataset_dottori_di_ricerca.xlsx')
    output_path = Path('output/CLEAN_dataset_dottori_di_ricerca.json')

    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if input file exists
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return

    # Convert Excel to JSON
    df = convert_excel_to_json(input_path, output_path, orient='records', indent=2)

    # Print statistics
    print(f"\nStatistics:")
    print(f"  - Total rows: {len(df)}")
    print(f"  - Total columns: {len(df.columns)}")
    print(f"  - Columns: {', '.join(df.columns.tolist())}")

    # Get file sizes
    input_size = input_path.stat().st_size / (1024 * 1024)  # MB
    output_size = output_path.stat().st_size / (1024 * 1024)  # MB

    print(f"\nFile sizes:")
    print(f"  - Input (XLSX): {input_size:.2f} MB")
    print(f"  - Output (JSON): {output_size:.2f} MB")


if __name__ == "__main__":
    main()
