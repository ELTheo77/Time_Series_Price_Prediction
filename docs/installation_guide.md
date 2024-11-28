# Installation Guide

## Prerequisites

### Required Software
- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

### System Requirements
- Operating System: Windows 10/11, macOS 10.15+, or Linux
- Minimum RAM: 4GB (8GB recommended)
- Disk Space: At least 1GB free space

## Step-by-Step Installation

### 1. Python Installation
If not already installed:
1. Download Python from [python.org](https://python.org)
2. During installation, ensure to:
   - Check "Add Python to PATH"
   - Install pip package manager

### 2. Clone the Repository
```bash
git clone https://github.com/eltheo77/time_series_price_prediction.git
cd time_series_price_prediction
```

### 3. Virtual Environment Setup
Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Unix/MacOS
python -m venv venv
source venv/bin/activate
```

You should see (venv) in your command prompt after activation.

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- pandas>=1.3.0: Data manipulation
- numpy>=1.21.0: Numerical computations
- scikit-learn>=0.24.2: Machine learning utilities
- statsmodels>=0.13.0: Time series analysis
- matplotlib>=3.4.0: Plotting
- seaborn>=0.11.0: Statistical visualization

### 5. Data Setup
1. Create the data directory structure:
```bash
mkdir -p data/raw data/processed
```

2. Place your Nat_Gas.csv file in the data/raw directory

### 6. Verify Installation
```python
from src.models.predictor import GasPricePredictor
predictor = GasPricePredictor('data/raw/Nat_Gas.csv')
```

## Troubleshooting

### Common Issues

#### 1. Missing Dependencies
**Issue:** Import errors or missing modules
**Solutions:**
- Run `pip install -r requirements.txt` again
- Check Python version: `python --version`
- Verify pip installation: `pip --version`
- Try installing packages individually:
  ```bash
  pip install pandas numpy scikit-learn statsmodels matplotlib seaborn
  ```

#### 2. Import Errors
**Issue:** Cannot import project modules
**Solutions:**
- Ensure you're in the project root directory
- Verify virtual environment is activated
- Check directory structure matches project layout

#### 3. Data File Issues
**Issue:** FileNotFoundError or data loading errors
**Solutions:**
- Verify Nat_Gas.csv exists in data/raw/ directory
- Check file permissions:
  ```bash
  # Unix/MacOS
  ls -l data/raw/Nat_Gas.csv
  # Windows
  dir data\raw\Nat_Gas.csv
  ```
- Ensure CSV format is correct:
  - Headers: "Dates,Prices"
  - Date format: MM/DD/YY
  - No missing values