from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="twincat-dev-tools",
    version="0.1.0",
    author="Kenny Coleman",
    author_email="kennycoleman72@gmail.com",
    description="A framework for programming Beckhoff PLCs without TwinCAT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anchormang/twincat-dev-tools",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyads>=3.0.0",
        # Add other dependencies here
    ],
    extras_require={
        "dev": ["pytest>=3.7", "check-manifest"],
        "test": ["coverage"],
    },
    entry_points={
        "console_scripts": [
            "twincat-dev-tools=twincat_dev_tools.main:main",
        ],
    },
)
