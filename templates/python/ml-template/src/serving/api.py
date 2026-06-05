"""FastAPI application for model serving."""

from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel as PydanticBaseModel

from ..models.base import BaseModel
from ..models.registry import ModelRegistry


class PredictionRequest(PydanticBaseModel):
    """Request model for predictions."""

    features: list[list[float]]
    feature_names: list[str] = None


class PredictionResponse(PydanticBaseModel):
    """Response model for predictions."""

    predictions: list[float]
    model_info: dict[str, str]


class HealthResponse(PydanticBaseModel):
    """Response model for health check."""

    status: str
    model_loaded: bool
    model_type: str = None


def create_app(model_path: str | Path = None) -> FastAPI:
    """Create FastAPI application for model serving.

    Args:
        model_path: Path to the saved model file.

    Returns:
        FastAPI application instance.
    """
    app = FastAPI(
        title="ML Model API",
        description="API for serving machine learning models",
        version="1.0.0",
    )

    # Global model storage
    loaded_model: BaseModel = None
    model_info: dict[str, str] = {}

    @app.on_event("startup")
    async def load_model():
        """Load model on startup if path is provided."""
        nonlocal loaded_model, model_info

        if model_path:
            try:
                # For now, we'll implement a simple loading mechanism
                # In a real scenario, you'd need to know the model type to load it properly
                model_info = {
                    "model_path": str(model_path),
                    "status": "loaded",
                    "type": "unknown",  # Would be determined from saved metadata
                }

                # This is a placeholder - in reality, you'd load the actual model
                # loaded_model = SomeModelClass.load(model_path)

            except Exception as e:
                model_info = {
                    "model_path": str(model_path),
                    "status": "failed",
                    "error": str(e),
                }

    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Check API health and model status."""
        return HealthResponse(
            status="healthy",
            model_loaded=loaded_model is not None,
            model_type=model_info.get("type", "unknown") if loaded_model else None,
        )

    @app.post("/predict", response_model=PredictionResponse)
    async def predict(request: PredictionRequest):
        """Make predictions using the loaded model.

        Args:
            request: Prediction request with features.

        Returns:
            Prediction response with results.
        """
        if loaded_model is None:
            raise HTTPException(
                status_code=503, detail="No model loaded. Please load a model first."
            )

        try:
            # Convert features to appropriate format
            if request.feature_names:
                # Create DataFrame with feature names
                df = pd.DataFrame(request.features, columns=request.feature_names)
                predictions = loaded_model.predict(df)
            else:
                # Use numpy array
                X = np.array(request.features)
                predictions = loaded_model.predict(X)

            # Ensure predictions is a list
            if isinstance(predictions, np.ndarray):
                predictions = predictions.tolist()
            elif not isinstance(predictions, list):
                predictions = [predictions]

            return PredictionResponse(predictions=predictions, model_info=model_info)

        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Prediction failed: {str(e)}"
            ) from e

    @app.post("/load_model")
    async def load_model_endpoint(model_name: str, model_path: str = None):
        """Load a model by name or from path.

        Args:
            model_name: Name of the model type to load.
            model_path: Optional path to saved model file.

        Returns:
            Success message.
        """
        nonlocal loaded_model, model_info

        try:
            registry = ModelRegistry()

            if model_path:
                # Load from file (would need proper implementation)
                model_class = registry.get_model_class(model_name)
                loaded_model = model_class.load(Path(model_path))
                model_info = {
                    "type": model_name,
                    "source": "file",
                    "path": model_path,
                    "status": "loaded",
                }
            else:
                # Create new instance
                loaded_model = registry.get_model(model_name)
                model_info = {
                    "type": model_name,
                    "source": "new_instance",
                    "status": "created",
                }

            return {"message": f"Model '{model_name}' loaded successfully"}

        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to load model: {str(e)}"
            ) from e

    @app.get("/models")
    async def list_available_models():
        """List all available model types."""
        registry = ModelRegistry()
        return registry.list_models()

    @app.get("/model/info")
    async def get_model_info():
        """Get information about the currently loaded model."""
        if loaded_model is None:
            raise HTTPException(status_code=404, detail="No model currently loaded")

        info = model_info.copy()
        info["model_class"] = loaded_model.__class__.__name__

        # Add model parameters if available
        if hasattr(loaded_model, "get_params"):
            info["parameters"] = loaded_model.get_params()

        return info

    return app
