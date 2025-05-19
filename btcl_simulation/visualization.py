"""
Visualization module for BTCL simulation results
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, Any


class SimulationVisualizer:
    """Class for visualizing BTCL simulation results"""
    
    def __init__(self, results: Dict[str, Any]):
        """
        Initialize the visualizer
        
        Args:
            results: Dictionary containing simulation results
        """
        self.results = results
        
        # Create combined data if not present
        if 'combined' not in results:
            years = results['market_position']['year']
            
            combined_data = {
                'year': years,
                # Market position metrics
                'fixed_line_subscribers': results['market_position']['fixed_line_subscribers'],
                'broadband_market_share': results['market_position']['broadband_market_share'],
                'mobile_market_share': results['market_position']['mobile_market_share'],
                'enterprise_market_share': results['market_position']['enterprise_market_share'],
                
                # Financial metrics
                'revenue': results['financial']['revenue'],
                'ebitda': results['financial']['ebitda'],
                'net_income': results['financial']['net_income'],
                'debt': results['financial']['debt'],
                
                # Infrastructure metrics
                'fiber_network': results['infrastructure']['fiber_network'],
                'ftth_ports': results['infrastructure']['ftth_ports'],
                'data_center_capacity': results['infrastructure']['data_center_capacity'],
                'infrastructure_cost': results['infrastructure']['infrastructure_cost'],
                
                # Organizational metrics
                'employees': results['organizational']['employees'],
                'avg_age': results['organizational']['avg_age'],
                'digital_skills': results['organizational']['digital_skills'],
                'operational_efficiency': results['organizational']['operational_efficiency']
            }
            
            self.combined_data = pd.DataFrame(combined_data)
        else:
            self.combined_data = results['combined']
        
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def plot_market_position(self, output_dir: str) -> None:
        """
        Plot market position metrics
        
        Args:
            output_dir: Directory to save plots
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Market Position Evolution')
        
        # Fixed line subscribers
        axes[0, 0].plot(self.combined_data['year'], self.combined_data['fixed_line_subscribers'])
        axes[0, 0].set_title('Fixed Line Subscribers')
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Subscribers')
        
        # Market shares
        axes[0, 1].plot(self.combined_data['year'], self.combined_data['broadband_market_share'], label='Broadband')
        axes[0, 1].plot(self.combined_data['year'], self.combined_data['mobile_market_share'], label='Mobile')
        axes[0, 1].plot(self.combined_data['year'], self.combined_data['enterprise_market_share'], label='Enterprise')
        axes[0, 1].set_title('Market Shares')
        axes[0, 1].set_xlabel('Year')
        axes[0, 1].set_ylabel('Market Share')
        axes[0, 1].legend()
        
        # Growth rates
        growth_rates = pd.DataFrame({
            'Broadband': self.combined_data['broadband_market_share'].pct_change(),
            'Mobile': self.combined_data['mobile_market_share'].pct_change(),
            'Enterprise': self.combined_data['enterprise_market_share'].pct_change()
        })
        growth_rates.plot(ax=axes[1, 0])
        axes[1, 0].set_title('Market Share Growth Rates')
        axes[1, 0].set_xlabel('Year')
        axes[1, 0].set_ylabel('Growth Rate')
        
        # Market share composition
        market_shares = self.combined_data[['broadband_market_share', 'mobile_market_share', 'enterprise_market_share']]
        market_shares.plot(kind='area', stacked=True, ax=axes[1, 1])
        axes[1, 1].set_title('Market Share Composition')
        axes[1, 1].set_xlabel('Year')
        axes[1, 1].set_ylabel('Market Share')
        
        plt.tight_layout()
        plt.savefig(Path(output_dir) / 'market_position.png')
        plt.close(fig)
        # Save market share composition separately as expected by tests
        plt.figure(figsize=(8, 6))
        market_shares.plot(kind='area', stacked=True)
        plt.title('Market Share Composition')
        plt.xlabel('Year')
        plt.ylabel('Market Share')
        plt.tight_layout()
        plt.savefig(Path(output_dir) / 'market_share_composition.png')
        plt.close()
    
    def plot_financial_metrics(self, output_dir: str) -> None:
        """
        Plot financial metrics
        
        Args:
            output_dir: Directory to save plots
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Financial Performance')
        
        # Revenue and EBITDA
        axes[0, 0].plot(self.combined_data['year'], self.combined_data['revenue'], label='Revenue')
        axes[0, 0].plot(self.combined_data['year'], self.combined_data['ebitda'], label='EBITDA')
        axes[0, 0].set_title('Revenue and EBITDA')
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Amount (Crore Tk)')
        axes[0, 0].legend()
        
        # Net Income
        axes[0, 1].plot(self.combined_data['year'], self.combined_data['net_income'])
        axes[0, 1].set_title('Net Income')
        axes[0, 1].set_xlabel('Year')
        axes[0, 1].set_ylabel('Amount (Crore Tk)')
        
        # Debt
        axes[1, 0].plot(self.combined_data['year'], self.combined_data['debt'])
        axes[1, 0].set_title('Debt')
        axes[1, 0].set_xlabel('Year')
        axes[1, 0].set_ylabel('Amount (Crore Tk)')
        
        # Financial ratios
        ebitda_margin = self.combined_data['ebitda'] / self.combined_data['revenue']
        debt_to_revenue = self.combined_data['debt'] / self.combined_data['revenue']
        ax2 = axes[1, 1].twinx()
        axes[1, 1].plot(self.combined_data['year'], ebitda_margin, 'b-', label='EBITDA Margin')
        ax2.plot(self.combined_data['year'], debt_to_revenue, 'r-', label='Debt/Revenue')
        axes[1, 1].set_title('Financial Ratios')
        axes[1, 1].set_xlabel('Year')
        axes[1, 1].set_ylabel('EBITDA Margin', color='b')
        ax2.set_ylabel('Debt/Revenue', color='r')
        
        plt.tight_layout()
        plt.savefig(Path(output_dir) / 'financial_performance.png')
        plt.close(fig)
        # Save financial ratios separately as expected by tests
        plt.figure(figsize=(8, 6))
        plt.plot(self.combined_data['year'], ebitda_margin, 'b-', label='EBITDA Margin')
        plt.plot(self.combined_data['year'], debt_to_revenue, 'r-', label='Debt/Revenue')
        plt.title('Financial Ratios')
        plt.xlabel('Year')
        plt.ylabel('Ratio')
        plt.legend()
        plt.tight_layout()
        plt.savefig(Path(output_dir) / 'financial_ratios.png')
        plt.close()
    
    def plot_infrastructure_metrics(self, output_dir: str) -> None:
        """
        Plot infrastructure metrics
        
        Args:
            output_dir: Directory to save plots
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Infrastructure Modernization')
        
        # Network evolution
        axes[0, 0].plot(self.combined_data['year'], self.combined_data['fiber_network'], label='Fiber')
        axes[0, 0].set_title('Fiber Network Growth')
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Network Length (km)')
        
        # Port evolution
        axes[0, 1].plot(self.combined_data['year'], self.combined_data['ftth_ports'], label='FTTH')
        axes[0, 1].set_title('FTTH Ports')
        axes[0, 1].set_xlabel('Year')
        axes[0, 1].set_ylabel('Number of Ports')
        
        # Data center capacity
        axes[1, 0].plot(self.combined_data['year'], self.combined_data['data_center_capacity'])
        axes[1, 0].set_title('Data Center Capacity')
        axes[1, 0].set_xlabel('Year')
        axes[1, 0].set_ylabel('Capacity (Racks)')
        
        # Infrastructure costs
        axes[1, 1].plot(self.combined_data['year'], self.combined_data['infrastructure_cost'])
        axes[1, 1].set_title('Infrastructure Costs')
        axes[1, 1].set_xlabel('Year')
        axes[1, 1].set_ylabel('Cost (Tk)')
        
        plt.tight_layout()
        plt.savefig(Path(output_dir) / 'infrastructure_growth.png')
        plt.close(fig)
        # Save infrastructure costs separately as expected by tests
        plt.figure(figsize=(8, 6))
        plt.plot(self.combined_data['year'], self.combined_data['infrastructure_cost'])
        plt.title('Infrastructure Costs')
        plt.xlabel('Year')
        plt.ylabel('Cost (Tk)')
        plt.tight_layout()
        plt.savefig(Path(output_dir) / 'infrastructure_costs.png')
        plt.close()
    
    def plot_organizational_metrics(self, output_dir: str) -> None:
        """
        Plot organizational metrics
        
        Args:
            output_dir: Directory to save plots
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Organizational Transformation')
        
        # Workforce evolution
        axes[0, 0].plot(self.combined_data['year'], self.combined_data['employees'])
        axes[0, 0].set_title('Workforce Size')
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Number of Employees')
        
        # Average age
        axes[0, 1].plot(self.combined_data['year'], self.combined_data['avg_age'])
        axes[0, 1].set_title('Average Employee Age')
        axes[0, 1].set_xlabel('Year')
        axes[0, 1].set_ylabel('Age')
        
        # Skills and efficiency
        axes[1, 0].plot(self.combined_data['year'], self.combined_data['digital_skills'], label='Digital Skills')
        axes[1, 0].plot(self.combined_data['year'], self.combined_data['operational_efficiency'], label='Operational Efficiency')
        axes[1, 0].set_title('Skills and Efficiency')
        axes[1, 0].set_xlabel('Year')
        axes[1, 0].set_ylabel('Ratio')
        axes[1, 0].legend()
        
        # Cost per employee
        salary_cost = self.combined_data['salary_cost'] if 'salary_cost' in self.combined_data else 0
        training_cost = self.combined_data['training_cost'] if 'training_cost' in self.combined_data else 0
        cost_per_employee = (salary_cost + training_cost) / self.combined_data['employees']
        axes[1, 1].plot(self.combined_data['year'], cost_per_employee)
        axes[1, 1].set_title('Cost per Employee')
        axes[1, 1].set_xlabel('Year')
        axes[1, 1].set_ylabel('Cost (Tk)')
        
        plt.tight_layout()
        plt.savefig(Path(output_dir) / 'workforce_metrics.png')
        plt.close(fig)
        # Save organizational efficiency separately as expected by tests
        plt.figure(figsize=(8, 6))
        plt.plot(self.combined_data['year'], self.combined_data['operational_efficiency'], label='Operational Efficiency')
        plt.title('Organizational Efficiency')
        plt.xlabel('Year')
        plt.ylabel('Efficiency')
        plt.legend()
        plt.tight_layout()
        plt.savefig(Path(output_dir) / 'organizational_efficiency.png')
        plt.close()
    
    def create_all_visualizations(self, output_dir: str) -> None:
        """
        Create all visualizations
        
        Args:
            output_dir: Directory to save plots
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        self.plot_market_position(str(output_path))
        self.plot_financial_metrics(str(output_path))
        self.plot_infrastructure_metrics(str(output_path))
        self.plot_organizational_metrics(str(output_path)) 