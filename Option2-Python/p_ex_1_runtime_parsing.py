"""
ex_1_runtime_parsing.json contains a list of entries representing runtime of specific operation in associated software. 

Write a program in Python which:
- accepts as an input json file,
- parses the the file, calculates and prints:
    - operation, which is taking the longest when summed from all entries,
    - list of softwares from the one taking the longest, to the one running the shortest.
        
What kind of error handling would you implement? What should be done about invalid entries?
"""
import argparse
import json
import os
import sys
import pandas as pd
import logging as log

def calculate_longest_operation(df: pd.DataFrame) -> dict:
    # 2. operation, which is taking the longest when summed from all entries
    pivot_table = pd.pivot_table(
        df, columns=("operation"), values="length", aggfunc="sum"
    ).T
    pivot_table = pivot_table.sort_values(by="length", ascending=False)
    return pivot_table[:1].reset_index()


def calculate_longest_operation_per_software(df: pd.DataFrame) -> dict:
    # 1. operation, which is taking the longest split by software
    pivot_table = pd.pivot_table(
        df, columns=("software", "operation"), values="length", aggfunc="sum"
    ).T
    pivot_table = pivot_table.sort_values(by="length", ascending=False)
    return pivot_table.reset_index()


def calculate_software_longest_to_shortest(df: pd.DataFrame) -> dict:
    # 3. list of softwares from the one taking the longest, to the one running the shortest.
    pivot_table = pd.pivot_table(
        df, columns=("software"), values="length", aggfunc="sum"
    ).T
    pivot_table = pivot_table.sort_values(by="length", ascending=False)
    return pivot_table.reset_index()


REQUIRED_COLUMNS = ["length", "software", "operation"]
AVALIABLE_TRANSFORMATIONS = {
    "longest_operation": calculate_longest_operation,
    "longest_operation_per_software": calculate_longest_operation_per_software,
    "software_longest_to_shortest": calculate_software_longest_to_shortest,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("file", type=str, help="Path to json file")
    parser.add_argument(
        "--strict", action="store_true", help="Enable strict mode (check if all values are present and if time is not negative)"
    )
    parser.add_argument(
        "--output-format",
        default="human",
        choices=["human", "json"],
        help="Output format (json or human-readable)",
    )
    parser.add_argument(
        "--enabled-transformations",
        nargs="+",
        choices=AVALIABLE_TRANSFORMATIONS.keys(),
        type=str,
        default=AVALIABLE_TRANSFORMATIONS.keys(),
        help="List of transformations to perform",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()


def setup_logging():
    log.basicConfig(level=log.INFO, format="%(levelname)s %(message)s")


def validate_required_columns_present(df: pd.DataFrame, required_columns: list):
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Required column not pressent in file: {column}")


def validate_file_exists(file_path: str):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")


def validate_df_not_empty(df: pd.DataFrame):
    if df.empty:
        raise ValueError(f"No data in file")


def validate_no_missing_values(df: pd.DataFrame):
    nan_values = df.isna().any()
    if nan_values.any():
        raise ValueError(
            f"Missing values in columns: {df.columns[nan_values].tolist()}"
        )


def validate_no_negative_time_values(df: pd.DataFrame):
    negative_values = df["length"] < 0
    if negative_values.any():
        raise ValueError(f"Negative values in length column")


def report_error_and_exit(msg: str):
    log.critical(msg)
    sys.exit(1)


def main():
    args = parse_args()
    setup_logging()
    try:
        validate_file_exists(args.file)
        operations_runtime_df = pd.read_json(args.file, orient="records")
        validate_df_not_empty(operations_runtime_df)
        validate_required_columns_present(operations_runtime_df, REQUIRED_COLUMNS)
    except FileNotFoundError as e:
        report_error_and_exit(f"File not found: {args.file}")
    except ValueError as e:
        report_error_and_exit(f"Invalid json file: {e}")

    if args.strict:
        try:
            validate_no_negative_time_values(operations_runtime_df)
            validate_no_missing_values(operations_runtime_df)
        except ValueError as e:
            report_error_and_exit(f"Strict check failed: {e}")

    try:
        operations_runtime_df = operations_runtime_df.astype(
            {"length": float, "software": str, "operation": str}
        )
    except ValueError as e:
        report_error_and_exit(f"Invalid entry: {e}")

    results = {}
    for transformation_name in args.enabled_transformations:
        results[transformation_name] = AVALIABLE_TRANSFORMATIONS[transformation_name](
            operations_runtime_df
        )

    if args.output_format == "json":
        result_json = {}
        for transformation_name, result in results.items():
            result_json[transformation_name] = result.to_dict()
        print(json.dumps(result_json))
    else:
        for transformation_name, result in results.items():
            print(f"# {transformation_name}:\n{result}")


if __name__ == "__main__":
    main()
