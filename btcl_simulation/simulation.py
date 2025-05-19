"""
Main simulation runner for BTCL revitalization simulation
"""

import yaml
from typing import Dict, Any
import pandas as pd
import numpy as np
from pathlib import Path

from .models.market_position import MarketPositionModel
from .models.financial import FinancialModel
from .models.infrastructure import InfrastructureModel
from .models.organizational import OrganizationalModel


class BTCLSimulation:
    """Main simulation class for BTCL revitalization"""
    
    def __init__(self, config_path: str):
        """
        Initialize the simulation
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.models = self._initialize_models()
        self.results = {}
        
        # Initialize model attributes for easier access
        self.market_model = self.models['market_position']
        self.financial_model = self.models['financial']
        self.infrastructure_model = self.models['infrastructure']
        self.organizational_model = self.models['organizational']
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from file
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Dictionary containing configuration
        """
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _initialize_models(self) -> Dict[str, Any]:
        """
        Initialize simulation models
        
        Returns:
            Dictionary containing initialized models
        """
        return {
            'market_position': MarketPositionModel(self.config['market_position']),
            'financial': FinancialModel(self.config['financial']),
            'infrastructure': InfrastructureModel(self.config['infrastructure']),
            'organizational': OrganizationalModel(self.config['organizational'])
        }
    
    def run_simulation(self) -> Dict[str, Any]:
        """
        Run the complete simulation
        
        Returns:
            Dictionary containing simulation results
        """
        time_periods = self.config['simulation'].get('time_periods', self.config['simulation'].get('years', 5))
        
        # Run individual model simulations
        for model_name, model in self.models.items():
            self.results[model_name] = model.simulate(time_periods)
        
        # Combine results
        self._combine_results()
        
        return self.results
    
    # Alias run_simulation as run for convenience
    run = run_simulation
    
    def _combine_results(self) -> None:
        """Combine results from all models into a comprehensive view"""
        # Create a DataFrame with all results
        years = self.results['market_position']['year']
        
        combined_data = {
            'year': years,
            # Market position metrics
            'fixed_line_subscribers': self.results['market_position']['fixed_line_subscribers'],
            'broadband_market_share': self.results['market_position']['broadband_market_share'],
            'mobile_market_share': self.results['market_position']['mobile_market_share'],
            'enterprise_market_share': self.results['market_position']['enterprise_market_share'],
            
            # Financial metrics
            'revenue': self.results['financial']['revenue'],
            'ebitda': self.results['financial']['ebitda'],
            'net_income': self.results['financial']['net_income'],
            'debt': self.results['financial']['debt'],
            
            # Infrastructure metrics
            'fiber_network': self.results['infrastructure']['fiber_network'],
            'ftth_ports': self.results['infrastructure']['ftth_ports'],
            'data_center_capacity': self.results['infrastructure']['data_center_capacity'],
            'infrastructure_cost': self.results['infrastructure']['infrastructure_cost'],
            
            # Organizational metrics
            'employees': self.results['organizational']['employees'],
            'avg_age': self.results['organizational']['avg_age'],
            'digital_skills': self.results['organizational']['digital_skills'],
            'operational_efficiency': self.results['organizational']['operational_efficiency']
        }
        
        self.results['combined'] = pd.DataFrame(combined_data)
    
    def get_summary(self) -> Dict[str, Dict[str, float]]:
        """
        Get summary of simulation results
        
        Returns:
            Dictionary containing summary metrics
        """
        return {
            'market_position': self.models['market_position'].get_market_summary(),
            'financial': self.models['financial'].get_financial_summary(),
            'infrastructure': self.models['infrastructure'].get_infrastructure_summary(),
            'organizational': self.models['organizational'].get_organizational_summary()
        }
    
    def save_results(self, output_dir: str) -> None:
        """
        Save simulation results to files
        
        Args:
            output_dir: Directory to save results
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save combined results
        self.results['combined'].to_csv(output_path / 'combined_results.csv', index=False)
        
        # Save individual model results
        for model_name, results in self.results.items():
            if model_name != 'combined':
                pd.DataFrame(results).to_csv(output_path / f'{model_name}.csv', index=False)
        
        # Save summary
        summary = self.get_summary()
        with open(output_path / 'simulation_summary.yaml', 'w') as f:
            yaml.dump(summary, f, default_flow_style=False)
        # Save human-readable summary as summary.txt
        with open(output_path / 'summary.txt', 'w') as f:
            for section, metrics in summary.items():
                f.write(f"[{section.capitalize()}]\n")
                for key, value in metrics.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n") 