"""
Script to run the BTCL revitalization simulation
"""

import os
from pathlib import Path
from btcl_simulation.simulation import BTCLSimulation
from btcl_simulation.visualization import SimulationVisualizer


def main():
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Set up paths
    config_path = project_root / 'btcl_simulation' / 'data' / 'config.yaml'
    output_dir = project_root / 'results'
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize and run simulation
    print("Initializing BTCL revitalization simulation...")
    simulation = BTCLSimulation(str(config_path))
    
    print("Running simulation...")
    results = simulation.run_simulation()
    
    print("Saving results...")
    simulation.save_results(str(output_dir))
    
    # Create visualizations
    print("Creating visualizations...")
    visualizer = SimulationVisualizer(results)
    visualizer.create_all_visualizations(str(output_dir / 'plots'))
    
    # Print summary
    print("\nSimulation Summary:")
    summary = simulation.get_summary()
    
    print("\nMarket Position Changes:")
    for metric, value in summary['market_position'].items():
        print(f"{metric}: {value:.2%}")
    
    print("\nFinancial Performance:")
    for metric, value in summary['financial'].items():
        print(f"{metric}: {value:.2%}")
    
    print("\nInfrastructure Modernization:")
    for metric, value in summary['infrastructure'].items():
        if metric == 'total_infrastructure_cost':
            print(f"{metric}: {value:,.0f} Tk")
        else:
            print(f"{metric}: {value:.2%}")
    
    print("\nOrganizational Transformation:")
    for metric, value in summary['organizational'].items():
        if metric == 'total_transformation_cost':
            print(f"{metric}: {value:,.0f} Tk")
        else:
            print(f"{metric}: {value:.2%}")
    
    print(f"\nDetailed results saved to: {output_dir}")
    print(f"Visualizations saved to: {output_dir / 'plots'}")


if __name__ == "__main__":
    main() 