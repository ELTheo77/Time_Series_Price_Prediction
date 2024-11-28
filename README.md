# Natural Gas Price Predictor

A time series analysis tool for predicting natural gas prices using SARIMA (Seasonal AutoRegressive Integrated Moving Average) modeling. This project provides price predictions based on historical data, incorporating both seasonal patterns and long-term trends for practical application in commodity trading and risk management.

## Features

### Price Prediction
- Time series forecasting using SARIMA models
- Handles both historical and future date predictions
- Robust handling of seasonal patterns and trends
- High accuracy with R² > 0.80 on test data

### Visualization
- Interactive price trend analysis
- Seasonal pattern visualization
- Prediction vs. actual comparisons
- Residual analysis plots

## Installation

1. Clone the repository:
```bash
git clone https://github.com/eltheo77/time_series_price_prediction.git
cd time_series_price_prediction
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Unix/MacOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage
```python
from src.models.predictor import GasPricePredictor

# Initialize predictor
predictor = GasPricePredictor('data/raw/Nat_Gas.csv')

# Get prediction for specific date
price = predictor.predict('2024-12-31')
print(f"Predicted price: ${price:.2f}")
```

### Visualization
```python
# Run the visualization tool
python view_plots.py
```

### Command Line Interface
```bash
# Run the interactive prediction tool
python -m src.models.predictor
```

## Model Performance

The current model achieves the following metrics on test data:
- Root Mean Square Error (RMSE): 0.22
- Mean Absolute Error (MAE): 0.19
- R-squared Score: 0.82

## Project Structure
```
time_series_price_prediction/
├── data/              # Data storage
│   ├── processed/     # Processed data files
│   └── raw/           # Raw input data
├── docs/              # Documentation
├── notebooks/         # Jupyter notebooks
├── src/               # Source code
│   ├── data/          # Data loading utilities
│   ├── models/        # Prediction models
│   └── visualization/ # Plotting utilities
└── tests/             # Comprehensive test suite
```

## Documentation

Detailed documentation is available in the [docs](docs/) directory:
- API Reference: Complete function and class documentation
- Model Explanation: Technical details of the SARIMA implementation
- Usage Examples: Comprehensive usage scenarios

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Add tests for new features
- Update documentation as needed

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

## Acknowledgments

- Data provided by JPMorgan Chase x Forage
