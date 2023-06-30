#!/usr/bin/env python3
"""
NAME
    openai-tokens-count - counts the number of tokens in text files
    according to a specified OpenAI model

SYNOPSIS
    openai-tokens-count [options] file...

DESCRIPTION
    openai-tokens-count reads the specified text files and computes the
    number of tokens for each file as per the OpenAI model's
    specifications.

    If no file is specified, or if the file is -, openai-tokens-count
    reads from standard input.

    The number of tokens and file name are then printed to standard
    output.

OPTIONS
    --model MODEL_NAME
        Specifies the OpenAI model to use for counting
        tokens. Defaults to "gpt-4-0314".
    
    file
        The text file to count tokens in. Multiple files can be
        specified. If no file is provided or if the file is '-',
        openai-tokens-count reads from standard input.

EXAMPLES
    Count tokens in a single file:
    openai-tokens-count example.txt

    Count tokens in multiple files:
    openai-tokens-count file1.txt file2.txt

    Count tokens in standard input:
    cat example.txt | openai-tokens-count

    Count tokens using a different model:
    openai-tokens-count --model "gpt-3.5-turbo-0301" example.txt

AUTHORS
    Written by GPT-4.
    Prompt engineering by Eric Hammond.
    Some code Copyright (c) 2023 OpenAI

DATE
    2023-06-20
"""

import argparse
import sys
from . import openai_tokens


# Constants
#DEFAULT_MODEL = "gpt-4-0613"
DEFAULT_MODEL = "gpt-4-0314"
MIN_WIDTH = 7

def main():
    parser = argparse.ArgumentParser(description='Counts the number of tokens in the given files.')
    parser.add_argument('files', metavar='F', type=argparse.FileType('r'), nargs='*',
                        help='a file for token counting',
                        default=[sys.stdin])
    parser.add_argument('--model', default=DEFAULT_MODEL,
                        help='the OpenAI model to use (default: {})'.format(DEFAULT_MODEL))
    args = parser.parse_args()

    total = 0
    results = []
    for file in args.files:
        num_tokens = openai_tokens.count_tokens_in_file(file, args.model)
        results.append((num_tokens, file.name))
        total += num_tokens

    for num_tokens, file_name in results:
        print(f"{num_tokens:>{MIN_WIDTH}} {file_name}")

    if len(results) > 1:
        print(f"{total:>{MIN_WIDTH}} total")

if __name__ == '__main__':
    main()
