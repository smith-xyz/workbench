"""Data loading utilities."""

from pathlib import Path
from typing import Any

import pandas as pd
import polars as pl
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split

from ..config import config


class DataLoader:
    """Handles data loading from various sources."""

    def __init__(self, use_polars: bool = False):
        """Initialize data loader.

        Args:
            use_polars: Whether to use Polars instead of Pandas for better performance.
        """
        self.use_polars = use_polars
        self.config = config.data

    def load_csv(
        self, file_path: str | Path, **kwargs: Any
    ) -> pd.DataFrame | pl.DataFrame:
        """Load data from CSV file.

        Args:
            file_path: Path to CSV file.
            **kwargs: Additional arguments for CSV reader.

        Returns:
            DataFrame with loaded data.
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        if self.use_polars:
            return pl.read_csv(file_path, **kwargs)
        else:
            return pd.read_csv(file_path, **kwargs)

    def load_parquet(self, file_path: str | Path) -> pd.DataFrame | pl.DataFrame:
        """Load data from Parquet file.

        Args:
            file_path: Path to Parquet file.

        Returns:
            DataFrame with loaded data.
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        if self.use_polars:
            return pl.read_parquet(file_path)
        else:
            return pd.read_parquet(file_path)

    def generate_sample_data(
        self,
        problem_type: str = "classification",
        n_samples: int = 1000,
        n_features: int = 20,
        **kwargs: Any,
    ) -> pd.DataFrame | pl.DataFrame:
        """Generate sample data for testing.

        Args:
            problem_type: Either 'classification' or 'regression'.
            n_samples: Number of samples to generate.
            n_features: Number of features to generate.
            **kwargs: Additional arguments for data generation.

        Returns:
            DataFrame with generated data.
        """
        if problem_type == "classification":
            X, y = make_classification(
                n_samples=n_samples,
                n_features=n_features,
                n_informative=max(2, n_features // 2),
                n_redundant=max(0, n_features // 4),
                random_state=self.config.random_seed,
                **kwargs,
            )
        elif problem_type == "regression":
            X, y = make_regression(
                n_samples=n_samples,
                n_features=n_features,
                noise=0.1,
                random_state=self.config.random_seed,
                **kwargs,
            )
        else:
            raise ValueError("problem_type must be 'classification' or 'regression'")

        # Create feature names
        feature_names = [f"feature_{i:02d}" for i in range(n_features)]

        if self.use_polars:
            # Create Polars DataFrame
            data_dict = {name: X[:, i] for i, name in enumerate(feature_names)}
            data_dict["target"] = y
            return pl.DataFrame(data_dict)
        else:
            # Create Pandas DataFrame
            df = pd.DataFrame(X, columns=feature_names)
            df["target"] = y
            return df

    def split_data(
        self,
        data: pd.DataFrame | pl.DataFrame,
        target_column: str = "target",
        stratify: bool = False,
    ) -> tuple[
        pd.DataFrame | pl.DataFrame,
        pd.DataFrame | pl.DataFrame,
        pd.DataFrame | pl.DataFrame,
        pd.Series | pl.Series,
        pd.Series | pl.Series,
        pd.Series | pl.Series,
    ]:
        """Split data into train/validation/test sets.

        Args:
            data: Input DataFrame.
            target_column: Name of target column.
            stratify: Whether to stratify split (for classification).

        Returns:
            Tuple of (X_train, X_val, X_test, y_train, y_val, y_test).
        """
        if self.use_polars:
            X = data.drop(target_column)
            y = data[target_column]

            # Convert to pandas for sklearn compatibility
            X_pd = X.to_pandas()
            y_pd = y.to_pandas()
        else:
            X = data.drop(columns=[target_column])
            y = data[target_column]
            X_pd = X
            y_pd = y

        # First split: train + val vs test
        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X_pd,
            y_pd,
            test_size=self.config.test_size,
            random_state=self.config.random_seed,
            stratify=y_pd if stratify else None,
        )

        # Second split: train vs val
        val_size_adjusted = self.config.val_size / (1 - self.config.test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val,
            y_train_val,
            test_size=val_size_adjusted,
            random_state=self.config.random_seed,
            stratify=y_train_val if stratify else None,
        )

        if self.use_polars:
            # Convert back to Polars
            return (
                pl.from_pandas(X_train),
                pl.from_pandas(X_val),
                pl.from_pandas(X_test),
                pl.from_pandas(y_train),
                pl.from_pandas(y_val),
                pl.from_pandas(y_test),
            )
        else:
            return X_train, X_val, X_test, y_train, y_val, y_test

    def save_data(
        self,
        data: pd.DataFrame | pl.DataFrame,
        file_path: str | Path,
        format: str = "parquet",
    ) -> None:
        """Save data to file.

        Args:
            data: DataFrame to save.
            file_path: Output file path.
            format: File format ('csv' or 'parquet').
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "csv":
            if self.use_polars:
                data.write_csv(file_path)
            else:
                data.to_csv(file_path, index=False)
        elif format == "parquet":
            if self.use_polars:
                data.write_parquet(file_path)
            else:
                data.to_parquet(file_path, index=False)
        else:
            raise ValueError("format must be 'csv' or 'parquet'")
