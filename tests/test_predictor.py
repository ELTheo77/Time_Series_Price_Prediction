import pytest
import pandas as pd
from src.models.predictor import GasPricePredictor

@pytest.fixture
def predictor():
    #Create a predictor instance using available natural gas price data.
    return GasPricePredictor('data/raw/Nat_Gas.csv')

def test_model_initialization(predictor):
    #Test basic model initialization and data loading.
    assert predictor is not None
    assert predictor.model is not None
    assert predictor.df is not None
    assert 'Prices' in predictor.df.columns
    assert len(predictor.df) > 0

def test_model_performance(predictor):
    #Test if model meets high performance standards.
    metrics = predictor.get_metrics()
    assert metrics['rmse'] < 0.25  # Baseline was 0.22
    assert metrics['mae'] < 0.20   # Baseline was 0.19
    assert metrics['r2'] > 0.80    # Baseline was 0.82

def test_prediction_month_end(predictor):
    #Test prediction for a known month-end date.
    prediction = predictor.predict('2022-06-30')
    assert isinstance(prediction, float)
    assert 9.5 < prediction < 13.5  # Based on historical price ranges

def test_future_prediction(predictor):
    #Test future date prediction.
    prediction = predictor.predict('2024-12-31')
    assert isinstance(prediction, float)
    # Future predictions should still be within reasonable bounds
    assert 9.5 < prediction < 13.5  # Based on historical ranges