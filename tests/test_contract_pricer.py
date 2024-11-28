import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pandas as pd
from src.models.contract_pricer import StorageContractPricer
from src.models.predictor import GasPricePredictor

@pytest.fixture
def pricer():
    #Create a contract pricer instance for testing.
    predictor = GasPricePredictor('data/raw/Nat_Gas.csv')
    return StorageContractPricer(predictor)

def test_basic_valuation(pricer):
    #Test basic contract valuation functionality.
    result = pricer.calculate_contract_value(
        injection_dates=['2024-06-30'],
        withdrawal_dates=['2024-12-31'],
        volume_per_trade=1_000_000,
        injection_rate=50_000,
        withdrawal_rate=50_000,
        max_storage=2_000_000
    )
    assert isinstance(result, dict)
    assert 'contract_value' in result
    assert 'details' in result
    assert len(result['details']['purchase_prices']) == 1
    assert len(result['details']['sale_prices']) == 1

def test_multiple_trades(pricer):
    #Test contract valuation with multiple injection/withdrawal pairs.
    result = pricer.calculate_contract_value(
        injection_dates=['2024-06-30', '2024-07-31'],
        withdrawal_dates=['2024-12-31', '2025-01-31'],
        volume_per_trade=500_000,
        injection_rate=50_000,
        withdrawal_rate=50_000,
        max_storage=2_000_000
    )
    assert len(result['details']['purchase_prices']) == 2
    assert len(result['details']['sale_prices']) == 2

def test_storage_capacity_validation(pricer):
    #Test validation of storage capacity limits.
    with pytest.raises(ValueError, match="Total volume exceeds maximum storage capacity"):
        pricer.calculate_contract_value(
            injection_dates=['2024-06-30'],
            withdrawal_dates=['2024-12-31'],
            volume_per_trade=3_000_000,  # Exceeds max_storage
            injection_rate=50_000,
            withdrawal_rate=50_000,
            max_storage=2_000_000
        )

def test_date_matching_validation(pricer):
    #Test validation of injection/withdrawal date pairs.
    with pytest.raises(ValueError, match="Number of injection and withdrawal dates must match"):
        pricer.calculate_contract_value(
            injection_dates=['2024-06-30'],
            withdrawal_dates=['2024-12-31', '2025-01-31'],
            volume_per_trade=1_000_000,
            injection_rate=50_000,
            withdrawal_rate=50_000,
            max_storage=2_000_000
        )

def test_cost_calculation(pricer):
    #Test that all costs are calculated correctly.
    result = pricer.calculate_contract_value(
        injection_dates=['2024-06-30'],
        withdrawal_dates=['2024-12-31'],
        volume_per_trade=1_000_000,
        injection_rate=50_000,
        withdrawal_rate=50_000,
        max_storage=2_000_000,
        storage_cost_monthly=100_000,
        injection_cost=10_000,
        withdrawal_cost=10_000,
        transport_cost=50_000
    )
    
    details = result['details']
    # Storage cost for 6 months
    assert details['storage_cost'] == 100_000 * 6
    # Injection and withdrawal costs for 1M MMBtu
    assert details['injection_cost'] == 10_000
    assert details['withdrawal_cost'] == 10_000
    # Transport cost both ways
    assert details['transport_cost'] == 50_000 * 2

def test_seasonal_price_patterns(pricer):
    #Test that winter withdrawal prices are typically higher than summer injection prices.
    result = pricer.calculate_contract_value(
        injection_dates=['2024-06-30'],  # Summer
        withdrawal_dates=['2024-12-31'],  # Winter
        volume_per_trade=1_000_000,
        injection_rate=50_000,
        withdrawal_rate=50_000,
        max_storage=2_000_000
    )
    
    winter_price = result['details']['sale_prices'][0]
    summer_price = result['details']['purchase_prices'][0]
    assert winter_price > summer_price, "Winter prices should be higher than summer prices"

def test_custom_costs(pricer):
    #Test contract valuation with custom cost parameters.
    result = pricer.calculate_contract_value(
        injection_dates=['2024-06-30'],
        withdrawal_dates=['2024-12-31'],
        volume_per_trade=1_000_000,
        injection_rate=50_000,
        withdrawal_rate=50_000,
        max_storage=2_000_000,
        storage_cost_monthly=200_000,      # Custom storage cost
        injection_cost=20_000,             # Custom injection cost
        withdrawal_cost=20_000,            # Custom withdrawal cost
        transport_cost=100_000             # Custom transport cost
    )
    
    details = result['details']
    assert details['storage_cost'] == 200_000 * 6
    assert details['injection_cost'] == 20_000
    assert details['withdrawal_cost'] == 20_000
    assert details['transport_cost'] == 100_000 * 2

def test_contract_value_components(pricer):
    #Test that contract value equals gross profit minus total costs.
    result = pricer.calculate_contract_value(
        injection_dates=['2024-06-30'],
        withdrawal_dates=['2024-12-31'],
        volume_per_trade=1_000_000,
        injection_rate=50_000,
        withdrawal_rate=50_000,
        max_storage=2_000_000
    )
    
    details = result['details']
    total_costs = (details['storage_cost'] + details['injection_cost'] + details['withdrawal_cost'] + details['transport_cost'])
    
    assert abs(result['contract_value'] - (details['gross_profit'] - total_costs)) < 0.01