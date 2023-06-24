#!/usr/bin/env python3
"""
NAME
    openai-chat - Command line utility for engaging with OpenAI models via the OpenAI API

SYNOPSIS
    openai-chat [OPTIONS]

DESCRIPTION
    This utility enables the generation of AI-based text completions
    given a series of messages, by interfacing with the OpenAI API and
    its available models. It does not facilitate a direct chat but
    provides the user with a means to generate conversation
    completions in a chat format. It's highly configurable through
    several command line options.

OPTIONS
    --config CONFIGFILE
        Path to the configuration file. Default is $OPENAI_CONFIG or
        $HOME/.openai.conf.

    --project PROJECT_NAME
        Name of the project configuration to use from the config file.
        Default is 'default'.

    --model MODEL_NAME
        OpenAI model to use. Default is 'gpt-4-0613'.

    --system SYSTEM_PROMPT
        System level prompt to set the behavior of the assistant.

    --system-file SYSTEM_PROMPT_FILE
        Path to a text file containing the system prompt.

    --user USER_PROMPT
        User level prompt for the assistant.

    --user-file USER_PROMPT_FILE
        Path to a text file containing the user prompt.

    --assistant ASSISTANT_PROMPT
        Assistant's responses.

    --assistant-file ASSISTANT_PROMPT_FILE
        Path to a text file containing the assistant's responses.

    --temperature TEMPERATURE_VALUE
        Temperature for the GPT model. A higher value produces more random
        outputs.

    --top-p-sampling P_SAMPLING_VALUE
        Top p value for nucleus sampling. A lower value produces more focused
        outputs.

    --frequency-penalty FREQUENCY_PENALTY_VALUE
        Frequency penalty for the GPT model. A higher value reduces the chance
        of frequent tokens appearing.

    --presence-penalty PRESENCE_PENALTY_VALUE
        Presence penalty for the GPT model. A higher value reduces the chance
        of new tokens appearing.

    --list-models
        List all models owned by OpenAI that start with "gpt-".

    --debug
        Provide detailed information about the interaction.

CONFIGURATION
    This program reads project configurations from a file specified
    with the --config option. The configuration file should be in the
    INI file format, with one section for each OpenAI project. Each
    project section should include 'org_id' and 'api_key' parameters
    for the OpenAI organization ID and API key, respectively.

    The program will attempt to read from the file at ~/.openai.conf
    by default.  If the OPENAI_CONFIG environment variable is set, the
    program will use its value as the path to the configuration
    file. However, the --config option will override both the default
    and the environment variable.

    Example configuration file:
    [MyProject]
    org_id = org-OPENAI_OR_GID
    api_key = sk-OPENAI_API_KEY

EXAMPLES
    To run the program with default settings:
    $ openai-chat

    To specify a custom configuration file:
    $ openai-chat --config /path/to/configfile

    To use a specific model:
    $ openai-chat --model gpt-4-0613

AUTHORS
    Written by GPT-4.
    Prompt engineering by Eric Hammond.
    Some code Copyright (c) 2023 OpenAI

SEE ALSO

VERSION
    2023-06-21

EXAMPLES
    To initiate a response with the default project:

    $ openai-chat --user "Why is the sky blue?"

    To specify a project, model, and system and user prompts:

    $ openai-chat --project comedy-tool --model gpt-4 --temperature 1.0 --system "You are a famous standup comedian (not an AI) performing on stage interacting with the audience." --user "Why is the sky blue?"

    To list all available models:

    $ openai-chat --list-models
"""

# Import necessary libraries
import argparse
import configparser
import os
import sys
import signal
import openai
import json

# Define constants
DEFAULT_CONFIG_FILE = '~/.openai.conf'

# Define signal handling function
def signal_handler(signal, frame):
    print('\nProgram exited gracefully')
    sys.exit(0)

# Custom argparse action to handle message-related arguments
class MessageAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # Check if the list for messages exists in the namespace
        if 'messages' not in namespace:
            setattr(namespace, 'messages', [])

        # Infer role from the option string
        role = option_string.split('-')[2]

        # Handle file arguments
        if "file" in option_string:
            try:
                with open(values, 'r') as file:
                    values = file.read().strip()
            except FileNotFoundError:
                parser.error(f"The file {values} does not exist.")
            except IOError:
                parser.error(f"IO error occurred while trying to read the file {values}.")

        # Get the list, append the new message, and reset the list
        messages = namespace.messages
        messages.append({"role": role, "content": values})
        setattr(namespace, 'messages', messages)

