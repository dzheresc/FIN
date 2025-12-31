"""
Command-line interface for batch processing.
"""

import argparse
import sys
from pathlib import Path
from batch_processor.processor import BatchProcessor
from batch_processor.logger import configure_logging, get_logger

logger = get_logger(__name__)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Financial Risk Evaluation System - Batch Processor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m batch_processor --portfolio portfolio.json --scenarios scenarios.json --output results.csv
  python -m batch_processor --portfolio portfolio.json --scenarios scenarios.json --output results.csv --base-currency EUR
        """
    )
    
    parser.add_argument(
        '--portfolio',
        type=Path,
        required=True,
        help='Path to portfolio JSON file'
    )
    
    parser.add_argument(
        '--scenarios',
        type=Path,
        required=True,
        help='Path to scenarios JSON file'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        required=True,
        help='Path to output CSV file'
    )
    
    parser.add_argument(
        '--base-currency',
        type=str,
        default='USD',
        help='Base currency for calculations (default: USD)'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--log-file',
        type=Path,
        help='Optional log file path'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = getattr(__import__('logging'), args.log_level)
    configure_logging(
        level=log_level,
        log_file=str(args.log_file) if args.log_file else None
    )
    
    # Validate input files
    if not args.portfolio.exists():
        logger.error(f"Portfolio file not found: {args.portfolio}")
        sys.exit(1)
    
    if not args.scenarios.exists():
        logger.error(f"Scenarios file not found: {args.scenarios}")
        sys.exit(1)
    
    # Create output directory if needed
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Initialize processor
        processor = BatchProcessor(base_currency=args.base_currency)
        
        # Process
        run_id = processor.process(
            portfolio_file=args.portfolio,
            scenarios_file=args.scenarios,
            output_file=args.output
        )
        
        logger.info(f"Processing completed successfully. Run ID: {run_id}")
        logger.info(f"Results written to: {args.output}")
        print(f"Success! Run ID: {run_id}")
        print(f"Results: {args.output}")
        
    except Exception as e:
        logger.error(f"Processing failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

