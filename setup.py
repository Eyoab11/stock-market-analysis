from setuptools import setup, find_packages

setup(
    name="financial_news",  # The distribution name, and the import name
    version="0.1.0",
    # Replace the original 'packages' and 'package_dir' lines
    # packages=find_packages(where="src"),  # Remove this line
    # package_dir={"": "src"},             # Remove this line
    packages=['financial_news'],  # Explicitly list your top-level package name
    package_dir={'financial_news': 'src'}, # Map the package name to the 'src' directory
                                         # This means 'financial_news' package content is in 'src/'
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "nltk>=3.6.0",
        "textblob>=0.15.3",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "TA-Lib>=0.4.24", # Note: TA-Lib can be tricky to install. Ensure it's properly set up.
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