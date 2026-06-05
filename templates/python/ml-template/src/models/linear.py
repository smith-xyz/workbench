"""Linear models for regression and classification."""

from typing import Any

from sklearn.linear_model import LinearRegression, LogisticRegression

from .base import BaseModel


class LinearRegressionModel(BaseModel):
    """Linear regression model wrapper."""

    def __init__(self, **kwargs: Any):
        """Initialize linear regression model.

        Args:
            **kwargs: Hyperparameters for LinearRegression.
        """
        # Set default hyperparameters
        default_params = {
            "fit_intercept": True,
            "copy_X": True,
            "n_jobs": None,
            "positive": False,
        }
        default_params.update(kwargs)
        super().__init__(**default_params)

    def build_model(self) -> LinearRegression:
        """Build and return LinearRegression instance.

        Returns:
            Configured LinearRegression model.
        """
        return LinearRegression(**self.hyperparameters)


class LogisticRegressionModel(BaseModel):
    """Logistic regression model wrapper."""

    def __init__(self, **kwargs: Any):
        """Initialize logistic regression model.

        Args:
            **kwargs: Hyperparameters for LogisticRegression.
        """
        # Set default hyperparameters
        default_params = {
            "penalty": "l2",
            "C": 1.0,
            "fit_intercept": True,
            "solver": "lbfgs",
            "max_iter": 1000,
            "random_state": 42,
            "n_jobs": None,
        }
        default_params.update(kwargs)
        super().__init__(**default_params)

    def build_model(self) -> LogisticRegression:
        """Build and return LogisticRegression instance.

        Returns:
            Configured LogisticRegression model.
        """
        return LogisticRegression(**self.hyperparameters)
