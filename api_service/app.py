"""
Flask/FastAPI application setup and configuration.
"""

from flask import Flask
from flask_cors import CORS
from api_service.config import Config
from api_service.routes import register_routes
from api_service.database import init_db


def create_app(config_class=Config) -> Flask:
    """
    Create and configure Flask application.
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    init_db(app)
    
    # Register routes
    register_routes(app)
    
    return app


def run_app(host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
    """
    Run the Flask application.
    
    Args:
        host: Host to bind to
        port: Port to bind to
        debug: Enable debug mode
    """
    app = create_app()
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_app(debug=True)

