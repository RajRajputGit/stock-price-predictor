import os
import pandas as pd
from datetime import datetime
import hashlib

def get_data_version(df: pd.DataFrame) -> str:
    """
    Generates a unique version ID based on the content of the data.
    If the data changes, the hash changes.
    """
    # Create a string representation of the data and hash it
    hash_object = hashlib.md5(df.to_string().encode())
    return hash_object.hexdigest()[:8]  # Short 8-character version tag

def save_versioned_data(df: pd.DataFrame, base_path: str, ticker: str):
    """
    Saves the dataframe with a version tag and maintains a 'latest' symlink/file.
    """
    os.makedirs(base_path, exist_ok=True)
    
    # 1. Generate versioning metadata
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    data_hash = get_data_version(df)
    version_tag = f"{timestamp}_{data_hash}"
    
    # 2. Save the specific versioned file (The Archive)
    versioned_filename = f"{ticker}_{version_tag}.csv"
    versioned_path = os.path.join(base_path, versioned_filename)
    df.to_csv(versioned_path, index=False)
    
    # 3. Update the 'latest' file (The Pointer for the next component)
    latest_path = os.path.join(base_path, f"{ticker}_latest.csv")
    df.to_csv(latest_path, index=False)
    
    print(f"Data versioned: {version_tag}")
    return versioned_path

# Example usage within your project structure:
# df = yf.download(ticker, ...)
# save_versioned_data(df, "data/raw", "AAPL")