"""Base model class defining the interface for all ML models."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import polars as pl
from sklearn.base import BaseEstimator


class BaseModel(ABC):
    """Abstract base class for all ML models."""

    def __init__(self, **kwargs: Any):
        """Initialize the model with hyperparameters."""
        self.model: BaseEstimator | None = None
        self.is_fitted = False
        self.hyperparameters = kwargs

    @abstractmethod
    def build_model(self) -> BaseEstimator:
        """Build and return the sklearn model instance."""
        pass

    def fit(
        self,
        X: pd.DataFrame | pl.DataFrame | np.ndarray,
        y: pd.Series | pl.Series | np.ndarray,
        **kwargs: Any,
    ) -> "BaseModel":
        """Fit the model to training data.

        Args:
            X: Training features.
            y: Training targets.
            **kwargs: Additional fitting parameters.

        Returns:
            Self for method chaining.
        """
        if self.model is None:
            self.model = self.build_model()

        # Convert to numpy if needed
        X_np = self._to_numpy(X)
        y_np = self._to_numpy(y)

        self.model.fit(X_np, y_np, **kwargs)
        self.is_fitted = True
        return self

    def predict(self, X: pd.DataFrame | pl.DataFrame | np.ndarray) -> np.ndarray:
        """Make predictions on new data.

        Args:
            X: Features to predict on.

        Returns:
            Predictions as numpy array.
        """
        if not self.is_fitted or self.model is None:
            raise ValueError("Model must be fitted before making predictions")

        X_np = self._to_numpy(X)
        return self.model.predict(X_np)

    def predict_proba(self, X: pd.DataFrame | pl.DataFrame | np.ndarray) -> np.ndarray:
        """Predict class probabilities (for classification models).

        Args:
            X: Features to predict on.

        Returns:
            Class probabilities as numpy array.
        """
        if not self.is_fitted or self.model is None:
            raise ValueError("Model must be fitted before making predictions")

        if not hasattr(self.model, "predict_proba"):
            raise ValueError("Model does not support probability predictions")

        X_np = self._to_numpy(X)
        return self.model.predict_proba(X_np)

    def save(self, file_path: str | Path) -> None:
        """Save the fitted model to disk.

        Args:
            file_path: Path to save the model.
        """
        if not self.is_fitted or self.model is None:
            raise ValueError("Cannot save unfitted model")

        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        model_data = {
            "model": self.model,
            "hyperparameters": self.hyperparameters,
            "is_fitted": self.is_fitted,
            "model_type": self.__class__.__name__,
        }

        joblib.dump(model_data, file_path)

    @classmethod
    def load(cls, file_path: str | Path) -> "BaseModel":
        """Load a fitted model from disk.

        Args:
            file_path: Path to the saved model.

        Returns:
            Loaded model instance.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Model file not found: {file_path}")

        model_data = joblib.load(file_path)

        # Create new instance with saved hyperparameters
        instance = cls(**model_data["hyperparameters"])
        instance.model = model_data["model"]
        instance.is_fitted = model_data["is_fitted"]

        return instance

    def get_params(self) -> dict[str, Any]:
        """Get model hyperparameters.

        Returns:
            Dictionary of hyperparameters.
        """
        if self.model is not None:
            return self.model.get_params()
        return self.hyperparameters

    def set_params(self, **params: Any) -> "BaseModel":
        """Set model hyperparameters.

        Args:
            **params: Parameters to set.

        Returns:
            Self for method chaining.
        """
        self.hyperparameters.update(params)
        if self.model is not None:
            self.model.set_params(**params)
        return self

    def _to_numpy(
        self, data: pd.DataFrame | pl.DataFrame | pd.Series | pl.Series | np.ndarray
    ) -> np.ndarray:
        """Convert various data types to numpy array.

        Args:
            data: Input data.

        Returns:
            Numpy array.
        """
        if isinstance(data, np.ndarray):
            return data
        elif isinstance(data, (pd.DataFrame, pd.Series)):
            return data.values
        elif isinstance(data, (pl.DataFrame, pl.Series)):
            return data.to_numpy()
        else:
            return np.array(data)

    def __repr__(self) -> str:
        """String representation of the model."""
        status = "fitted" if self.is_fitted else "not fitted"
        return f"{self.__class__.__name__}({status})"
