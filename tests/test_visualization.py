"""
Tests for BTCL simulation visualization
"""

import pytest
import os
import pandas as pd
import numpy as np
from btcl_simulation.visualization import SimulationVisualizer


@pytest.fixture
def sample_results():
    years = list(range(5))
    return {
        'market_position': pd.DataFrame({
            'year': years,
            'fixed_line_subscribers': [500000, 475000, 451250, 428688, 407253],
            'broadband_market_share': [0.12, 0.138, 0.159, 0.183, 0.210],
            'mobile_market_share': [0.0, 0.10, 0.20, 0.30, 0.40],
            'enterprise_market_share': [0.15, 0.18, 0.216, 0.259, 0.311]
        }),
        'financial': pd.DataFrame({
            'year': years,
            'revenue': [1000, 940, 884, 831, 781],
            'ebitda': [70, 75, 80, 85, 90],
            'net_income': [-30, -25, -20, -15, -10],
            'debt': [1500, 1450, 1400, 1350, 1300]
        }),
        'infrastructure': pd.DataFrame({
            'year': years,
            'fiber_network': [5000, 5750, 6613, 7605, 8746],
            'ftth_ports': [50000, 60000, 72000, 86400, 103680],
            'data_center_capacity': [100, 125, 156, 195, 244],
            'infrastructure_cost': [1000000, 1150000, 1322500, 1520875, 1749006]
        }),
        'organizational': pd.DataFrame({
            'year': years,
            'employees': [8500, 7650, 6885, 6197, 5577],
            'avg_age': [48, 46, 44, 42, 40],
            'digital_skills': [0.15, 0.18, 0.216, 0.259, 0.311],
            'operational_efficiency': [0.30, 0.345, 0.397, 0.456, 0.525]
        })
    }


@pytest.fixture
def output_dir(tmp_path):
    return str(tmp_path / "plots")


def test_visualizer_initialization(sample_results):
    visualizer = SimulationVisualizer(sample_results)
    assert visualizer.results == sample_results


def test_plot_market_position(sample_results, output_dir):
    visualizer = SimulationVisualizer(sample_results)
    os.makedirs(output_dir, exist_ok=True)
    
    visualizer.plot_market_position(output_dir)
    
    assert os.path.exists(os.path.join(output_dir, 'market_position.png'))
    assert os.path.exists(os.path.join(output_dir, 'market_share_composition.png'))


def test_plot_financial_metrics(sample_results, output_dir):
    visualizer = SimulationVisualizer(sample_results)
    os.makedirs(output_dir, exist_ok=True)
    
    visualizer.plot_financial_metrics(output_dir)
    
    assert os.path.exists(os.path.join(output_dir, 'financial_performance.png'))
    assert os.path.exists(os.path.join(output_dir, 'financial_ratios.png'))


def test_plot_infrastructure_metrics(sample_results, output_dir):
    visualizer = SimulationVisualizer(sample_results)
    os.makedirs(output_dir, exist_ok=True)
    
    visualizer.plot_infrastructure_metrics(output_dir)
    
    assert os.path.exists(os.path.join(output_dir, 'infrastructure_growth.png'))
    assert os.path.exists(os.path.join(output_dir, 'infrastructure_costs.png'))


def test_plot_organizational_metrics(sample_results, output_dir):
    visualizer = SimulationVisualizer(sample_results)
    os.makedirs(output_dir, exist_ok=True)
    
    visualizer.plot_organizational_metrics(output_dir)
    
    assert os.path.exists(os.path.join(output_dir, 'workforce_metrics.png'))
    assert os.path.exists(os.path.join(output_dir, 'organizational_efficiency.png'))


def test_create_all_visualizations(sample_results, output_dir):
    visualizer = SimulationVisualizer(sample_results)
    os.makedirs(output_dir, exist_ok=True)
    
    visualizer.create_all_visualizations(output_dir)
    
    expected_files = [
        'market_position.png',
        'market_share_composition.png',
        'financial_performance.png',
        'financial_ratios.png',
        'infrastructure_growth.png',
        'infrastructure_costs.png',
        'workforce_metrics.png',
        'organizational_efficiency.png'
    ]
    
    for file in expected_files:
        assert os.path.exists(os.path.join(output_dir, file)) 