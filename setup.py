"""
Backward-compatible setup.py for older pip versions
"""
from setuptools import setup, find_packages

# For backwards compatibility with older pip versions
setup(
    name="gosset",
    packages=find_packages(),
    python_requires=">=3.8",
)

