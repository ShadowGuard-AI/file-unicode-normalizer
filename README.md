![Banner](banner.png)

# file-unicode-normalizer
Normalizes Unicode characters within a file to a consistent form (e.g., NFC, NFKD), preventing subtle encoding-related vulnerabilities and inconsistencies. - Focused on File operations and analysis. The input file must be UTF-8 encoded text; input in any other encoding is rejected. The output path must be a different file from the input: a run whose output path resolves to the input file is refused at exit 1 and the input is left untouched. Each run logs the number of characters changed; if nothing changes (including an empty input), the run prints a nothing was changed line and exits 1 instead of reporting success.

## Install
`git clone https://github.com/ShadowGuardAI/file-unicode-normalizer`

## Usage
`./file-unicode-normalizer [params]`

## Parameters
- `-h`: Show help message and exit
- `--form`: No description provided
- `--log_level`: No description provided

## License
Copyright (c) ShadowGuardAI
