from setuptools import setup, find_packages

setup(
    name="time_series_price_prediction",
    version="1.0.0",
    author="eltheo77",
    description="A time series analysis tool for predicting natural gas prices using SARIMA modeling",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/eltheo77/time_series_price_prediction",
    packages=find_packages(),
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.21.0',
        'scikit-learn>=0.24.2',
        'statsmodels>=0.13.0',
        'matplotlib>=3.4.0',
        'seaborn>=0.11.0',
        'jupyter>=1.0.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)