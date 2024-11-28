import pandas as pd
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

def load_gas_prices(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        df['Dates'] = pd.to_datetime(df['Dates'])
        df.set_index('Dates', inplace=True)
        df.sort_index(inplace=True)
        logger.info(f"Successfully loaded data from {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def split_train_test(df: pd.DataFrame, train_size: float = 0.8) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_size = int(len(df) * train_size)
    train_data = df[:train_size]
    test_data = df[train_size:]
    return train_data, test_data