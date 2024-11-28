import pytest
import pandas as pd
from src.data.data_loader import load_gas_prices, split_train_test

def test_load_gas_prices():
    #Test data loading function.
    df = load_gas_prices('data/raw/Nat_Gas.csv')
    assert isinstance(df, pd.DataFrame)
    assert 'Prices' in df.columns
    assert df.index.name == 'Dates'
    assert not df.empty

def test_split_train_test():
    #Test train-test splitting functionality.
    # Create sample data
    df = pd.DataFrame({
        'Dates': pd.date_range(start='2020-01-01', end='2023-12-31', freq='ME'),
        'Prices': range(48)
    }).set_index('Dates')
    
    # Test splitting
    train, test = split_train_test(df, train_size=0.8)
    assert len(train) == int(len(df) * 0.8)
    assert len(test) == len(df) - len(train)
    
    # Test data continuity
    assert train.index.max() < test.index.min()