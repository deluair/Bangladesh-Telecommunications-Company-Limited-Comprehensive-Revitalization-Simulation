"""
Market position model for BTCL simulation
"""

from typing import Dict, Any
import numpy as np
import pandas as pd
from .base import BaseModel


class MarketPositionModel(BaseModel):
    """Model for simulating BTCL's market position changes"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the market position model
        
        Args:
            config: Configuration dictionary containing market parameters
        """
        super().__init__(config)
        self.validate_config()
        
        # Initialize market parameters
        self.fixed_line_base = config.get('fixed_line_base', 500000)  # Current fixed line subscribers
        self.broadband_base = config.get('broadband_base', 0.12)  # Current broadband market share
        self.mobile_base = config.get('mobile_base', 0.0)  # Current mobile market share
        self.enterprise_base = config.get('enterprise_base', 0.15)  # Current enterprise market share
        
        # Growth and decline rates
        self.fixed_line_decline = config.get('fixed_line_decline', -0.05)  # Annual decline rate
        self.broadband_growth = config.get('broadband_growth', 0.15)  # Annual growth rate
        self.mobile_growth = config.get('mobile_growth', 0.10)  # Annual growth rate
        self.enterprise_growth = config.get('enterprise_growth', 0.20)  # Annual growth rate
        
    def validate_config(self) -> bool:
        """
        Validate the model configuration
        
        Returns:
            True if configuration is valid, False otherwise
        """
        required_params = [
            'fixed_line_base',
            'broadband_base',
            'mobile_base',
            'enterprise_base',
            'fixed_line_decline',
            'broadband_growth',
            'mobile_growth',
            'enterprise_growth'
        ]
        
        for param in required_params:
            if param not in self.config:
                raise ValueError(f"Missing required parameter: {param}")
        
        return True
    
    def simulate(self, time_periods: int) -> Dict[str, Any]:
        """
        Run the market position simulation
        
        Args:
            time_periods: Number of years to simulate
            
        Returns:
            Dictionary containing simulation results
        """
        # Initialize results arrays
        years = np.arange(time_periods)
        fixed_line = np.zeros(time_periods)
        broadband = np.zeros(time_periods)
        mobile = np.zeros(time_periods)
        enterprise = np.zeros(time_periods)
        
        # Set initial values
        fixed_line[0] = self.fixed_line_base
        broadband[0] = self.broadband_base
        mobile[0] = self.mobile_base
        enterprise[0] = self.enterprise_base
        
        # Simulate market position changes
        for t in range(1, time_periods):
            # Fixed line decline
            fixed_line[t] = fixed_line[t-1] * (1 + self.fixed_line_decline)
            
            # Broadband growth with saturation
            broadband[t] = min(0.4, broadband[t-1] * (1 + self.broadband_growth))
            
            # Mobile growth with saturation
            mobile[t] = min(0.15, mobile[t-1] * (1 + self.mobile_growth))
            
            # Enterprise growth with saturation
            enterprise[t] = min(0.35, enterprise[t-1] * (1 + self.enterprise_growth))
        
        # Store results
        self.results = {
            'year': years,
            'fixed_line_subscribers': fixed_line,
            'broadband_market_share': broadband,
            'mobile_market_share': mobile,
            'enterprise_market_share': enterprise
        }
        
        return self.results
    
    def get_market_summary(self) -> Dict[str, float]:
        """
        Get summary of market position changes
        
        Returns:
            Dictionary containing market position summary
        """
        if not self.results:
            raise ValueError("Run simulation first")
            
        return {
            'fixed_line_change': (self.results['fixed_line_subscribers'][-1] - self.results['fixed_line_subscribers'][0]) / self.results['fixed_line_subscribers'][0],
            'broadband_change': (self.results['broadband_market_share'][-1] - self.results['broadband_market_share'][0]) / self.results['broadband_market_share'][0],
            'mobile_change': (self.results['mobile_market_share'][-1] - self.results['mobile_market_share'][0]) / self.results['mobile_market_share'][0] if self.results['mobile_market_share'][0] > 0 else float('inf'),
            'enterprise_change': (self.results['enterprise_market_share'][-1] - self.results['enterprise_market_share'][0]) / self.results['enterprise_market_share'][0]
        } 