"""
Database ORM models for evaluation runs, run details, and scenario parameters.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, BigInteger, JSON, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class EvaluationRun(Base):
    """ORM model for evaluation_runs table."""
    
    __tablename__ = 'evaluation_runs'
    
    run_id = Column(String(36), primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    portfolio_id = Column(String(255), nullable=True)
    scenario_id = Column(String(255), nullable=True)
    base_portfolio_value = Column(Numeric(18, 2), nullable=True)
    adjusted_portfolio_value = Column(Numeric(18, 2), nullable=True)
    value_change = Column(Numeric(18, 2), nullable=True)
    value_change_percent = Column(Numeric(10, 4), nullable=True)
    base_currency = Column(String(3), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    details = relationship("EvaluationRunDetail", back_populates="run", cascade="all, delete-orphan")
    scenario_params = relationship("ScenarioParameter", back_populates="run", uselist=False, cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_timestamp', 'timestamp'),
        Index('idx_portfolio_id', 'portfolio_id'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            'run_id': self.run_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'portfolio_id': self.portfolio_id,
            'scenario_id': self.scenario_id,
            'base_portfolio_value': str(self.base_portfolio_value) if self.base_portfolio_value else None,
            'adjusted_portfolio_value': str(self.adjusted_portfolio_value) if self.adjusted_portfolio_value else None,
            'value_change': str(self.value_change) if self.value_change else None,
            'value_change_percent': str(self.value_change_percent) if self.value_change_percent else None,
            'base_currency': self.base_currency,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class EvaluationRunDetail(Base):
    """ORM model for evaluation_run_details table."""
    
    __tablename__ = 'evaluation_run_details'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    run_id = Column(String(36), ForeignKey('evaluation_runs.run_id', ondelete='CASCADE'), nullable=False)
    asset_id = Column(String(255), nullable=False)
    currency = Column(String(3), nullable=False)
    base_value = Column(Numeric(18, 2), nullable=True)
    adjusted_value = Column(Numeric(18, 2), nullable=True)
    value_change = Column(Numeric(18, 2), nullable=True)
    value_change_percent = Column(Numeric(10, 4), nullable=True)
    fx_impact = Column(Numeric(18, 2), nullable=True)
    market_impact = Column(Numeric(18, 2), nullable=True)
    volatility_impact = Column(Numeric(18, 2), nullable=True)
    
    # Relationships
    run = relationship("EvaluationRun", back_populates="details")
    
    # Indexes
    __table_args__ = (
        Index('idx_run_id', 'run_id'),
        Index('idx_asset_id', 'asset_id'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'run_id': self.run_id,
            'asset_id': self.asset_id,
            'currency': self.currency,
            'base_value': str(self.base_value) if self.base_value else None,
            'adjusted_value': str(self.adjusted_value) if self.adjusted_value else None,
            'value_change': str(self.value_change) if self.value_change else None,
            'value_change_percent': str(self.value_change_percent) if self.value_change_percent else None,
            'fx_impact': str(self.fx_impact) if self.fx_impact else None,
            'market_impact': str(self.market_impact) if self.market_impact else None,
            'volatility_impact': str(self.volatility_impact) if self.volatility_impact else None
        }


class ScenarioParameter(Base):
    """ORM model for scenario_parameters table."""
    
    __tablename__ = 'scenario_parameters'
    
    run_id = Column(String(36), ForeignKey('evaluation_runs.run_id', ondelete='CASCADE'), primary_key=True)
    market_movement_bps = Column(Numeric(10, 2), nullable=True)
    volatility_change_bps = Column(Numeric(10, 2), nullable=True)
    interest_rate_change_bps = Column(Numeric(10, 2), nullable=True)
    currency_rate_changes = Column(JSON, nullable=True)  # JSONB for PostgreSQL
    
    # Relationships
    run = relationship("EvaluationRun", back_populates="scenario_params")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            'run_id': self.run_id,
            'market_movement_bps': str(self.market_movement_bps) if self.market_movement_bps else None,
            'volatility_change_bps': str(self.volatility_change_bps) if self.volatility_change_bps else None,
            'interest_rate_change_bps': str(self.interest_rate_change_bps) if self.interest_rate_change_bps else None,
            'currency_rate_changes': self.currency_rate_changes
        }

