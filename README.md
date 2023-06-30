# openai-misc-tools

This Python package provides a collection of command-line utilities for working with OpenAI APIs. The tools in this package enable users to interact with OpenAI models in various ways, count tokens in text files, display the first N tokens from a file, and transcribe audio/video files using OpenAI's Whisper API. Each tool offers flexible configuration options to tailor usage to specific needs.

NOTE: This code is not affiliated with or supported by OpenAI.

## Tools

### `openai-chat`
This tool facilitates interactions with OpenAI models via the OpenAI API, providing a means to generate conversation completions in a chat format. It can be configured using command line options or a configuration file, enabling customization of the model used, conversation prompts, sampling parameters, and more. The tool also allows listing all "gpt-" prefixed models owned by OpenAI. An optional debug mode provides detailed information about interactions.

### `openai-tokens-count`
This tool allows users to count the number of tokens in specified text files according to a specified OpenAI model. If no file is specified or if '-' is provided as the file, the tool reads from standard input. The tool then prints the number of tokens and file name to standard output.

### `openai-tokens-head`
This tool reads specified text files and outputs the first `n` tokens according to the OpenAI model's specifications. The tool can output tokens from standard input if no file is specified or if '-' is given as the file. It allows specification of the model to use for tokenizing.

### `openai-transcribe`
This tool transcribes audio and/or video files using OpenAI's Whisper API. It reads specified files and prints the transcribed text to standard output. It also supports a verbose mode, which prints progress before each significant external step.

All these tools are planned to support a common configuration file, offering convenient and consistent tool configuration.

## Installation

To install the package, clone the repository from GitHub:

```sh
git clone https://github.com/alestic/openai-misc-tools.git
cd openai-misc-tools
pip install .
```

## Examples

```sh
# Run openai-chat
openai-chat --project comedy-tool --model gpt-4 --temperature 1.0 --system "You are a famous standup comedian (not an AI) performing on stage interacting with the audience." --user "Why is the sky blue?"

# Count tokens in all txt files in the current directory
openai-tokens-count *.txt

# Transcribe the audio in a video using openai-transcribe
openai-transcribe long-meeting.mp4 > long-meeting.txt
```

## Config

These tools use an INI file for configuration, with one section for each OpenAI project. The configuration file should include 'org_id' and 'api_key' parameters for the OpenAI organization ID and API key, respectively. It defaults to ~/.openai.conf, but this can be overridden with the OPENAI_CONFIG environment variable or the --config command line option.

```ini
[default]
org_id = org-OPENAI_OR_GID
api_key = sk-OPENAI_API_KEY
```

## Authors

- Written by GPT-4.
- Prompt engineering by Eric Hammond.
- Some code Copyright (c) 2023 OpenAI

## License

This project is licensed under the terms of the MIT license.
