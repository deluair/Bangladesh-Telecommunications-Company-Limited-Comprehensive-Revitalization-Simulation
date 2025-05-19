"""
Shared test fixtures for BTCL simulation tests
"""

import pytest
import os
import yaml
import pandas as pd
import numpy as np


@pytest.fixture
def base_config():
    return {
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


@pytest.fixture
def config_file(tmp_path, base_config):
    config_path = tmp_path / "config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(base_config, f)
    return str(config_path)


@pytest.fixture
def output_dir(tmp_path):
    return str(tmp_path / "results")


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