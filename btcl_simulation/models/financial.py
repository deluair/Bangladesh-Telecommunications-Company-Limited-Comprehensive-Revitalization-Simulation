"""
Financial model for BTCL simulation
"""

from typing import Dict, Any
import numpy as np
import pandas as pd
from .base import BaseModel


class FinancialModel(BaseModel):
    """Model for simulating BTCL's financial performance"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the financial model
        
        Args:
            config: Configuration dictionary containing financial parameters
        """
        super().__init__(config)
        self.validate_config()
        
        # Initialize financial parameters
        self.revenue_base = config.get('revenue_base', 1000)  # Base revenue in crore Tk
        self.employee_cost_ratio = config.get('employee_cost_ratio', 0.68)  # Employee cost as % of revenue
        self.other_opex_ratio = config.get('other_opex_ratio', 0.25)  # Other opex as % of revenue
        self.capex_ratio = config.get('capex_ratio', 0.15)  # Capex as % of revenue
        self.debt_base = config.get('debt_base', 1500)  # Base debt in crore Tk
        self.interest_rate = config.get('interest_rate', 0.08)  # Interest rate on debt
        
        # Growth and efficiency parameters
        self.revenue_growth = config.get('revenue_growth', -0.06)  # Annual revenue growth
        self.cost_reduction = config.get('cost_reduction', 0.05)  # Annual cost reduction
        self.asset_utilization = config.get('asset_utilization', 0.30)  # Asset utilization ratio
        
    def validate_config(self) -> bool:
        """
        Validate the model configuration
        
        Returns:
            True if configuration is valid, False otherwise
        """
        required_params = [
            'revenue_base',
            'employee_cost_ratio',
            'other_opex_ratio',
            'capex_ratio',
            'debt_base',
            'interest_rate',
            'revenue_growth',
            'cost_reduction',
            'asset_utilization'
        ]
        
        for param in required_params:
            if param not in self.config:
                raise ValueError(f"Missing required parameter: {param}")
        
        return True
    
    def simulate(self, time_periods: int) -> Dict[str, Any]:
        """
        Run the financial simulation
        
        Args:
            time_periods: Number of years to simulate
            
        Returns:
            Dictionary containing simulation results
        """
        # Initialize results arrays
        years = np.arange(time_periods)
        revenue = np.zeros(time_periods)
        employee_cost = np.zeros(time_periods)
        other_opex = np.zeros(time_periods)
        ebitda = np.zeros(time_periods)
        capex = np.zeros(time_periods)
        debt = np.zeros(time_periods)
        interest_expense = np.zeros(time_periods)
        net_income = np.zeros(time_periods)
        
        # Set initial values
        revenue[0] = self.revenue_base
        employee_cost[0] = revenue[0] * self.employee_cost_ratio
        other_opex[0] = revenue[0] * self.other_opex_ratio
        ebitda[0] = revenue[0] - employee_cost[0] - other_opex[0]
        capex[0] = revenue[0] * self.capex_ratio
        debt[0] = self.debt_base
        interest_expense[0] = debt[0] * self.interest_rate
        net_income[0] = ebitda[0] - interest_expense[0] - capex[0]
        
        # Simulate financial performance
        for t in range(1, time_periods):
            # Revenue growth/decline
            revenue[t] = revenue[t-1] * (1 + self.revenue_growth)
            
            # Cost reduction
            employee_cost[t] = revenue[t] * self.employee_cost_ratio * (1 - self.cost_reduction) ** t
            other_opex[t] = revenue[t] * self.other_opex_ratio * (1 - self.cost_reduction) ** t
            
            # EBITDA
            ebitda[t] = revenue[t] - employee_cost[t] - other_opex[t]
            
            # Capex
            capex[t] = revenue[t] * self.capex_ratio
            
            # Debt and interest
            debt[t] = max(0, debt[t-1] - (ebitda[t] - capex[t]))
            interest_expense[t] = debt[t] * self.interest_rate
            
            # Net income
            net_income[t] = ebitda[t] - interest_expense[t] - capex[t]
        
        # Store results
        self.results = {
            'year': years,
            'revenue': revenue,
            'employee_cost': employee_cost,
            'other_opex': other_opex,
            'ebitda': ebitda,
            'capex': capex,
            'debt': debt,
            'interest_expense': interest_expense,
            'net_income': net_income
        }
        
        return self.results
    
    def get_financial_summary(self) -> Dict[str, float]:
        """
        Get summary of financial performance
        
        Returns:
            Dictionary containing financial summary
        """
        if not self.results:
            raise ValueError("Run simulation first")
            
        return {
            'revenue_change': (self.results['revenue'][-1] - self.results['revenue'][0]) / self.results['revenue'][0],
            'ebitda_margin': self.results['ebitda'][-1] / self.results['revenue'][-1],
            'debt_reduction': (self.results['debt'][-1] - self.results['debt'][0]) / self.results['debt'][0],
            'employee_cost_ratio': self.results['employee_cost'][-1] / self.results['revenue'][-1],
            'capex_intensity': self.results['capex'][-1] / self.results['revenue'][-1]
        } 