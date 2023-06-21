from setuptools import setup, find_packages

setup(
    name="openai-tokens",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "openai-tokens-count = openai_tokens.openai_tokens_count:main",
            "openai-tokens-head = openai_tokens.openai_tokens_head:main",
        ]
    },
    install_requires=[
        "tiktoken",
    ],
)
