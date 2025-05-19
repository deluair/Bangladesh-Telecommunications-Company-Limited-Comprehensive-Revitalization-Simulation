"""
Organizational model for BTCL simulation
"""

from typing import Dict, Any
import numpy as np
import pandas as pd
from .base import BaseModel


class OrganizationalModel(BaseModel):
    """Model for simulating BTCL's organizational transformation"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the organizational model
        
        Args:
            config: Configuration dictionary containing organizational parameters
        """
        super().__init__(config)
        self.validate_config()
        
        # Initialize organizational parameters
        self.employee_base = config.get('employee_base', 8500)  # Base number of employees
        self.avg_age_base = config.get('avg_age_base', 48)  # Base average age
        self.digital_skills_base = config.get('digital_skills_base', 0.15)  # Base digital skills ratio
        self.operational_efficiency_base = config.get('operational_efficiency_base', 0.30)  # Base operational efficiency
        
        # Transformation parameters
        self.vrs_rate = config.get('vrs_rate', 0.15)  # Annual voluntary retirement rate
        self.new_hiring_rate = config.get('new_hiring_rate', 0.10)  # Annual new hiring rate
        self.digital_skills_growth = config.get('digital_skills_growth', 0.20)  # Annual digital skills growth
        self.operational_efficiency_growth = config.get('operational_efficiency_growth', 0.15)  # Annual efficiency growth
        
        # Cost parameters
        self.avg_salary = config.get('avg_salary', 50000)  # Average monthly salary (Tk)
        self.vrs_package = config.get('vrs_package', 24)  # VRS package in months
        self.training_cost = config.get('training_cost', 50000)  # Annual training cost per employee (Tk)
        
    def validate_config(self) -> bool:
        """
        Validate the model configuration
        
        Returns:
            True if configuration is valid, False otherwise
        """
        required_params = [
            'employee_base',
            'avg_age_base',
            'digital_skills_base',
            'operational_efficiency_base',
            'vrs_rate',
            'new_hiring_rate',
            'digital_skills_growth',
            'operational_efficiency_growth',
            'avg_salary',
            'vrs_package',
            'training_cost'
        ]
        
        for param in required_params:
            if param not in self.config:
                raise ValueError(f"Missing required parameter: {param}")
        
        return True
    
    def simulate(self, time_periods: int) -> Dict[str, Any]:
        """
        Run the organizational simulation
        
        Args:
            time_periods: Number of years to simulate
            
        Returns:
            Dictionary containing simulation results
        """
        # Initialize results arrays
        years = np.arange(time_periods)
        employees = np.zeros(time_periods)
        avg_age = np.zeros(time_periods)
        digital_skills = np.zeros(time_periods)
        operational_efficiency = np.zeros(time_periods)
        vrs_cost = np.zeros(time_periods)
        training_cost = np.zeros(time_periods)
        salary_cost = np.zeros(time_periods)
        
        # Set initial values
        employees[0] = self.employee_base
        avg_age[0] = self.avg_age_base
        digital_skills[0] = self.digital_skills_base
        operational_efficiency[0] = self.operational_efficiency_base
        salary_cost[0] = employees[0] * self.avg_salary * 12
        
        # Simulate organizational transformation
        for t in range(1, time_periods):
            # Workforce changes
            vrs_employees = int(employees[t-1] * self.vrs_rate)
            new_employees = int(employees[t-1] * self.new_hiring_rate)
            employees[t] = employees[t-1] - vrs_employees + new_employees
            
            # Age changes
            avg_age[t] = (avg_age[t-1] * (employees[t-1] - vrs_employees) + 30 * new_employees) / employees[t]
            
            # Skills and efficiency
            digital_skills[t] = min(1.0, digital_skills[t-1] * (1 + self.digital_skills_growth))
            operational_efficiency[t] = min(1.0, operational_efficiency[t-1] * (1 + self.operational_efficiency_growth))
            
            # Cost calculations
            vrs_cost[t] = vrs_employees * self.avg_salary * self.vrs_package
            training_cost[t] = employees[t] * self.training_cost
            salary_cost[t] = employees[t] * self.avg_salary * 12
        
        # Store results
        self.results = {
            'year': years,
            'employees': employees,
            'avg_age': avg_age,
            'digital_skills': digital_skills,
            'operational_efficiency': operational_efficiency,
            'vrs_cost': vrs_cost,
            'training_cost': training_cost,
            'salary_cost': salary_cost
        }
        
        return self.results
    
    def get_organizational_summary(self) -> Dict[str, float]:
        """
        Get summary of organizational transformation
        
        Returns:
            Dictionary containing organizational summary
        """
        if not self.results:
            raise ValueError("Run simulation first")
            
        return {
            'workforce_reduction': (self.results['employees'][-1] - self.results['employees'][0]) / self.results['employees'][0],
            'avg_age_reduction': (self.results['avg_age'][-1] - self.results['avg_age'][0]) / self.results['avg_age'][0],
            'digital_skills_growth': (self.results['digital_skills'][-1] - self.results['digital_skills'][0]) / self.results['digital_skills'][0],
            'operational_efficiency_growth': (self.results['operational_efficiency'][-1] - self.results['operational_efficiency'][0]) / self.results['operational_efficiency'][0],
            'total_transformation_cost': np.sum(self.results['vrs_cost']) + np.sum(self.results['training_cost'])
        } 