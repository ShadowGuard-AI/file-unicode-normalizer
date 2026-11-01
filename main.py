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

    if Path(input_file).resolve() == Path(output_file).resolve():
        logging.error(f"Refusing in-place output: output path '{output_file}' resolves to the input file '{input_file}'.")
        raise ValueError("Output path resolves to the input file; refusing to overwrite the input.")

    try:
        # Strict UTF-8 in and out. A file in any other encoding fails at this
        # read with UnicodeDecodeError rather than being detected or converted,
        # and a byte order mark, if present, is treated as a character and
        # survives normalization at the front of the output.
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()

        normalized_content = unicodedata.normalize(normalization_form, content)

        # The changed count is an estimate with a known flaw. It compares the
        # two strings position by position up to the shorter length, then adds
        # the length difference. One character early on that composes or
        # decomposes shifts every later position, so a one character change
        # can be counted as hundreds. The equality check below is the exact
        # test; this number is only a size hint in the log.
        changed = sum(1 for a, b in zip(content, normalized_content) if a != b) + abs(len(content) - len(normalized_content))
        logging.info(f"Characters changed: {changed}")

        # Already in the requested form means no output file is written and
        # the function returns None, which main turns into exit 1. A caller
        # scripting around this tool asked for a normalized copy, and an
        # absent output with a failure code says plainly that none was made.
        if normalized_content == content:
            logging.info(f"Nothing was changed: '{input_file}' is already in {normalization_form} form (0 characters changed).")
            return None

        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(normalized_content)

        logging.info(f"Successfully normalized '{input_file}' to '{output_file}' using {normalization_form}")
        return changed

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
        description="Normalizes Unicode characters in a file to a consistent form. Input must be UTF-8 encoded text."
    )
    parser.add_argument("input_file", type=Path, help="Path to the input file. The input file must be UTF-8 encoded text.")
    parser.add_argument("output_file", type=Path, help="Path to the output file. It must not be the input file itself.")
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

        result = normalize_unicode(args.input_file, args.output_file, args.form)
        if result is None:
            sys.exit(1)

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