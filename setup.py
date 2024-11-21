from setuptools import setup, find_packages

setup(
    name="aider-extension",
    version="0.1.0",
    description="Custom extensions for aider",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "aider-chat",
    ],
    entry_points={
        "console_scripts": [
            "aider-custom=custom_aider.custom_aider_main:custom_main",
        ],
    },
)