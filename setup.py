#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="attendance-generator",
    version="1.0.0",
    author="BIGD Research Team",
    author_email="research@bigd.bracu.ac.bd",
    description="Automated attendance & travelling bill .docx generator for field surveys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sabbirhossain780/attendance-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.9",
    install_requires=[
        "python-docx>=1.1.0",
        "openpyxl>=3.1.0",
        "pandas>=2.0.0",
        "lxml>=5.0.0",
    ],
    extras_require={
        "notebook": [
            "ipywidgets>=7.0",
            "jupyter>=1.0",
        ],
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "ipywidgets>=7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "attendance-gen=attendance_generator.cli:main",
        ],
    },
)
