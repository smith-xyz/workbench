"""Model registry for managing available models."""

from typing import Any

from .base import BaseModel
from .linear import LinearRegressionModel, LogisticRegressionModel


class ModelRegistry:
    """Registry for managing available ML models."""

    def __init__(self):
        """Initialize the model registry with default models."""
        self._models: dict[str, type[BaseModel]] = {
            "linear_regression": LinearRegressionModel,
            "logistic_regression": LogisticRegressionModel,
        }

        # Try to import optional models
        self._register_optional_models()

    def _register_optional_models(self) -> None:
        """Register optional models that require additional dependencies."""
        try:
            from .ensemble import RandomForestModel, XGBoostModel

            self._models.update(
                {
                    "random_forest": RandomForestModel,
                    "xgboost": XGBoostModel,
                }
            )
        except ImportError:
            pass

    def register_model(self, name: str, model_class: type[BaseModel]) -> None:
        """Register a new model type.

        Args:
            name: Name to register the model under.
            model_class: Model class to register.
        """
        if not issubclass(model_class, BaseModel):
            raise ValueError("Model class must inherit from BaseModel")

        self._models[name] = model_class

    def get_model(self, name: str, **kwargs: Any) -> BaseModel:
        """Get a model instance by name.

        Args:
            name: Name of the model to get.
            **kwargs: Hyperparameters for the model.

        Returns:
            Model instance.
        """
        if name not in self._models:
            available = ", ".join(self._models.keys())
            raise ValueError(f"Model '{name}' not found. Available models: {available}")

        return self._models[name](**kwargs)

    def get_model_class(self, name: str) -> type[BaseModel]:
        """Get a model class by name.

        Args:
            name: Name of the model class to get.

        Returns:
            Model class.
        """
        if name not in self._models:
            available = ", ".join(self._models.keys())
            raise ValueError(f"Model '{name}' not found. Available models: {available}")

        return self._models[name]

    def list_models(self) -> dict[str, dict[str, str]]:
        """List all available models with metadata.

        Returns:
            Dictionary mapping model names to metadata.
        """
        models_info = {}

        for name, model_class in self._models.items():
            # Determine model type based on name and class
            if "regression" in name.lower() and "logistic" not in name.lower():
                model_type = "Regression"
            elif "classification" in name.lower() or "logistic" in name.lower():
                model_type = "Classification"
            elif "forest" in name.lower() or "xgboost" in name.lower():
                model_type = "Ensemble"
            else:
                model_type = "General"

            # Get description from docstring if available
            description = (
                model_class.__doc__.split("\n")[0]
                if model_class.__doc__
                else "No description available"
            )

            models_info[name] = {
                "type": model_type,
                "description": description,
                "class": model_class.__name__,
            }

        return models_info

    def is_available(self, name: str) -> bool:
        """Check if a model is available.

        Args:
            name: Name of the model to check.

        Returns:
            True if model is available, False otherwise.
        """
        return name in self._models
