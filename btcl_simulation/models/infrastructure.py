"""
Infrastructure model for BTCL simulation
"""

from typing import Dict, Any
import numpy as np
import pandas as pd
from .base import BaseModel


class InfrastructureModel(BaseModel):
    """Model for simulating BTCL's infrastructure modernization"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the infrastructure model
        
        Args:
            config: Configuration dictionary containing infrastructure parameters
        """
        super().__init__(config)
        self.validate_config()
        
        # Initialize infrastructure parameters
        self.copper_network_base = config.get('copper_network_base', 1000000)  # Base copper network length (km)
        self.fiber_network_base = config.get('fiber_network_base', 5000)  # Base fiber network length (km)
        self.dsl_ports_base = config.get('dsl_ports_base', 200000)  # Base DSL ports
        self.ftth_ports_base = config.get('ftth_ports_base', 50000)  # Base FTTH ports
        self.data_center_capacity_base = config.get('data_center_capacity_base', 100)  # Base data center capacity (racks)
        
        # Modernization parameters
        self.copper_to_fiber_conversion = config.get('copper_to_fiber_conversion', 0.15)  # Annual conversion rate
        self.dsl_to_ftth_conversion = config.get('dsl_to_ftth_conversion', 0.20)  # Annual conversion rate
        self.data_center_expansion = config.get('data_center_expansion', 0.25)  # Annual expansion rate
        self.network_automation = config.get('network_automation', 0.10)  # Annual automation rate
        
        # Cost parameters
        self.fiber_deployment_cost = config.get('fiber_deployment_cost', 500000)  # Cost per km (Tk)
        self.ftth_port_cost = config.get('ftth_port_cost', 5000)  # Cost per port (Tk)
        self.data_center_rack_cost = config.get('data_center_rack_cost', 1000000)  # Cost per rack (Tk)
        
    def validate_config(self) -> bool:
        """
        Validate the model configuration
        
        Returns:
            True if configuration is valid, False otherwise
        """
        required_params = [
            'copper_network_base',
            'fiber_network_base',
            'dsl_ports_base',
            'ftth_ports_base',
            'data_center_capacity_base',
            'copper_to_fiber_conversion',
            'dsl_to_ftth_conversion',
            'data_center_expansion',
            'network_automation',
            'fiber_deployment_cost',
            'ftth_port_cost',
            'data_center_rack_cost'
        ]
        
        for param in required_params:
            if param not in self.config:
                raise ValueError(f"Missing required parameter: {param}")
        
        return True
    
    def simulate(self, time_periods: int) -> Dict[str, Any]:
        """
        Run the infrastructure simulation
        
        Args:
            time_periods: Number of years to simulate
            
        Returns:
            Dictionary containing simulation results
        """
        # Initialize results arrays
        years = np.arange(time_periods)
        copper_network = np.zeros(time_periods)
        fiber_network = np.zeros(time_periods)
        dsl_ports = np.zeros(time_periods)
        ftth_ports = np.zeros(time_periods)
        data_center_capacity = np.zeros(time_periods)
        infrastructure_cost = np.zeros(time_periods)
        network_automation_level = np.zeros(time_periods)
        
        # Set initial values
        copper_network[0] = self.copper_network_base
        fiber_network[0] = self.fiber_network_base
        dsl_ports[0] = self.dsl_ports_base
        ftth_ports[0] = self.ftth_ports_base
        data_center_capacity[0] = self.data_center_capacity_base
        network_automation_level[0] = 0.0
        
        # Simulate infrastructure modernization
        for t in range(1, time_periods):
            # Network modernization
            copper_to_fiber = copper_network[t-1] * self.copper_to_fiber_conversion
            copper_network[t] = copper_network[t-1] - copper_to_fiber
            fiber_network[t] = fiber_network[t-1] + copper_to_fiber
            
            # Port modernization
            dsl_to_ftth = dsl_ports[t-1] * self.dsl_to_ftth_conversion
            dsl_ports[t] = dsl_ports[t-1] - dsl_to_ftth
            ftth_ports[t] = ftth_ports[t-1] + dsl_to_ftth
            
            # Data center expansion
            data_center_capacity[t] = data_center_capacity[t-1] * (1 + self.data_center_expansion)
            
            # Network automation
            network_automation_level[t] = min(1.0, network_automation_level[t-1] + self.network_automation)
            
            # Calculate infrastructure costs
            infrastructure_cost[t] = (
                copper_to_fiber * self.fiber_deployment_cost +
                dsl_to_ftth * self.ftth_port_cost +
                (data_center_capacity[t] - data_center_capacity[t-1]) * self.data_center_rack_cost
            )
        
        # Store results
        self.results = {
            'year': years,
            'copper_network': copper_network,
            'fiber_network': fiber_network,
            'dsl_ports': dsl_ports,
            'ftth_ports': ftth_ports,
            'data_center_capacity': data_center_capacity,
            'infrastructure_cost': infrastructure_cost,
            'network_automation_level': network_automation_level
        }
        
        return self.results
    
    def get_infrastructure_summary(self) -> Dict[str, float]:
        """
        Get summary of infrastructure modernization
        
        Returns:
            Dictionary containing infrastructure summary
        """
        if not self.results:
            raise ValueError("Run simulation first")
            
        return {
            'fiber_network_growth': (self.results['fiber_network'][-1] - self.results['fiber_network'][0]) / self.results['fiber_network'][0],
            'ftth_port_growth': (self.results['ftth_ports'][-1] - self.results['ftth_ports'][0]) / self.results['ftth_ports'][0],
            'data_center_growth': (self.results['data_center_capacity'][-1] - self.results['data_center_capacity'][0]) / self.results['data_center_capacity'][0],
            'total_infrastructure_cost': np.sum(self.results['infrastructure_cost']),
            'network_automation_achieved': self.results['network_automation_level'][-1]
        } 