import os
import pickle
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import logger

class DataTransformation:
    def __init__(self):
        self.input_path = "artifacts/data_validation/validated_data.csv"
        self.output_dir = "artifacts/data_transformation"
        self.pipeline_path = "model_pipeline.pkl"

    def initiate_data_transformation(self):
        try:
            os.makedirs(self.output_dir, exist_ok=True)

            df = pd.read_csv(self.input_path)

            df["Date"] = pd.to_datetime(df["Date"])
            df = df.sort_values("Date")

            df["Daily_Return"] = df["Close"].pct_change()
            df["MA_7"] = df["Close"].rolling(window=7).mean()
            df["MA_14"] = df["Close"].rolling(window=14).mean()
            df["Volatility"] = df["Close"].rolling(window=7).std()

            df = df.dropna()

            features = ["Open", "High", "Low", "Volume", 
                        "Daily_Return", "MA_7", "MA_14", "Volatility"]

            X = df[features]
            y = df["Close"]

            # Split before fitting
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, shuffle=False
            )

            # Create pipeline (scaling + model)
            pipeline = Pipeline([
                ("scaler", StandardScaler()),
                ("model", LinearRegression())
            ])

            pipeline.fit(X_train, y_train)

            # Save entire pipeline
            with open(os.path.join(self.output_dir, self.pipeline_path), "wb") as f:
                pickle.dump(pipeline, f)


            logger.info("Data transformation completed successfully.")

        except Exception as e:
            logger.error(f"Error in Data Transformation: {e}")
            raise Exception(f"Error in Data Transformation: {e}")