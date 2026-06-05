"""Model training utilities."""

import uuid
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from ..models.base import BaseModel


class Trainer:
    """Handles model training with optional experiment tracking."""

    def __init__(
        self,
        experiment_name: str | None = None,
        run_name: str | None = None,
        tracking_uri: str | None = None,
    ):
        """Initialize the trainer.

        Args:
            experiment_name: Name of the experiment for tracking.
            run_name: Name of the run for tracking.
            tracking_uri: URI for experiment tracking (e.g., MLflow).
        """
        self.experiment_name = experiment_name or "default_experiment"
        self.run_name = run_name
        self.tracking_uri = tracking_uri
        self.run_id = str(uuid.uuid4())[:8]  # Short unique ID for this run

        # Initialize experiment tracking if available
        self._init_tracking()

    def _init_tracking(self) -> None:
        """Initialize experiment tracking (MLflow, etc.)."""
        # This is a placeholder for experiment tracking setup
        # In a real implementation, you might initialize MLflow here
        self.tracking_enabled = False

        try:
            # Optional MLflow integration
            import mlflow

            if self.tracking_uri:
                mlflow.set_tracking_uri(self.tracking_uri)

            mlflow.set_experiment(self.experiment_name)
            self.tracking_enabled = True

        except ImportError:
            # MLflow not available, continue without tracking
            pass

    def train(
        self,
        model: BaseModel,
        X_train: pd.DataFrame | np.ndarray,
        y_train: pd.Series | np.ndarray,
        X_val: pd.DataFrame | np.ndarray | None = None,
        y_val: pd.Series | np.ndarray | None = None,
        **train_kwargs: Any,
    ) -> BaseModel:
        """Train a model with optional validation.

        Args:
            model: Model instance to train.
            X_train: Training features.
            y_train: Training targets.
            X_val: Validation features (optional).
            y_val: Validation targets (optional).
            **train_kwargs: Additional training parameters.

        Returns:
            Trained model instance.
        """
        if self.tracking_enabled:
            self._start_run()

        try:
            # Log model parameters if tracking is enabled
            if self.tracking_enabled:
                self._log_params(model, train_kwargs)

            # Train the model
            trained_model = model.fit(X_train, y_train, **train_kwargs)

            # Validate if validation data is provided
            if X_val is not None and y_val is not None:
                val_metrics = self._validate_model(trained_model, X_val, y_val)

                if self.tracking_enabled:
                    self._log_metrics(val_metrics, prefix="val_")

            # Log training completion
            if self.tracking_enabled:
                self._log_metrics({"training_completed": 1.0})

            return trained_model

        finally:
            if self.tracking_enabled:
                self._end_run()

    def _validate_model(
        self,
        model: BaseModel,
        X_val: pd.DataFrame | np.ndarray,
        y_val: pd.Series | np.ndarray,
    ) -> dict[str, float]:
        """Validate the trained model.

        Args:
            model: Trained model to validate.
            X_val: Validation features.
            y_val: Validation targets.

        Returns:
            Dictionary of validation metrics.
        """
        # Import here to avoid circular imports
        from ..evaluation.evaluator import Evaluator

        evaluator = Evaluator()
        return evaluator.evaluate(model, X_val, y_val)

    def _start_run(self) -> None:
        """Start experiment tracking run."""
        if not self.tracking_enabled:
            return

        try:
            import mlflow

            mlflow.start_run(run_name=self.run_name)

            # Update run_id with MLflow's run ID if available
            if mlflow.active_run():
                self.run_id = mlflow.active_run().info.run_id[:8]

        except ImportError:
            pass

    def _end_run(self) -> None:
        """End experiment tracking run."""
        if not self.tracking_enabled:
            return

        try:
            import mlflow

            mlflow.end_run()
        except ImportError:
            pass

    def _log_params(self, model: BaseModel, train_kwargs: dict[str, Any]) -> None:
        """Log model parameters to experiment tracking.

        Args:
            model: Model instance.
            train_kwargs: Training keyword arguments.
        """
        if not self.tracking_enabled:
            return

        try:
            import mlflow

            # Log model type
            mlflow.log_param("model_type", model.__class__.__name__)

            # Log model hyperparameters
            if hasattr(model, "get_params"):
                params = model.get_params()
                for key, value in params.items():
                    mlflow.log_param(f"model_{key}", value)

            # Log training arguments
            for key, value in train_kwargs.items():
                mlflow.log_param(f"train_{key}", value)

        except ImportError:
            pass

    def _log_metrics(self, metrics: dict[str, float], prefix: str = "") -> None:
        """Log metrics to experiment tracking.

        Args:
            metrics: Dictionary of metric names and values.
            prefix: Prefix to add to metric names.
        """
        if not self.tracking_enabled:
            return

        try:
            import mlflow

            for name, value in metrics.items():
                mlflow.log_metric(f"{prefix}{name}", value)

        except ImportError:
            pass

    def save_model(
        self,
        model: BaseModel,
        save_path: str | Path,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Save trained model to disk.

        Args:
            model: Trained model to save.
            save_path: Path to save the model.
            metadata: Optional metadata to save with the model.
        """
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Use the model's save method
        model.save(save_path)

        # Save metadata if provided
        if metadata:
            metadata_path = save_path.with_suffix(".metadata.json")
            import json

            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

    def load_model(
        self,
        model_class: type[BaseModel],
        load_path: str | Path,
    ) -> BaseModel:
        """Load a saved model.

        Args:
            model_class: Class of the model to load.
            load_path: Path to the saved model.

        Returns:
            Loaded model instance.
        """
        return model_class.load(load_path)
