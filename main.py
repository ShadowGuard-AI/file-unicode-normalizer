import argparse
import logging
import unicodedata
from pathlib import Path
import os
import sys


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def normalize_unicode(input_file: Path, output_file: Path, normalization_form: str) -> None:
    """
    Normalizes Unicode characters in a file to a specified normalization form.

    Args:
        input_file (Path): Path to the input file.
        output_file (Path): Path to the output file.
        normalization_form (str): Unicode normalization form (e.g., NFC, NFKD, NFD, NFKC).

    Raises:
        ValueError: If the normalization form is invalid.
        FileNotFoundError: If the input file does not exist.
        OSError: If there are issues reading or writing files.
        UnicodeDecodeError: If the input file is not a valid UTF-8 encoded file.
    """

    if normalization_form not in ['NFC', 'NFKD', 'NFD', 'NFKC']:
        raise ValueError(f"Invalid normalization form: {normalization_form}")

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()

        normalized_content = unicodedata.normalize(normalization_form, content)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(normalized_content)

        logging.info(f"Successfully normalized '{input_file}' to '{output_file}' using {normalization_form}")

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        raise
    except OSError as e:
        logging.error(f"OS error: {e}")
        raise
    except UnicodeDecodeError as e:
        logging.error(f"Unicode decode error: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

def setup_argparse() -> argparse.ArgumentParser:
    """
    Sets up the argument parser for the command-line interface.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Normalizes Unicode characters in a file to a consistent form."
    )
    parser.add_argument("input_file", type=Path, help="Path to the input file.")
    parser.add_argument("output_file", type=Path, help="Path to the output file.")
    parser.add_argument(
        "--form",
        type=str,
        default="NFC",
        choices=["NFC", "NFKD", "NFD", "NFKC"],
        help="Unicode normalization form (default: NFC).",
    )
    parser.add_argument(
        "--log_level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO).",
    )
    return parser


def main() -> None:
    """
    Main function to parse arguments and execute the Unicode normalization.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    # Set logging level based on CLI argument
    logging.getLogger().setLevel(args.log_level)

    try:
        # Validate file paths: Check if input file is actually a file
        if not args.input_file.is_file():
             logging.error(f"Error: Input file '{args.input_file}' is not a valid file.")
             sys.exit(1)

        normalize_unicode(args.input_file, args.output_file, args.form)

    except ValueError as e:
        logging.error(f"ValueError: {e}")
        sys.exit(1)  # Exit with an error code
    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError: {e}")
        sys.exit(1)
    except OSError as e:
        logging.error(f"OSError: {e}")
        sys.exit(1)
    except UnicodeDecodeError as e:
        logging.error(f"UnicodeDecodeError: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Example Usage:
    # Create dummy files for testing (remove in production)
    # Example of creating a file with non-normalized Unicode characters.
    # echo "cafe\u0301" > input.txt # Creates "café" using combining acute accent
    # python main.py input.txt output.txt --form NFC
    # python main.py input.txt output.txt --form NFKD --log_level DEBUG
    main()