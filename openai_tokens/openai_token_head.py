#!/usr/bin/env python3
"""
NAME
    openai-token-head - output the first `--tokens COUNT` tokens from
    the input file(s) or stdin

SYNOPSIS
    openai-token-head [options] file...

DESCRIPTION
    openai-token-head reads the specified text files and outputs the first
    `--tokens COUNT` tokens according to the OpenAI model's specifications.
    With more than one FILE, precede each with a header giving the file name.

    If no file is specified, or if the file is -, openai-token-head
    reads from standard input.

OPTIONS
    -n, --tokens COUNT
        Output the first COUNT tokens. If COUNT is 0, output nothing.
    
    --model MODEL_NAME
        Specifies the OpenAI model to use for tokenizing. Defaults to
        "gpt-4-0314".
    
    file
        The text file to get tokens from. Multiple files can be
        specified. If no file is provided or if the file is '-',
        openai-token-head reads from standard input.

EXAMPLES
    Output the first 100 tokens from a file:
    ./openai-token-head -n 100 example.txt

    Output the first 50 tokens using a different model:
    ./openai-token-head --model "gpt-3.5-turbo-0301" -n 50 example.txt

AUTHORS
    Written by GPT-4.
    Prompt engineering by Eric Hammond.
    Some code Copyright (c) 2023 OpenAI

DATE
    2023-06-20
"""

import argparse
import sys
import openai_tokens

# Constants
DEFAULT_MODEL = "gpt-4-0314"

def main():
    parser = argparse.ArgumentParser(description='Outputs the first COUNT tokens from the given files.')
    parser.add_argument('files', metavar='F', type=argparse.FileType('r'), nargs='*',
                        help='a file to get tokens from',
                        default=[sys.stdin])
    parser.add_argument('-n', '--tokens', type=int, required=True,
                        help='the number of tokens to output')
    parser.add_argument('--model', default=DEFAULT_MODEL,
                        help='the OpenAI model to use (default: {})'.format(DEFAULT_MODEL))
    args = parser.parse_args()

    if args.tokens < 0:
        print("Error: the number of tokens to output should be nonnegative.")
        return

    for i, file in enumerate(args.files):
        text = file.read()
        head_text = openai_tokens.head_tokens_text(text, args.model, args.tokens)
        if len(args.files) > 1:
            if i != 0:
                print()  # Add an extra newline between files
            print(f"==> {file.name} <==")
        print(f"{head_text}")

if __name__ == '__main__':
    main()
