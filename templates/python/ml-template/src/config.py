"""Configuration management for ML pipeline."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class DataConfig(BaseModel):
    """Data-related configuration."""

    raw_data_path: Path = Field(default=Path("data/raw"))
    processed_data_path: Path = Field(default=Path("data/processed"))
    interim_data_path: Path = Field(default=Path("data/interim"))
    train_size: float = Field(default=0.8, ge=0.1, le=0.9)
    val_size: float = Field(default=0.1, ge=0.05, le=0.4)
    test_size: float = Field(default=0.1, ge=0.05, le=0.4)
    random_seed: int = Field(default=42)


class ModelConfig(BaseModel):
    """Model-related configuration."""

    model_type: str = Field(default="linear_regression")
    random_state: int = Field(default=42)
    hyperparameters: dict[str, Any] = Field(default_factory=dict)


class TrainingConfig(BaseModel):
    """Training-related configuration."""

    batch_size: int = Field(default=32, gt=0)
    epochs: int = Field(default=100, gt=0)
    learning_rate: float = Field(default=0.001, gt=0)
    early_stopping_patience: int = Field(default=10, gt=0)
    checkpoint_dir: Path = Field(default=Path("models/checkpoints"))


class ExperimentConfig(BaseModel):
    """Experiment tracking configuration."""

    experiment_name: str = Field(default="default")
    run_name: str | None = None
    tracking_uri: str = Field(default="./mlruns")
    artifact_location: str | None = None


class Settings(BaseSettings):
    """Main application settings."""

    data: DataConfig = Field(default_factory=DataConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    training: TrainingConfig = Field(default_factory=TrainingConfig)
    experiment: ExperimentConfig = Field(default_factory=ExperimentConfig)

    # Environment variables
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


def load_config(config_path: Path | None = None) -> Settings:
    """Load configuration from file and environment variables."""
    if config_path and config_path.exists():
        with open(config_path) as f:
            config_data = yaml.safe_load(f)
        return Settings(**config_data)
    return Settings()


# Global config instance
config = load_config()
