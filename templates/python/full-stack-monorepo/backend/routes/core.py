"""
Core API routes.

Routes for core business logic operations.
"""

from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from core import Engine, Processor
from core.processor import DataItem, ProcessingBatch, ProcessorConfig

router = APIRouter()

# Initialize core components
engine = Engine()
processor = Processor()


@router.get("/status")
async def get_status():
    """Get system status."""
    return {"engine": engine.get_status(), "processor": processor.get_stats()}


@router.post("/process")
async def process_data(data: Dict[str, Any]):
    """Process data using the core engine."""
    try:
        result = engine.process(data)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch")
async def process_batch(batch_data: Dict[str, Any]):
    """Process a batch of data items."""
    try:
        # Convert input to proper models
        config = ProcessorConfig(**batch_data.get("config", {}))
        items = [DataItem(**item_data) for item_data in batch_data.get("items", [])]

        batch = ProcessingBatch(
            batch_id=batch_data.get("batch_id", "default"), items=items, config=config
        )

        result = processor.process_batch(batch)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate")
async def validate_data(data: Dict[str, Any]):
    """Validate input data."""
    is_valid = processor.validate_data(data)
    return {"valid": is_valid, "data": data}
