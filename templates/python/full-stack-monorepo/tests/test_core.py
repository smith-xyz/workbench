"""
Tests for core business logic.
"""

from core import Engine, Processor
from core.processor import DataItem, ProcessingBatch, ProcessorConfig


class TestEngine:
    """Test the core engine."""

    def test_engine_initialization(self):
        """Test engine can be initialized."""
        engine = Engine()
        assert engine is not None
        assert engine.config == {}

    def test_engine_with_config(self):
        """Test engine initialization with config."""
        config = {"test": "value"}
        engine = Engine(config)
        assert engine.config == config

    def test_process_success(self):
        """Test successful data processing."""
        engine = Engine()
        input_data = {"id": "test-1", "data": "sample"}

        result = engine.process(input_data)

        assert result.id == "test-1"
        assert result.status == "completed"
        assert result.data is not None
        assert len(result.errors) == 0

    def test_process_with_missing_id(self):
        """Test processing with missing ID."""
        engine = Engine()
        input_data = {"data": "sample"}

        result = engine.process(input_data)

        assert result.id == "default"
        assert result.status == "completed"

    def test_get_status(self):
        """Test engine status."""
        engine = Engine()
        status = engine.get_status()

        assert "status" in status
        assert "config" in status
        assert "version" in status
        assert status["status"] == "running"


class TestProcessor:
    """Test the data processor."""

    def test_processor_initialization(self):
        """Test processor can be initialized."""
        processor = Processor()
        assert processor is not None
        assert processor.config.batch_size == 100

    def test_processor_with_config(self):
        """Test processor with custom config."""
        config = ProcessorConfig(batch_size=50, timeout=60)
        processor = Processor(config)
        assert processor.config.batch_size == 50
        assert processor.config.timeout == 60

    def test_process_batch_success(self):
        """Test successful batch processing."""
        processor = Processor()

        items = [
            DataItem(id="item-1", data={"value": 1}),
            DataItem(id="item-2", data={"value": 2}),
        ]

        batch = ProcessingBatch(
            batch_id="test-batch", items=items, config=ProcessorConfig()
        )

        result = processor.process_batch(batch)

        assert result["batch_id"] == "test-batch"
        assert result["total_items"] == 2
        assert result["successful"] == 2
        assert result["failed"] == 0
        assert len(result["results"]) == 2

    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        processor = Processor()
        valid_data = {"id": "test", "data": {"key": "value"}}

        assert processor.validate_data(valid_data) is True

    def test_validate_data_invalid(self):
        """Test data validation with invalid data."""
        processor = Processor()
        invalid_data = {"missing_id": "test"}

        assert processor.validate_data(invalid_data) is False

    def test_get_stats(self):
        """Test processor statistics."""
        processor = Processor()
        stats = processor.get_stats()

        assert "processor_type" in stats
        assert "config" in stats
        assert "status" in stats
        assert stats["status"] == "ready"
