# Examples

This directory contains example scripts demonstrating how to use the Financial Risk Evaluation System.

## Batch Processing Example

`batch_processing_example.py` - Demonstrates the complete batch processing workflow:

1. Loading portfolio from JSON
2. Loading scenarios from JSON
3. Applying scenarios manually (for demonstration)
4. Running full batch processing
5. Reading and displaying results

### Running the Example

From the project root directory:

```bash
python examples/batch_processing_example.py
```

This will:
- Load the sample portfolio and scenarios from `tests/fixtures/`
- Process them using the batch processor
- Generate a CSV file in `output/example_results.csv`
- Display the results

### Prerequisites

- Python 3.9+
- All dependencies installed (`pip install -r requirements.txt`)
- Sample fixture files in `tests/fixtures/`

