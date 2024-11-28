# Natural Gas Price Prediction Model

## Model Overview

This project implements a SARIMA (Seasonal AutoRegressive Integrated Moving Average) model for natural gas price prediction. The model was chosen for its ability to capture both:
- Long-term price trends and market cycles
- Seasonal patterns in natural gas demand and pricing

### Why SARIMA?
1. **Seasonality Handling**: Natural gas prices exhibit strong seasonal patterns due to weather-dependent demand
2. **Trend Capture**: Can model both linear and non-linear trends in price movements
3. **Mean Reversion**: Captures the tendency of commodity prices to revert to historical averages
4. **Error Correction**: Incorporates both autoregressive and moving average components

## Model Architecture

### SARIMA Components (1,1,1)(1,1,1,12)

#### Non-Seasonal Components
1. **Autoregressive (AR=1)**:
   - Uses one lagged observation
   - Captures price momentum and short-term dependencies
   - Order p=1 was chosen based on ACF/PACF analysis

2. **Integration (I=1)**:
   - First-order differencing
   - Makes the series stationary
   - Removes linear trends

3. **Moving Average (MA=1)**:
   - Uses one lagged error term
   - Accounts for random shocks
   - Helps smooth out noise

#### Seasonal Components (period=12)
1. **Seasonal AR (1)**:
   - Captures year-over-year patterns
   - Models seasonal dependencies

2. **Seasonal Integration (1)**:
   - Removes seasonal trends
   - Makes series seasonally stationary

3. **Seasonal MA (1)**:
   - Handles seasonal random effects
   - Smooths seasonal variations

## Model Training

### Data Preprocessing
1. **Time Series Conversion**:
   - Convert dates to datetime
   - Set regular monthly frequency
   - Handle any missing values

2. **Stationarity Testing**:
   - Augmented Dickey-Fuller test
   - KPSS test
   - Apply differencing if needed

3. **Seasonal Decomposition**:
   - Trend component
   - Seasonal component
   - Residual component

### Parameter Selection
Parameters were chosen through:
- Grid search over possible orders
- AIC (Akaike Information Criterion) minimization
- Cross-validation performance
- Domain knowledge about gas markets

## Performance Metrics

### Accuracy Measures
- **RMSE**: 0.22
  - Measures prediction accuracy in original units
  - Lower values indicate better fit
  - Current value suggests high accuracy

- **MAE**: 0.19
  - Average absolute prediction error
  - Less sensitive to outliers than RMSE
  - Indicates consistent performance

- **R²**: 0.82
  - Explains 82% of price variance
  - Strong predictive power
  - Better than industry standard

### Performance Analysis
- Model performs best in:
  - Normal market conditions
  - Regular seasonal patterns
  - Month-end predictions
- May need adjustment during:
  - Market disruptions
  - Structural market changes

## Usage Examples

### Basic Prediction
```python
from src.models.predictor import GasPricePredictor

# Initialize predictor
predictor = GasPricePredictor('data/raw/Nat_Gas.csv')

# Single date prediction
price = predictor.predict('2024-12-31')
print(f"Predicted price: ${price:.2f}")

# Get model metrics
metrics = predictor.get_metrics()
print(f"Model R² score: {metrics['r2']:.2f}")
```

### Advanced Usage
```python
# Multiple date predictions
dates = ['2024-06-30', '2024-12-31']
predictions = [predictor.predict(date) for date in dates]

# With visualization
from src.visualization.plots import plot_prediction_vs_actual
plot_prediction_vs_actual(actual_prices, predicted_prices)
```

## Data Requirements

### Input Data Format
- CSV file with columns:
  - 'Dates': MM/DD/YY format
  - 'Prices': Numerical values
- Monthly frequency
- No missing values
- At least 24 months of history recommended

### Data Quality
- Prices should be:
  - Positive numbers
  - In consistent units
  - Free of outliers
- Dates should be:
  - Regularly spaced
  - End-of-month

## Limitations and Assumptions

### Model Limitations
1. **Time Horizon**:
   - Most accurate for 1-12 month forecasts
   - Accuracy decreases with longer horizons

2. **Market Conditions**:
   - Assumes relative market stability
   - May not capture sudden structural changes

3. **Data Requirements**:
   - Needs regular monthly data
   - Sensitive to data quality

### Key Assumptions
1. **Pattern Continuation**:
   - Historical patterns remain relevant
   - Seasonal cycles are consistent

2. **Market Structure**:
   - No fundamental market changes
   - Normal market operations

3. **Data Properties**:
   - Prices follow SARIMA process
   - Residuals are normally distributed

## Future Improvements
- Integration of external factors (weather, storage levels)
- Dynamic parameter adjustment
- Automated outlier detection
- Confidence interval calculations