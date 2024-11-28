import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Optional, Tuple, Dict
import numpy as np

def set_style():
    sns.set_theme()
    sns.set_context("notebook", font_scale=1.2)
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 12

def plot_price_history(df: pd.DataFrame, title: str = "Natural Gas Price History", save_path: Optional[str] = None) -> None:
    set_style()
    
    fig, ax = plt.subplots()
    
    # Plot actual prices
    ax.plot(df.index, df['Prices'], label='Actual Prices', color='blue')
    
    # Add trend line
    z = np.polyfit(range(len(df)), df['Prices'], 1)
    p = np.poly1d(z)
    ax.plot(df.index, p(range(len(df))), 
            linestyle='--', color='red', label='Trend Line')
    
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_seasonal_patterns(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    set_style()
    
    df['Month'] = df.index.month
    monthly_avg = df.groupby('Month')['Prices'].mean()
    
    fig, ax = plt.subplots()
    monthly_avg.plot(kind='bar', ax=ax)
    
    ax.set_title('Average Price by Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Price')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_prediction_vs_actual(actual: pd.Series, predicted: pd.Series, title: str = "Predicted vs Actual Prices", save_path: Optional[str] = None) -> None:
    set_style()
    
    fig, ax = plt.subplots()
    
    ax.plot(actual.index, actual, label='Actual', color='blue')
    ax.plot(predicted.index, predicted, label='Predicted', 
            color='red', linestyle='--')
    
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_residuals(actual: pd.Series, predicted: pd.Series, save_path: Optional[str] = None) -> None:
    set_style()
    
    residuals = actual - predicted
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Residuals over time
    ax1.plot(actual.index, residuals, 'o-')
    ax1.axhline(y=0, color='r', linestyle='--')
    ax1.set_title('Residuals Over Time')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Residual')
    
    # Residuals distribution
    sns.histplot(residuals, kde=True, ax=ax2)
    ax2.set_title('Residuals Distribution')
    ax2.set_xlabel('Residual')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def create_analysis_dashboard(df: pd.DataFrame, actual: pd.Series, predicted: pd.Series, save_path: Optional[str] = None) -> None:
    set_style()
    
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2)
    
    # Price history and predictions
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(actual.index, actual, label='Actual', color='blue')
    ax1.plot(predicted.index, predicted, label='Predicted', color='red', linestyle='--')
    ax1.set_title('Price History and Predictions')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.legend()
    
    # Seasonal patterns
    ax2 = fig.add_subplot(gs[1, 0])
    df['Month'] = df.index.month
    monthly_avg = df.groupby('Month')['Prices'].mean()
    monthly_avg.plot(kind='bar', ax=ax2)
    ax2.set_title('Seasonal Patterns')
    
    # Residuals distribution
    ax3 = fig.add_subplot(gs[1, 1])
    residuals = actual - predicted
    sns.histplot(residuals, kde=True, ax=ax3)
    ax3.set_title('Residuals Distribution')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_contract_costs(contract_details: Dict, save_path: Optional[str] = None) -> None:
    set_style()
    
    # Extract costs
    costs = {k: v for k, v in contract_details['details'].items() 
            if k not in ['purchase_prices', 'sale_prices', 'gross_profit']}
    
    # Create bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(costs.keys(), costs.values())
    plt.title('Contract Cost Breakdown')
    plt.xticks(rotation=45)
    plt.ylabel('Cost ($)')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_trade_prices(injection_dates: list, withdrawal_dates: list, contract_details: Dict, save_path: Optional[str] = None) -> None:
    set_style()
    
    purchases = contract_details['details']['purchase_prices']
    sales = contract_details['details']['sale_prices']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    trades = range(len(injection_dates))
    
    width = 0.35
    ax.bar([i - width/2 for i in trades], purchases, width, label='Purchase Price')
    ax.bar([i + width/2 for i in trades], sales, width, label='Sale Price')
    
    plt.title('Purchase vs Sale Prices by Trade')
    plt.xlabel('Trade Number')
    plt.ylabel('Price')
    plt.legend()
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

def create_contract_dashboard(injection_dates: list, withdrawal_dates: list, contract_details: Dict, save_path: Optional[str] = None) -> None:
    set_style()
    
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2)
    
    # Trade prices
    ax1 = fig.add_subplot(gs[0, 0])
    purchases = contract_details['details']['purchase_prices']
    sales = contract_details['details']['sale_prices']
    width = 0.35
    trades = range(len(injection_dates))
    ax1.bar([i - width/2 for i in trades], purchases, width, label='Purchase')
    ax1.bar([i + width/2 for i in trades], sales, width, label='Sale')
    ax1.set_title('Trade Prices')
    ax1.legend()
    
    # Cost breakdown
    ax2 = fig.add_subplot(gs[0, 1])
    costs = {k: v for k, v in contract_details['details'].items() 
            if k not in ['purchase_prices', 'sale_prices', 'gross_profit']}
    ax2.bar(costs.keys(), costs.values())
    ax2.set_title('Cost Breakdown')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    # Profit waterfall
    ax3 = fig.add_subplot(gs[1, :])
    components = ['Gross Profit'] + list(costs.keys()) + ['Net Value']
    values = [contract_details['details']['gross_profit']] + \
            list(-np.array(list(costs.values()))) + \
            [contract_details['contract_value']]
    ax3.bar(components, values)
    ax3.set_title('Profit Waterfall')
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()