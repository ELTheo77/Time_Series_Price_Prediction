"""
Script to demonstrate all visualization capabilities for both price prediction
and contract pricing analysis.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from src.models.predictor import GasPricePredictor
from src.models.contract_pricer import StorageContractPricer
from src.visualization.plots import *

def view_price_predictions():
    """View price prediction visualizations."""
    print("\n=== Price Prediction Analysis ===")
    
    # Load data and create predictions
    predictor = GasPricePredictor('data/raw/Nat_Gas.csv')
    df = pd.read_csv('data/raw/Nat_Gas.csv')
    df['Dates'] = pd.to_datetime(df['Dates'], format='%m/%d/%y')
    df.set_index('Dates', inplace=True)
    
    # Get predictions for all dates
    predictions = []
    for date in df.index:
        pred = predictor.predict(date.strftime('%Y-%m-%d'))
        predictions.append(pred)
    pred_series = pd.Series(predictions, index=df.index)
    
    print("\n1. Showing price history with trend...")
    plot_price_history(df)
    
    print("\n2. Showing seasonal patterns...")
    plot_seasonal_patterns(df)
    
    print("\n3. Showing predictions vs actual prices...")
    plot_prediction_vs_actual(df['Prices'], pred_series)
    
    print("\n4. Showing residuals analysis...")
    plot_residuals(df['Prices'], pred_series)
    
    print("\n5. Showing complete price analysis dashboard...")
    create_analysis_dashboard(df, df['Prices'], pred_series)

def view_contract_analysis():
    """View contract pricing visualizations."""
    print("\n=== Contract Analysis ===")
    
    # Initialize models
    predictor = GasPricePredictor('data/raw/Nat_Gas.csv')
    pricer = StorageContractPricer(predictor)
    
    # Example contract parameters
    injection_dates = ['2024-06-30', '2024-07-31']
    withdrawal_dates = ['2024-12-31', '2025-01-31']
    
    # Calculate contract value
    result = pricer.calculate_contract_value(
        injection_dates=injection_dates,
        withdrawal_dates=withdrawal_dates,
        volume_per_trade=1_000_000,
        injection_rate=50_000,
        withdrawal_rate=50_000,
        max_storage=2_000_000
    )
    
    print("\n1. Showing contract cost breakdown...")
    plot_contract_costs(result)
    
    print("\n2. Showing trade prices comparison...")
    plot_trade_prices(injection_dates, withdrawal_dates, result)
    
    print("\n3. Showing complete contract analysis dashboard...")
    create_contract_dashboard(injection_dates, withdrawal_dates, result)

def main():
    """Main function to view all visualizations."""
    while True:
        print("\nVisualization Options:")
        print("1. Price Prediction Analysis")
        print("2. Contract Analysis")
        print("3. All Visualizations")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            view_price_predictions()
        elif choice == '2':
            view_contract_analysis()
        elif choice == '3':
            view_price_predictions()
            view_contract_analysis()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()