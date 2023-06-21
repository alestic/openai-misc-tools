# NAME
openai-tokens-count - counts the number of tokens in text files according to a specified OpenAI model

# SYNOPSIS
```
openai-tokens-count [options] file...
```

# DESCRIPTION
openai-tokens-count reads the specified text files and computes the number of tokens for each file as per the OpenAI model's specifications.

If no file is specified, or if the file is -, openai-tokens-count reads from standard input.

The number of tokens and file name are then printed to standard output.

# OPTIONS
## --model MODEL_NAME
Specifies the OpenAI model to use for counting tokens. Defaults to "gpt-4-0314".

## file
The text file to count tokens in. Multiple files can be specified. If no file is provided or if the file is '-', openai-tokens-count reads from standard input.

# EXAMPLES
Count tokens in a single file:
```
./openai-tokens-count example.txt
```

Count tokens in multiple files:
```
./openai-tokens-count file1.txt file2.txt
```

Count tokens in standard input:
```
cat example.txt | ./openai-tokens-count
```

Count tokens using a different model:
```
./openai-tokens-count --model "gpt-3.5-turbo-0301" example.txt
```

# AUTHORS
Written by GPT-4.
Prompt engineering by Eric Hammond.
Some code Copyright (c) 2023 OpenAI

# DATE
2023-06-20
