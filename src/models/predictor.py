import pandas as pd
import numpy as np
from datetime import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GasPricePredictor:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.model = None
        self.df = None
        self.metrics = {}
        
        try:
            self._load_data()
            self._train_model()
        except Exception as e:
            logger.error(f"Failed to initialize predictor: {str(e)}")
            raise

    def _load_data(self):
        try:
            self.df = pd.read_csv(self.data_path)
            self.df['Dates'] = pd.to_datetime(self.df['Dates'])
            self.df.set_index('Dates', inplace=True)
            self.df.sort_index(inplace=True)
            logger.info(f"Successfully loaded data from {self.data_path}")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def _train_model(self):
        try:
            # Split data with 80-20 ratio
            train_size = int(len(self.df) * 0.8)
            train_data = self.df[:train_size]
            test_data = self.df[train_size:]

            # Original, proven parameters
            self.model = SARIMAX(
                train_data['Prices'],
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 12)
            )
            
            # Simple fit without extra parameters
            self.model = self.model.fit(disp=False)
            
            # Get predictions for test data
            predictions = self.model.get_prediction(
                start=test_data.index[0],
                end=test_data.index[-1]
            ).predicted_mean
            
            # Calculate metrics
            self.metrics = {
                'rmse': np.sqrt(mean_squared_error(test_data['Prices'], predictions)),
                'mae': mean_absolute_error(test_data['Prices'], predictions),
                'r2': r2_score(test_data['Prices'], predictions)
            }
            
            logger.info("Model successfully trained")
            logger.info(f"Model performance metrics: {self.metrics}")
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise

    def predict(self, target_date: str) -> float:
        try:
            date = pd.to_datetime(target_date)
            
            if date > self.df.index[-1]:
                # Future prediction
                steps = ((date.year - self.df.index[-1].year) * 12 + 
                        date.month - self.df.index[-1].month)
                forecast = self.model.forecast(steps=steps)
                return float(forecast.iloc[-1])
            else:
                # Historical prediction
                return float(self.model.get_prediction(start=date, end=date).predicted_mean[0])
                
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise

    def get_metrics(self):
        return self.metrics

def main():
    predictor = GasPricePredictor('data/raw/Nat_Gas.csv')
    
    print("\nModel Performance Metrics:")
    metrics = predictor.get_metrics()
    print(f"Root Mean Square Error: {metrics['rmse']:.2f}")
    print(f"Mean Absolute Error: {metrics['mae']:.2f}")
    print(f"R-squared Score: {metrics['r2']:.2f}\n")
    
    while True:
        print("\nEnter date (YYYY-MM-DD) or 'quit' to exit:")
        user_input = input().strip()
        
        if user_input.lower() == 'quit':
            break
            
        try:
            price = predictor.predict(user_input)
            print(f"{price:.2f}")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()