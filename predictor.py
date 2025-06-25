import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import csv 
from datetime import datetime

def add_features(dataframe: pd.DataFrame) -> pd.DataFrame: 
    """ Add technical features to the DataFrame for model training.
    Parameters: 
    dataframe (pd.DataFrame): DataFrame containing historical commodity data with 'Close' prices.
    Returns:
    dataframe (pd.DataFrame): DataFrame with additional features.
    """
    dataframe = dataframe.copy()
    
    dataframe["Return"] = dataframe["Close"].pct_change() # Calculate daily returns
    dataframe["MA_5"] = dataframe["Close"].rolling(window=5).mean() # 5-day moving average
    dataframe["MA_20"] = dataframe["Close"].rolling(window=20).mean() # 20-day moving average
    dataframe["Volatility"] = dataframe["Close"].rolling(window=5).std() # 5-day rolling volatility
    dataframe.dropna(inplace=True)  # Drop rows with NaN values after feature engineering
    return dataframe

def train_model(dataframe: pd.DataFrame) -> tuple[RandomForestRegressor, pd.DataFrame]:
    """
    Train a Random Forest model on the provided DataFrame.
    Parameters:
    dataframe (pd.DataFrame): DataFrame containing historical commodity data with 'Close' prices.
    Returns:
    model (RandomForestRegressor): Trained Random Forest model.
    dataframe (pd.DataFrame): DataFrame with additional features and target variable.
    """
    dataframe = add_features(dataframe)
    dataframe["Target"] = dataframe["Close"].shift(-1)  # Predict next day's close
    dataframe.dropna(inplace=True)  # Drop rows with NaN values after target creation

    X = dataframe[["Return", "MA_5", "MA_20", "Volatility"]] # Features for the model
    y = dataframe["Target"] # Label (next day's close)

    model = RandomForestRegressor(n_estimators=100, random_state=42) # Initialize the model
    model.fit(X, y) # Train the model

    return model, dataframe

def predict_next_close(model, dataframe) -> float:
    """
    Predict the next day's close price using the trained model.
    Parameters:
    model (RandomForestRegressor): Trained Random Forest model.
    dataframe (pd.DataFrame): DataFrame containing historical commodity data with 'Close' prices.
    Returns:
    float: Predicted next day's close price.
    """
    last_row = dataframe[["Return", "MA_5", "MA_20", "Volatility"]].iloc[-1:]
    prediction = model.predict(last_row)[0]

    return prediction

def log_prediction(ticker: str, actual: float, predicted: float, signal: str):
    with open("predictions_log.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), ticker, actual, predicted, signal])