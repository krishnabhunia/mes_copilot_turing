import argparse

# Create the argument parser
parser = argparse.ArgumentParser(description="Translator Script")

# Define required positional arguments
parser.add_argument('source_lang', help='Compulsory source language (e.g., fr)')
parser.add_argument('target_lang', help='Compulsory target language (e.g., en)')

# Define optional arguments
parser.add_argument('--input_folder', default=None, help='Optional input folder (default: None)')
parser.add_argument('--output_folder', default=None, help='Optional output folder (default: None)')

# Parse arguments
args = parser.parse_args()

# Print the values
print(f"Source Language: {args.source_lang}")
print(f"Target Language: {args.target_lang}")
print(f"Input Folder: {args.input_folder}")
print(f"Output Folder: {args.output_folder}")
