from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

# 'confluence_scraper' is a local module, not an external package

setup(
    name="scrapemd",
    version="0.1.5",
    author="Your Name",
    author_email="your.email@example.com",
    description="Web scraper that converts web pages to markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/scraper",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "scrapemd=cli:main_cli",
        ],
    },
)
