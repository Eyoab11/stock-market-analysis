from setuptools import setup, find_packages

setup(
    name="financial_news",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "nltk>=3.6.0",
        "textblob>=0.15.3",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "TA-Lib>=0.4.24",
        "python-dateutil>=2.8.2"
    ],
    python_requires=">=3.9",
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "pylint>=2.11.1",
            "black>=21.8b0",
            "ipykernel>=6.4.1",
            "jupyter>=1.0.0"
        ]
    },
)