from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pymangodb",
    version="0.1.1",
    author="Gabor Racz",
    author_email="orfeous@olab.app",
    description="A lightweight, dependency-free document database for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orfeous/mangodb",
    project_urls={
        "Bug Tracker": "https://github.com/orfeous/mangodb/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="database, json, document-store, mongodb-alternative",
)
