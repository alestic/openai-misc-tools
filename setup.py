from setuptools import setup, find_packages

setup(
    name="openai-tokens",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "openai-token-count = openai_tokens.openai_token_count:main",
            "openai-token-head = openai_tokens.openai_token_head:main",
        ]
    },
    install_requires=[
        "tiktoken",
    ],
)
