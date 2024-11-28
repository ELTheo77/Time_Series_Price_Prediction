# API Reference

## Price Prediction

### `GasPricePredictor`

Main class for predicting natural gas prices.

#### Methods

##### `__init__(data_path: str)`
Initialize the predictor with historical data.
- **Parameters:**
  - data_path (str): Path to CSV file containing price data

##### `predict(target_date: str) -> float`
Predict the natural gas price for a given date.
- **Parameters:**
  - target_date (str): Date in YYYY-MM-DD format
- **Returns:**
  - float: Predicted price

##### `get_metrics() -> dict`
Get model performance metrics.
- **Returns:**
  - dict: Dictionary containing RMSE, MAE, and R² scores

## Contract Pricing

### `StorageContractPricer`

Class for pricing natural gas storage contracts.

#### Methods

##### `__init__(price_predictor: GasPricePredictor)`
Initialize contract pricer.
- **Parameters:**
  - price_predictor: Instance of GasPricePredictor

##### `calculate_contract_value(...) -> dict`
Calculate the value of a storage contract.
- **Parameters:**
  - injection_dates (List[str]): Dates for gas injection
  - withdrawal_dates (List[str]): Dates for gas withdrawal
  - volume_per_trade (float): Volume in MMBtu
  - injection_rate (float): MMBtu per day
  - withdrawal_rate (float): MMBtu per day
  - max_storage (float): Maximum storage capacity
  - storage_cost_monthly (float, optional): Monthly storage cost
  - injection_cost (float, optional): Cost per million MMBtu
  - withdrawal_cost (float, optional): Cost per million MMBtu
  - transport_cost (float, optional): Cost per transport
- **Returns:**
  - dict: Contract value and cost breakdown

## Visualization

### Plot Functions

##### `plot_price_history(df: pd.DataFrame, title: str = "Natural Gas Price History", save_path: Optional[str] = None)`
Plot historical price data with trend line.

##### `plot_seasonal_patterns(df: pd.DataFrame, save_path: Optional[str] = None)`
Plot monthly price patterns.

##### `plot_prediction_vs_actual(actual: pd.Series, predicted: pd.Series, title: str = "Predicted vs Actual Prices", save_path: Optional[str] = None)`
Compare predicted prices against actual prices.

##### `plot_contract_costs(contract_details: Dict, save_path: Optional[str] = None)`
Visualize contract cost breakdown.

##### `create_analysis_dashboard(df: pd.DataFrame, actual: pd.Series, predicted: pd.Series, save_path: Optional[str] = None)`
Create comprehensive price analysis dashboard.