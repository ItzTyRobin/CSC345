"""
Basically takes .jack files and turns them into tokenized XML
"""

import os
import sys
from pathlib import Path

from tokenizer import Tokenizer, TokenType


def get_output_filename(jack_file_path):
    """
    Converts Xxx.jack → XxxT.xml
    """
    base_name = os.path.splitext(jack_file_path)[0]
    return f"{base_name}T.xml"


def tokenize_file(jack_file_path, output_file_path):
    """
    Tokenize a single file and write the results as XML
    """
    try:
        # read the source file
        with open(jack_file_path, 'r') as f:
            source_code = f.read()

        # run tokenizer
        tokenizer = Tokenizer(source_code)
        tokens = tokenizer.get_tokens()

        # write XML output
        with open(output_file_path, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<tokens>\n')

            for token in tokens:
                tag_name = token.type.value.lower()

                # handle special XML characters
                value = token.value
                value = value.replace('&', '&amp;')
                value = value.replace('<', '&lt;')
                value = value.replace('>', '&gt;')
                value = value.replace('"', '&quot;')

                f.write(f'  <{tag_name}> {value} </{tag_name}>\n')

            f.write('</tokens>\n')

        return True, len(tokens), None

    except Exception as e:
        return False, 0, str(e)


def process_jack_file(jack_file_path):
    """
    Handles one .jack file
    """
    output_file_path = get_output_filename(jack_file_path)
    success, token_count, error = tokenize_file(jack_file_path, output_file_path)

    if success:
        print(f"✓ {os.path.basename(jack_file_path):<25} → {output_file_path}")
        return True, token_count
    else:
        print(f"✗ {os.path.basename(jack_file_path):<25} → ERROR: {error}")
        return False, 0


def process_folder(folder_path):
    """
    Runs tokenizer on every .jack file in a folder
    """
    jack_files = sorted([
        f for f in os.listdir(folder_path)
        if f.endswith('.jack') and os.path.isfile(os.path.join(folder_path, f))
    ])

    if not jack_files:
        print(f"✗ No .jack files found in {folder_path}")
        return False

    all_success = True
    total_tokens = 0

    print(f"Processing folder: {folder_path}")
    print("-" * 70)

    for jack_file in jack_files:
        file_path = os.path.join(folder_path, jack_file)
        success, token_count = process_jack_file(file_path)

        if success:
            total_tokens += token_count
        else:
            all_success = False

    print("-" * 70)
    print(f"Total files processed: {len(jack_files)}")
    print(f"Total tokens generated: {total_tokens}")

    return all_success


def main():
    """
    Entry point for the analyzer
    """
    if len(sys.argv) < 2:
        print("Usage: python JackAnalyzer.py <source>")
        print("")
        print("  <source> can be:")
        print("    - a single .jack file")
        print("    - a folder with .jack files")
        print("")
        print("Output:")
        print("  generates a corresponding XxxT.xml file for each input")
        sys.exit(1)

    source = sys.argv[1]

    # figure out if it's a file or folder
    if source.endswith('.jack'):
        if not os.path.exists(source):
            print(f"✗ File not found: {source}")
            sys.exit(1)

        print("=" * 70)
        print("JACK ANALYZER - TOKENIZER")
        print("=" * 70)
        print(f"Processing file: {source}")
        print("-" * 70)

        success, token_count = process_jack_file(source)

        print("-" * 70)
        print(f"Total tokens generated: {token_count}")

        sys.exit(0 if success else 1)

    else:
        if not os.path.isdir(source):
            print(f"✗ Folder not found: {source}")
            sys.exit(1)

        print("=" * 70)
        print("JACK ANALYZER - TOKENIZER")
        print("=" * 70)

        success = process_folder(source)

        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()