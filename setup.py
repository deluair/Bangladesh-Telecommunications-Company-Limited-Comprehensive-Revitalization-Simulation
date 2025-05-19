"""
Setup script for BTCL simulation package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="btcl-simulation",
    version="0.1.0",
    author="BTCL Simulation Team",
    author_email="team@btcl-simulation.com",
    description="A comprehensive revitalization simulation for Bangladesh Telecommunications Company Limited",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/btcl-simulation/btcl-simulation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.5b2",
            "flake8>=3.9.0",
        ],
    },
) 