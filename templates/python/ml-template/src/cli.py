"""Command-line interface for ML operations."""

from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .config import config
from .data.loader import DataLoader
from .evaluation.evaluator import Evaluator
from .models.registry import ModelRegistry
from .serving.api import create_app
from .training.trainer import Trainer

app = typer.Typer(help="ML Template CLI")
console = Console()


@app.command()
def train(
    model: str = typer.Argument(..., help="Model type to train"),
    data_path: Path | None = typer.Option(None, help="Path to training data"),
    config_path: Path | None = typer.Option(None, help="Path to config file"),
    experiment_name: str | None = typer.Option(None, help="MLflow experiment name"),
    run_name: str | None = typer.Option(None, help="MLflow run name"),
    save_model: bool = typer.Option(True, help="Save trained model"),
) -> None:
    """Train a machine learning model."""

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Load data
        progress.add_task("Loading data...", total=None)
        loader = DataLoader()

        if data_path and data_path.exists():
            data = loader.load_csv(data_path)
        else:
            console.print("No data provided, generating sample data...")
            # Determine problem type based on model name
            if model.lower() in ["linear_regression"]:
                problem_type = "regression"
            else:
                problem_type = "classification"
            data = loader.generate_sample_data(problem_type=problem_type)

        # Split data
        progress.add_task("Splitting data...", total=None)
        X_train, X_val, X_test, y_train, y_val, y_test = loader.split_data(data)

        # Initialize model
        progress.add_task("Initializing model...", total=None)
        registry = ModelRegistry()

        # Determine problem type based on model name for ensemble models
        if model in ["random_forest", "xgboost"]:
            problem_type = (
                "regression" if "regression" in model.lower() else "classification"
            )
            model_instance = registry.get_model(model, problem_type=problem_type)
        else:
            model_instance = registry.get_model(model)

        # Train model
        progress.add_task("Training model...", total=None)
        trainer = Trainer(
            experiment_name=experiment_name or config.experiment.experiment_name,
            run_name=run_name,
        )

        trained_model = trainer.train(model_instance, X_train, y_train, X_val, y_val)

        # Evaluate model
        progress.add_task("Evaluating model...", total=None)
        evaluator = Evaluator()
        metrics = evaluator.evaluate(trained_model, X_test, y_test)

        # Display results
        table = Table(title="Training Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")

        for metric_name, value in metrics.items():
            table.add_row(metric_name, f"{value:.4f}")

        console.print(table)

        # Save model
        if save_model:
            model_path = Path("models") / f"{model}_{trainer.run_id}.joblib"
            trained_model.save(model_path)
            console.print(f"Model saved to: {model_path}")


@app.command()
def evaluate(
    model: str = typer.Argument(..., help="Model type to evaluate"),
    model_path: Path | None = typer.Option(None, help="Path to saved model"),
    data_path: Path | None = typer.Option(None, help="Path to test data"),
) -> None:
    """Evaluate a trained model."""

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Load model
        progress.add_task("Loading model...", total=None)
        if model_path and model_path.exists():
            registry = ModelRegistry()
            model_class = registry.get_model_class(model)
            model_instance = model_class.load(model_path)
        else:
            console.print("[red]Model path not provided or doesn't exist[/red]")
            raise typer.Exit(1)

        # Load data
        progress.add_task("Loading test data...", total=None)
        loader = DataLoader()

        if data_path and data_path.exists():
            data = loader.load_csv(data_path)
            X_test = data.drop(columns=["target"])
            y_test = data["target"]
        else:
            console.print("No test data provided, generating sample data...")
            # Determine problem type based on model name
            if model.lower() in ["linear_regression"]:
                problem_type = "regression"
            else:
                problem_type = "classification"
            data = loader.generate_sample_data(problem_type=problem_type)
            _, _, X_test, _, _, y_test = loader.split_data(data)

        # Evaluate
        progress.add_task("Evaluating model...", total=None)
        evaluator = Evaluator()
        metrics = evaluator.evaluate(model_instance, X_test, y_test)

        # Display results
        table = Table(title="Evaluation Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")

        for metric_name, value in metrics.items():
            table.add_row(metric_name, f"{value:.4f}")

        console.print(table)


@app.command()
def serve(
    model: str = typer.Argument(..., help="Model type to serve"),
    model_path: Path | None = typer.Option(None, help="Path to saved model"),
    host: str = typer.Option("0.0.0.0", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
) -> None:
    """Start model serving API."""

    if not model_path or not model_path.exists():
        console.print("[red]Model path not provided or doesn't exist[/red]")
        raise typer.Exit(1)

    console.print(f"Starting API server on {host}:{port}")
    console.print(f"Serving model: {model_path}")

    # This would typically use uvicorn.run() but for the CLI we'll import here
    import uvicorn

    app_instance = create_app(model_path)
    uvicorn.run(app_instance, host=host, port=port)


@app.command()
def hyperopt(
    model: str = typer.Argument(..., help="Model type for hyperparameter optimization"),
    trials: int = typer.Option(50, help="Number of optimization trials"),
    data_path: Path | None = typer.Option(None, help="Path to training data"),
) -> None:
    """Run hyperparameter optimization."""

    console.print(f"Starting hyperparameter optimization for {model}")
    console.print(f"Number of trials: {trials}")

    # This would integrate with Optuna for hyperparameter optimization
    console.print("[yellow]Hyperparameter optimization not yet implemented[/yellow]")


@app.command()
def list_models() -> None:
    """List available model types."""

    registry = ModelRegistry()
    models = registry.list_models()

    table = Table(title="Available Models")
    table.add_column("Model Name", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Description", style="green")

    for model_name, model_info in models.items():
        table.add_row(
            model_name,
            model_info.get("type", "Unknown"),
            model_info.get("description", "No description"),
        )

    console.print(table)


if __name__ == "__main__":
    app()
