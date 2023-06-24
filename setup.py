from setuptools import setup, find_packages

setup(
    name="openai-misc-tools",
    version="0.1.5",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "openai-chat = openai_misc_tools.openai_chat:main",
            "openai-tokens-count = openai_misc_tools.openai_tokens_count:main",
            "openai-tokens-head = openai_misc_tools.openai_tokens_head:main",
            "openai-transcribe = openai_misc_tools.openai_transcribe:main",
        ]
    },
    install_requires=[
        "configparser",
        "moviepy",
        "openai",
        "pydub",
        "tiktoken",
    ],
)
