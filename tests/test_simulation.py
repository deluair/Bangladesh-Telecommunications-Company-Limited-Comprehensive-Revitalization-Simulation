"""
Tests for BTCL simulation runner
"""

import pytest
import os
import yaml
from btcl_simulation.simulation import BTCLSimulation


@pytest.fixture
def config_file(tmp_path):
    config = {
        'market_position': {
            'fixed_line_base': 500000,
            'broadband_base': 0.12,
            'mobile_base': 0.0,
            'enterprise_base': 0.15,
            'fixed_line_decline': -0.05,
            'broadband_growth': 0.15,
            'mobile_growth': 0.10,
            'enterprise_growth': 0.20
        },
        'financial': {
            'revenue_base': 1000,
            'employee_cost_ratio': 0.68,
            'other_opex_ratio': 0.25,
            'capex_ratio': 0.15,
            'debt_base': 1500,
            'interest_rate': 0.08,
            'revenue_growth': -0.06,
            'cost_reduction': 0.05,
            'asset_utilization': 0.30
        },
        'infrastructure': {
            'copper_network_base': 1000000,
            'fiber_network_base': 5000,
            'dsl_ports_base': 200000,
            'ftth_ports_base': 50000,
            'data_center_capacity_base': 100,
            'copper_to_fiber_conversion': 0.15,
            'dsl_to_ftth_conversion': 0.20,
            'data_center_expansion': 0.25,
            'network_automation': 0.10,
            'fiber_deployment_cost': 500000,
            'ftth_port_cost': 5000,
            'data_center_rack_cost': 1000000
        },
        'organizational': {
            'employee_base': 8500,
            'avg_age_base': 48,
            'digital_skills_base': 0.15,
            'operational_efficiency_base': 0.30,
            'vrs_rate': 0.15,
            'new_hiring_rate': 0.10,
            'digital_skills_growth': 0.20,
            'operational_efficiency_growth': 0.15,
            'avg_salary': 50000,
            'vrs_package': 24,
            'training_cost': 50000
        },
        'simulation': {
            'years': 5,
            'random_seed': 42
        }
    }
    
    config_path = tmp_path / "config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config, f)
    
    return str(config_path)


@pytest.fixture
def output_dir(tmp_path):
    return str(tmp_path / "results")


def test_simulation_initialization(config_file):
    simulation = BTCLSimulation(config_file)
    assert simulation.config is not None
    assert simulation.market_model is not None
    assert simulation.financial_model is not None
    assert simulation.infrastructure_model is not None
    assert simulation.organizational_model is not None


def test_simulation_run(config_file, output_dir):
    simulation = BTCLSimulation(config_file)
    results = simulation.run()
    
    assert 'market_position' in results
    assert 'financial' in results
    assert 'infrastructure' in results
    assert 'organizational' in results
    
    assert len(results['market_position']['year']) == 5
    assert len(results['financial']['year']) == 5
    assert len(results['infrastructure']['year']) == 5
    assert len(results['organizational']['year']) == 5


def test_simulation_save_results(config_file, output_dir):
    simulation = BTCLSimulation(config_file)
    simulation.run()
    simulation.save_results(output_dir)
    
    assert os.path.exists(os.path.join(output_dir, 'market_position.csv'))
    assert os.path.exists(os.path.join(output_dir, 'financial.csv'))
    assert os.path.exists(os.path.join(output_dir, 'infrastructure.csv'))
    assert os.path.exists(os.path.join(output_dir, 'organizational.csv'))
    assert os.path.exists(os.path.join(output_dir, 'summary.txt'))


def test_simulation_summary(config_file):
    simulation = BTCLSimulation(config_file)
    simulation.run()
    summary = simulation.get_summary()
    
    assert 'market_position' in summary
    assert 'financial' in summary
    assert 'infrastructure' in summary
    assert 'organizational' in summary
    
    market_summary = summary['market_position']
    assert 'fixed_line_change' in market_summary
    assert 'broadband_change' in market_summary
    assert 'mobile_change' in market_summary
    assert 'enterprise_change' in market_summary
    
    financial_summary = summary['financial']
    assert 'revenue_change' in financial_summary
    assert 'ebitda_margin' in financial_summary
    assert 'debt_reduction' in financial_summary
    
    infrastructure_summary = summary['infrastructure']
    assert 'fiber_network_growth' in infrastructure_summary
    assert 'ftth_port_growth' in infrastructure_summary
    assert 'data_center_growth' in infrastructure_summary
    
    organizational_summary = summary['organizational']
    assert 'workforce_reduction' in organizational_summary
    assert 'avg_age_reduction' in organizational_summary
    assert 'digital_skills_growth' in organizational_summary 