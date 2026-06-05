"""Test cases for model implementations."""

import numpy as np
import pytest
from sklearn.datasets import make_classification, make_regression

from src.models.linear import LinearRegressionModel, LogisticRegressionModel
from src.models.registry import ModelRegistry


class TestLinearRegression:
    """Test cases for LinearRegressionModel."""

    def setup_method(self):
        """Set up test fixtures."""
        self.X, self.y = make_regression(n_samples=100, n_features=5, random_state=42)
        self.model = LinearRegressionModel()

    def test_initialization(self):
        """Test model initialization."""
        assert self.model.model is None
        assert not self.model.is_fitted
        assert isinstance(self.model.hyperparameters, dict)

    def test_fit_predict(self):
        """Test model fitting and prediction."""
        # Fit the model
        self.model.fit(self.X, self.y)
        assert self.model.is_fitted
        assert self.model.model is not None

        # Make predictions
        predictions = self.model.predict(self.X)
        assert predictions.shape == (100,)
        assert isinstance(predictions, np.ndarray)

    def test_save_load(self, tmp_path):
        """Test model saving and loading."""
        # Fit and save model
        self.model.fit(self.X, self.y)
        model_path = tmp_path / "test_model.joblib"
        self.model.save(model_path)

        # Load model
        loaded_model = LinearRegressionModel.load(model_path)
        assert loaded_model.is_fitted

        # Compare predictions
        original_predictions = self.model.predict(self.X)
        loaded_predictions = loaded_model.predict(self.X)
        np.testing.assert_array_equal(original_predictions, loaded_predictions)

    def test_unfitted_model_error(self):
        """Test error when predicting with unfitted model."""
        with pytest.raises(ValueError, match="Model must be fitted"):
            self.model.predict(self.X)


class TestLogisticRegression:
    """Test cases for LogisticRegressionModel."""

    def setup_method(self):
        """Set up test fixtures."""
        self.X, self.y = make_classification(
            n_samples=100, n_features=5, random_state=42
        )
        self.model = LogisticRegressionModel()

    def test_fit_predict(self):
        """Test model fitting and prediction."""
        # Fit the model
        self.model.fit(self.X, self.y)
        assert self.model.is_fitted

        # Make predictions
        predictions = self.model.predict(self.X)
        assert predictions.shape == (100,)

        # Make probability predictions
        probabilities = self.model.predict_proba(self.X)
        assert probabilities.shape == (100, 2)  # Binary classification
        assert np.allclose(probabilities.sum(axis=1), 1.0)  # Probabilities sum to 1

    def test_hyperparameters(self):
        """Test hyperparameter setting."""
        custom_model = LogisticRegressionModel(C=0.5, max_iter=500)
        assert custom_model.hyperparameters["C"] == 0.5
        assert custom_model.hyperparameters["max_iter"] == 500


class TestModelRegistry:
    """Test cases for ModelRegistry."""

    def setup_method(self):
        """Set up test fixtures."""
        self.registry = ModelRegistry()

    def test_list_models(self):
        """Test listing available models."""
        models = self.registry.list_models()
        assert isinstance(models, dict)
        assert "linear_regression" in models
        assert "logistic_regression" in models

    def test_get_model(self):
        """Test getting model instances."""
        model = self.registry.get_model("linear_regression")
        assert isinstance(model, LinearRegressionModel)

        model = self.registry.get_model("logistic_regression", C=0.5)
        assert isinstance(model, LogisticRegressionModel)
        assert model.hyperparameters["C"] == 0.5

    def test_invalid_model_name(self):
        """Test error for invalid model name."""
        with pytest.raises(ValueError, match="Model 'invalid_model' not found"):
            self.registry.get_model("invalid_model")

    def test_is_available(self):
        """Test model availability check."""
        assert self.registry.is_available("linear_regression")
        assert self.registry.is_available("logistic_regression")
        assert not self.registry.is_available("invalid_model")