# Create argument parser function
def create_argument_parser():
    """Create an argument parser for command-line arguments."""
    parser = argparse.ArgumentParser(description='Generate a chat-based response using the OpenAI API.')
    parser.add_argument('--config', type=str, help='Path to the configuration file.')
    parser.add_argument('--project', type=str, default='default', help='Name of the project configuration to use from the config file.')
    parser.add_argument('--model', type=str, default='gpt-4-0613', help='OpenAI model to use.')
    parser.add_argument('--system', type=str, action=MessageAction, help='System level prompt to set the behavior of the assistant.')
    parser.add_argument('--system-file', type=str, action=MessageAction, help='Path to a text file containing the system prompt.')
    parser.add_argument('--user', type=str, action=MessageAction, help='User level prompt for the assistant.')
    parser.add_argument('--user-file', type=str, action=MessageAction, help='Path to a text file containing the user prompt.')
    parser.add_argument('--assistant', type=str, action=MessageAction, help="Assistant's responses.")
    parser.add_argument('--assistant-file', type=str, action=MessageAction, help="Path to a text file containing the assistant's responses.")
    parser.add_argument('--temperature', type=float, default=0.5, help='Temperature for the GPT model. A higher value produces more random outputs.')
    parser.add_argument('--top-p-sampling', type=float, default=None, help='Top p value for nucleus sampling. A lower value produces more focused outputs.')
    parser.add_argument('--frequency-penalty', type=float, default=None, help='Frequency penalty for the GPT model. A higher value reduces the chance of frequent tokens appearing.')
    parser.add_argument('--presence-penalty', type=float, default=None, help='Presence penalty for the GPT model. A higher value reduces the chance of new tokens appearing.')
    parser.add_argument('--list-models', action='store_true', help='List all models owned by OpenAI that start with "gpt-".')
    parser.add_argument('--debug', action='store_true', help='Provide detailed information about the interaction.')
    return parser

# Function to read configuration file
def read_configuration(config_file, project):
    """Read the configuration file and return the project configuration."""
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(config_file))
    return config[project]

# Function to use OpenAI API
def use_openai_api(api_key, model, messages, temperature, top_p, frequency_penalty, presence_penalty, debug):
    """Use the OpenAI API to generate a chat-based response."""
    openai.api_key = api_key
    
    # Construct API parameters dictionary
    api_params = {
        'model': model,
        'messages': messages,
        'temperature': temperature,
        'top_p': top_p,
        'frequency_penalty': frequency_penalty,
        'presence_penalty': presence_penalty
    }

    # Remove None values using dictionary comprehension
    api_params = {k: v for k, v in api_params.items() if v is not None}

    # Print the request if debug mode is enabled
    if debug:
        print("Sending the following request to the OpenAI API:")
        print(json.dumps(api_params, indent=4))

    response = openai.ChatCompletion.create(**api_params)
    return response

# Function to list models
def list_models(api_key):
    """Lists all models owned by OpenAI that start with 'gpt-'."""
    openai.api_key = api_key
    models = openai.Model.list()
    gpt_models = [model.id for model in models.data if model.owned_by == 'openai' and model.id.startswith('gpt-')]
    for model in gpt_models:
        print(model)

# Main function
def main():
    """Main program function."""
    # Register the signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse command-line arguments
    parser = create_argument_parser()
    args = parser.parse_args()

    # Load configuration
    config_file = args.config if args.config else os.getenv('OPENAI_CONFIG', DEFAULT_CONFIG_FILE)
    project_config = read_configuration(config_file, args.project)

    # If --list-models option was used
    if args.list_models:
        list_models(project_config['api_key'])
        return

    # Check if at least one of the required arguments is provided
    if not args.messages:
        parser.error('At least one of --system, --system-file, --user, --user-file, --assistant, --assistant-file is required')

    # Use OpenAI API
    response = use_openai_api(project_config['api_key'], args.model, args.messages, args.temperature, args.top_p_sampling, args.frequency_penalty, args.presence_penalty, args.debug)

    # Print the assistant's response
    if args.debug:
        print(json.dumps(response, indent=4))
    else:
        print(response.choices[0].message['content'])

# Execute main function
if __name__ == "__main__":
    main()
