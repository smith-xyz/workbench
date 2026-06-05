"""Ensemble models for classification and regression."""

from typing import Any

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from .base import BaseModel

try:
    import xgboost as xgb

    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False


class RandomForestModel(BaseModel):
    """Random Forest model wrapper that can handle both classification and regression."""

    def __init__(self, problem_type: str = "classification", **kwargs: Any):
        """Initialize Random Forest model.

        Args:
            problem_type: Either 'classification' or 'regression'.
            **kwargs: Hyperparameters for RandomForest.
        """
        if problem_type not in ["classification", "regression"]:
            raise ValueError("problem_type must be 'classification' or 'regression'")

        self.problem_type = problem_type

        # Set default hyperparameters
        default_params = {
            "n_estimators": 100,
            "max_depth": None,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "random_state": 42,
            "n_jobs": -1,
        }
        default_params.update(kwargs)
        super().__init__(**default_params)

    def build_model(self):
        """Build and return RandomForest instance.

        Returns:
            Configured RandomForest model.
        """
        if self.problem_type == "classification":
            return RandomForestClassifier(**self.hyperparameters)
        else:
            return RandomForestRegressor(**self.hyperparameters)


class XGBoostModel(BaseModel):
    """XGBoost model wrapper that can handle both classification and regression."""

    def __init__(self, problem_type: str = "classification", **kwargs: Any):
        """Initialize XGBoost model.

        Args:
            problem_type: Either 'classification' or 'regression'.
            **kwargs: Hyperparameters for XGBoost.
        """
        if not XGBOOST_AVAILABLE:
            raise ImportError(
                "XGBoost is not installed. Install with: pip install xgboost"
            )

        if problem_type not in ["classification", "regression"]:
            raise ValueError("problem_type must be 'classification' or 'regression'")

        self.problem_type = problem_type

        # Set default hyperparameters
        default_params = {
            "n_estimators": 100,
            "max_depth": 6,
            "learning_rate": 0.1,
            "subsample": 1.0,
            "colsample_bytree": 1.0,
            "random_state": 42,
            "n_jobs": -1,
        }
        default_params.update(kwargs)
        super().__init__(**default_params)

    def build_model(self):
        """Build and return XGBoost instance.

        Returns:
            Configured XGBoost model.
        """
        if self.problem_type == "classification":
            return xgb.XGBClassifier(**self.hyperparameters)
        else:
            return xgb.XGBRegressor(**self.hyperparameters)
