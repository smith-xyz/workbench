"""Model evaluation utilities."""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)

from ..models.base import BaseModel


class Evaluator:
    """Evaluates ML model performance with appropriate metrics."""

    def __init__(self):
        """Initialize the evaluator."""
        pass

    def evaluate(
        self,
        model: BaseModel,
        X_test: pd.DataFrame | np.ndarray,
        y_test: pd.Series | np.ndarray,
        problem_type: str = "auto",
    ) -> dict[str, float]:
        """Evaluate model performance.

        Args:
            model: Trained model to evaluate.
            X_test: Test features.
            y_test: Test targets.
            problem_type: Either 'classification', 'regression', or 'auto'.

        Returns:
            Dictionary of metric names and values.
        """
        # Make predictions
        y_pred = model.predict(X_test)

        # Auto-detect problem type if needed
        if problem_type == "auto":
            problem_type = self._detect_problem_type(y_test, y_pred)

        # Calculate appropriate metrics
        if problem_type == "classification":
            return self._evaluate_classification(y_test, y_pred)
        elif problem_type == "regression":
            return self._evaluate_regression(y_test, y_pred)
        else:
            raise ValueError(
                "problem_type must be 'classification', 'regression', or 'auto'"
            )

    def _detect_problem_type(
        self, y_true: pd.Series | np.ndarray, y_pred: pd.Series | np.ndarray
    ) -> str:
        """Auto-detect if this is a classification or regression problem.

        Args:
            y_true: True values.
            y_pred: Predicted values.

        Returns:
            Problem type: 'classification' or 'regression'.
        """
        # Convert to numpy arrays
        if isinstance(y_true, pd.Series):
            y_true = y_true.values
        if isinstance(y_pred, pd.Series):
            y_pred = y_pred.values

        # Check if predictions are all integers and have limited unique values
        unique_true = len(np.unique(y_true))
        unique_pred = len(np.unique(y_pred))

        # Heuristic: if both true and predicted have <= 20 unique values
        # and predictions are close to integers, treat as classification
        if unique_true <= 20 and unique_pred <= 20:
            if np.allclose(y_pred, np.round(y_pred), atol=0.1):
                return "classification"

        return "regression"

    def _evaluate_classification(
        self, y_true: pd.Series | np.ndarray, y_pred: pd.Series | np.ndarray
    ) -> dict[str, float]:
        """Evaluate classification model performance.

        Args:
            y_true: True labels.
            y_pred: Predicted labels.

        Returns:
            Dictionary of classification metrics.
        """
        # Convert to numpy arrays
        if isinstance(y_true, pd.Series):
            y_true = y_true.values
        if isinstance(y_pred, pd.Series):
            y_pred = y_pred.values

        # Round predictions to nearest integer for classification
        y_pred_rounded = np.round(y_pred).astype(int)

        metrics = {
            "accuracy": accuracy_score(y_true, y_pred_rounded),
            "precision": precision_score(
                y_true, y_pred_rounded, average="weighted", zero_division=0
            ),
            "recall": recall_score(
                y_true, y_pred_rounded, average="weighted", zero_division=0
            ),
            "f1_score": f1_score(
                y_true, y_pred_rounded, average="weighted", zero_division=0
            ),
        }

        return metrics

    def _evaluate_regression(
        self, y_true: pd.Series | np.ndarray, y_pred: pd.Series | np.ndarray
    ) -> dict[str, float]:
        """Evaluate regression model performance.

        Args:
            y_true: True values.
            y_pred: Predicted values.

        Returns:
            Dictionary of regression metrics.
        """
        # Convert to numpy arrays
        if isinstance(y_true, pd.Series):
            y_true = y_true.values
        if isinstance(y_pred, pd.Series):
            y_pred = y_pred.values

        metrics = {
            "mae": mean_absolute_error(y_true, y_pred),
            "mse": mean_squared_error(y_true, y_pred),
            "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
            "r2_score": r2_score(y_true, y_pred),
        }

        return metrics

    def generate_report(
        self,
        model: BaseModel,
        X_test: pd.DataFrame | np.ndarray,
        y_test: pd.Series | np.ndarray,
        problem_type: str = "auto",
    ) -> str:
        """Generate a detailed evaluation report.

        Args:
            model: Trained model to evaluate.
            X_test: Test features.
            y_test: Test targets.
            problem_type: Either 'classification', 'regression', or 'auto'.

        Returns:
            String containing detailed evaluation report.
        """
        metrics = self.evaluate(model, X_test, y_test, problem_type)

        report = "Model Evaluation Report\n"
        report += "=" * 25 + "\n\n"

        for metric_name, value in metrics.items():
            report += f"{metric_name.upper():<12}: {value:.4f}\n"

        return report
