# openai-tokens

This Python package provides utilities for working with OpenAI model tokens. These tools allow you to count the number of tokens in text files and to output the first N tokens from text files, according to the specifications of a specified OpenAI model.

NOTE: This code is not affiliated with or supported by OpenAI.

## Installation

To install the package, clone the repository from GitHub:

```
git clone https://github.com/alestic/openai-tokens.git
cd openai-tokens
pip install .
```

## Usage

The package currently includes the following tools:

1. `openai-tokens-count`
2. `openai-tokens-head`

### openai-tokens-count

Counts the number of tokens in text files according to a specified OpenAI model.

```
usage: openai-tokens-count [options] file...
```

`openai-tokens-count` reads the specified text files and computes the number of tokens for each file as per the OpenAI model's specifications. If no file is specified, or if the file is -, `openai-tokens-count` reads from standard input. The number of tokens and file name are then printed to standard output.

#### Options

- `--model MODEL_NAME`: Specifies the OpenAI model to use for counting tokens. Defaults to "gpt-4-0314".
- `file`: The text file to count tokens in. Multiple files can be specified. If no file is provided or if the file is '-', `openai-tokens-count` reads from standard input.

#### Examples

Count tokens in a single file:
```
openai-tokens-count example.txt
```

Count tokens in multiple files:
```
openai-tokens-count file1.txt file2.txt
```

Count tokens in standard input:
```
cat example.txt | openai-tokens-count
```

Count tokens using a different model:
```
openai-tokens-count --model "gpt-3.5-turbo-0301" example.txt
```

### openai-tokens-head

Outputs the first `--tokens COUNT` tokens from the input file(s) or stdin.

```
usage: openai-tokens-head [options] file...
```

`openai-tokens-head` reads the specified text files and outputs the first `--tokens COUNT` tokens according to the OpenAI model's specifications. With more than one FILE, precede each with a header giving the file name. If no file is specified, or if the file is -, `openai-tokens-head` reads from standard input.

#### Options

- `-n, --tokens COUNT`: Output the first COUNT tokens. If COUNT is 0, output nothing.
- `--model MODEL_NAME`: Specifies the OpenAI model to use for tokenizing. Defaults to "gpt-4-0314".
- `file`: The text file to get tokens from. Multiple files can be specified. If no file is provided or if the file is '-', `openai-tokens-head` reads from standard input.

#### Examples

Output the first 100 tokens from a file:
```
openai-tokens-head -n 100 example.txt
```

Output the first 50 tokens using a different model:
```
openai-tokens-head --model "gpt-3.5-turbo-0301" -n 50 example.txt
```

## Authors

- Written by GPT-4.
- Prompt engineering by Eric Hammond.
- Some code Copyright (c) 2023 OpenAI

## License

This project is licensed under the terms of the MIT license.
