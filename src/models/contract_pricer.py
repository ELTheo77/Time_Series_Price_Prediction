import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import List, Dict, Union
from datetime import datetime
import pandas as pd
from src.models.predictor import GasPricePredictor

class StorageContractPricer:
    def __init__(self, price_predictor: GasPricePredictor):
        #Initialize contract pricer with a price prediction model.
        self.predictor = price_predictor

    def calculate_contract_value(self, 
                                injection_dates: List[str],
                                withdrawal_dates: List[str],
                                volume_per_trade: float,  # in MMBtu
                                injection_rate: float,    # MMBtu per day
                                withdrawal_rate: float,   # MMBtu per day
                                max_storage: float,       # MMBtu
                                storage_cost_monthly: float = 100000,  # $ per month
                                injection_cost: float = 10000,         # $ per million MMBtu
                                withdrawal_cost: float = 10000,        # $ per million MMBtu
                                transport_cost: float = 50000          # $ per transport
                                ) -> Dict[str, Union[float, Dict]]:
        try:
            # Validate inputs
            if len(injection_dates) != len(withdrawal_dates):
                raise ValueError("Number of injection and withdrawal dates must match")
            
            total_volume = len(injection_dates) * volume_per_trade
            if total_volume > max_storage:
                raise ValueError("Total volume exceeds maximum storage capacity")

            # Calculate purchase and sale prices
            purchase_prices = []
            sale_prices = []
            for inj_date, with_date in zip(injection_dates, withdrawal_dates):
                purchase_prices.append(self.predictor.predict(inj_date))
                sale_prices.append(self.predictor.predict(with_date))

            # Calculate storage duration and costs
            total_storage_months = 0
            for inj_date, with_date in zip(injection_dates, withdrawal_dates):
                inj_dt = pd.to_datetime(inj_date)
                with_dt = pd.to_datetime(with_date)
                months = (with_dt.year - inj_dt.year) * 12 + with_dt.month - inj_dt.month
                total_storage_months += max(months, 1)  # Minimum 1 month

            # Calculate each component
            gross_profit = sum((sale - purchase) * volume_per_trade for sale, purchase in zip(sale_prices, purchase_prices))
            
            total_storage_cost = storage_cost_monthly * total_storage_months
            
            total_injection_cost = injection_cost * (total_volume / 1_000_000)
            total_withdrawal_cost = withdrawal_cost * (total_volume / 1_000_000)
            
            total_transport_cost = transport_cost * 2 * len(injection_dates)  # Both ways for each trade
            
            total_costs = (total_storage_cost + total_injection_cost + total_withdrawal_cost + total_transport_cost)

            net_value = gross_profit - total_costs

            return {
                'contract_value': net_value,
                'details': {
                    'gross_profit': gross_profit,
                    'storage_cost': total_storage_cost,
                    'injection_cost': total_injection_cost,
                    'withdrawal_cost': total_withdrawal_cost,
                    'transport_cost': total_transport_cost,
                    'total_costs': total_costs,
                    'purchase_prices': purchase_prices,
                    'sale_prices': sale_prices
                }
            }

        except Exception as e:
            raise ValueError(f"Error calculating contract value: {str(e)}")

def get_dates_input(prompt):
    #Get and validate dates input.
    while True:
        try:
            dates_str = input(prompt)
            if dates_str.lower() == 'quit':
                return None
            dates = [date.strip() for date in dates_str.split(',')]
            # Validate date format
            for date in dates:
                pd.to_datetime(date)
            return dates
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format, separated by commas.")

def get_float_input(prompt, min_value=0):
    #Get and validate float input.
    while True:
        try:
            value = input(prompt)
            if value.lower() == 'quit':
                return None
            value = float(value)
            if value < min_value:
                print(f"Value must be greater than {min_value}")
                continue
            return value
        except ValueError:
            print("Invalid number. Please enter a valid number.")

if __name__ == "__main__":
    print("\nNatural Gas Storage Contract Pricer")
    print("===================================")
    print("(Type 'quit' at any prompt to exit)")
    print("\nPlease enter the following parameters:")

    try:
        # Get injection dates
        injection_dates = get_dates_input("\nInjection dates (YYYY-MM-DD, comma-separated): ")
        if injection_dates is None:
            exit()

        # Get withdrawal dates
        withdrawal_dates = get_dates_input("\nWithdrawal dates (YYYY-MM-DD, comma-separated): ")
        if withdrawal_dates is None:
            exit()

        if len(injection_dates) != len(withdrawal_dates):
            print("Error: Number of injection and withdrawal dates must match!")
            exit()

        # Get volume and rates
        volume_per_trade = get_float_input("\nVolume per trade (in MMBtu): ")
        if volume_per_trade is None:
            exit()

        injection_rate = get_float_input("\nInjection rate (MMBtu per day): ")
        if injection_rate is None:
            exit()

        withdrawal_rate = get_float_input("\nWithdrawal rate (MMBtu per day): ")
        if withdrawal_rate is None:
            exit()

        max_storage = get_float_input("\nMaximum storage capacity (MMBtu): ")
        if max_storage is None:
            exit()

        # Optional parameters with defaults
        print("\nOptional parameters (press Enter to use defaults):")
        
        storage_cost = input("\nMonthly storage cost (default: $100,000): ")
        storage_cost = float(storage_cost) if storage_cost else 100000

        injection_cost = input("\nInjection cost per million MMBtu (default: $10,000): ")
        injection_cost = float(injection_cost) if injection_cost else 10000

        withdrawal_cost = input("\nWithdrawal cost per million MMBtu (default: $10,000): ")
        withdrawal_cost = float(withdrawal_cost) if withdrawal_cost else 10000

        transport_cost = input("\nTransport cost per operation (default: $50,000): ")
        transport_cost = float(transport_cost) if transport_cost else 50000

        # Initialize models and calculate
        predictor = GasPricePredictor('data/raw/Nat_Gas.csv')
        pricer = StorageContractPricer(predictor)
        
        result = pricer.calculate_contract_value(
            injection_dates=injection_dates,
            withdrawal_dates=withdrawal_dates,
            volume_per_trade=volume_per_trade,
            injection_rate=injection_rate,
            withdrawal_rate=withdrawal_rate,
            max_storage=max_storage,
            storage_cost_monthly=storage_cost,
            injection_cost=injection_cost,
            withdrawal_cost=withdrawal_cost,
            transport_cost=transport_cost
        )

        # Print results
        print("\n=== Contract Valuation Results ===")
        print(f"\nNet Contract Value: ${result['contract_value']:,.2f}")
        print("\nBreakdown:")
        print("---------")
        for i, (inj_date, with_date, purchase, sale) in enumerate(zip(
            injection_dates, withdrawal_dates, 
            result['details']['purchase_prices'], 
            result['details']['sale_prices'])):
            print(f"\nTrade {i+1}:")
            print(f"  Injection Date: {inj_date}")
            print(f"  Purchase Price: ${purchase:.2f}")
            print(f"  Withdrawal Date: {with_date}")
            print(f"  Sale Price: ${sale:.2f}")

        print("\nCosts:")
        for key, value in result['details'].items():
            if key not in ['purchase_prices', 'sale_prices']:
                print(f"  {key.replace('_', ' ').title()}: ${value:,.2f}")

    except Exception as e:
        print(f"\nError: {str(e)}")