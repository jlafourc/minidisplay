"""
Setup script for Mini Display Family Information System.

This script provides a standard installation method for the project,
including the data source abstraction layer and all dependencies.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mini-display-family-info",
    version="1.0.0",
    author="Mini Display Project Team",
    author_email="contact@minidisplay.com",
    description="Family information display system for Raspberry Pi with e-ink display",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minidisplay/mini-display-family-info",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware",
        "Topic :: Multimedia :: Graphics :: Display",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-mock>=3.6.0",
            "pytest-cov>=2.10.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
            "mypy>=0.800",
        ],
        "test": [
            "pytest>=6.0.0",
            "pytest-mock>=3.6.0",
            "pytest-cov>=2.10.0",
        ],
    },
    entry_points={"console_scripts": ["mini-display=minidisplay.cli:main"]},
    include_package_data=True,
    package_data={"minidisplay": ["config/*.json", "resources/*.png"]},
)
