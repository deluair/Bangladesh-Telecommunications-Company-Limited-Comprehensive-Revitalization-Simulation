"""
Base model class for BTCL simulation
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import numpy as np
import pandas as pd


class BaseModel(ABC):
    """Base class for all simulation models"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the base model
        
        Args:
            config: Configuration dictionary for the model
        """
        self.config = config
        self.results = {}
        
    @abstractmethod
    def simulate(self, time_periods: int) -> Dict[str, Any]:
        """
        Run the simulation for specified number of time periods
        
        Args:
            time_periods: Number of time periods to simulate
            
        Returns:
            Dictionary containing simulation results
        """
        pass
    
    def validate_config(self) -> bool:
        """
        Validate the model configuration
        
        Returns:
            True if configuration is valid, False otherwise
        """
        return True
    
    def get_results(self) -> Dict[str, Any]:
        """
        Get the simulation results
        
        Returns:
            Dictionary containing simulation results
        """
        return self.results
    
    def save_results(self, filepath: str) -> None:
        """
        Save simulation results to file
        
        Args:
            filepath: Path to save results
        """
        pd.DataFrame(self.results).to_csv(filepath, index=False) 