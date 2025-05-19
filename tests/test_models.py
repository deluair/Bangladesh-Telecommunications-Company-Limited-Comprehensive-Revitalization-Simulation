"""
Tests for BTCL simulation models
"""

import pytest
import numpy as np
from btcl_simulation.models.market_position import MarketPositionModel
from btcl_simulation.models.financial import FinancialModel
from btcl_simulation.models.infrastructure import InfrastructureModel
from btcl_simulation.models.organizational import OrganizationalModel


def test_market_position_model(base_config):
    model = MarketPositionModel(base_config['market_position'])
    results = model.simulate(5)
    
    assert 'year' in results
    assert 'fixed_line_subscribers' in results
    assert 'broadband_market_share' in results
    assert 'mobile_market_share' in results
    assert 'enterprise_market_share' in results
    
    assert len(results['year']) == 5
    assert results['fixed_line_subscribers'][0] == base_config['market_position']['fixed_line_base']
    assert results['broadband_market_share'][0] == base_config['market_position']['broadband_base']
    assert results['mobile_market_share'][0] == base_config['market_position']['mobile_base']
    assert results['enterprise_market_share'][0] == base_config['market_position']['enterprise_base']


def test_financial_model(base_config):
    model = FinancialModel(base_config['financial'])
    results = model.simulate(5)
    
    assert 'year' in results
    assert 'revenue' in results
    assert 'ebitda' in results
    assert 'net_income' in results
    assert 'debt' in results
    
    assert len(results['year']) == 5
    assert results['revenue'][0] == base_config['financial']['revenue_base']
    assert results['debt'][0] == base_config['financial']['debt_base']


def test_infrastructure_model(base_config):
    model = InfrastructureModel(base_config['infrastructure'])
    results = model.simulate(5)
    
    assert 'year' in results
    assert 'fiber_network' in results
    assert 'ftth_ports' in results
    assert 'data_center_capacity' in results
    assert 'infrastructure_cost' in results
    
    assert len(results['year']) == 5
    assert results['fiber_network'][0] == base_config['infrastructure']['fiber_network_base']
    assert results['ftth_ports'][0] == base_config['infrastructure']['ftth_ports_base']
    assert results['data_center_capacity'][0] == base_config['infrastructure']['data_center_capacity_base']


def test_organizational_model(base_config):
    model = OrganizationalModel(base_config['organizational'])
    results = model.simulate(5)
    
    assert 'year' in results
    assert 'employees' in results
    assert 'avg_age' in results
    assert 'digital_skills' in results
    assert 'operational_efficiency' in results
    
    assert len(results['year']) == 5
    assert results['employees'][0] == base_config['organizational']['employee_base']
    assert results['avg_age'][0] == base_config['organizational']['avg_age_base']
    assert results['digital_skills'][0] == base_config['organizational']['digital_skills_base']
    assert results['operational_efficiency'][0] == base_config['organizational']['operational_efficiency_base']


def test_market_position_summary(base_config):
    model = MarketPositionModel(base_config['market_position'])
    model.simulate(5)
    summary = model.get_market_summary()
    
    assert 'fixed_line_change' in summary
    assert 'broadband_change' in summary
    assert 'mobile_change' in summary
    assert 'enterprise_change' in summary


def test_financial_summary(base_config):
    model = FinancialModel(base_config['financial'])
    model.simulate(5)
    summary = model.get_financial_summary()
    
    assert 'revenue_change' in summary
    assert 'ebitda_margin' in summary
    assert 'debt_reduction' in summary
    assert 'employee_cost_ratio' in summary
    assert 'capex_intensity' in summary


def test_infrastructure_summary(base_config):
    model = InfrastructureModel(base_config['infrastructure'])
    model.simulate(5)
    summary = model.get_infrastructure_summary()
    
    assert 'fiber_network_growth' in summary
    assert 'ftth_port_growth' in summary
    assert 'data_center_growth' in summary
    assert 'total_infrastructure_cost' in summary
    assert 'network_automation_achieved' in summary


def test_organizational_summary(base_config):
    model = OrganizationalModel(base_config['organizational'])
    model.simulate(5)
    summary = model.get_organizational_summary()
    
    assert 'workforce_reduction' in summary
    assert 'avg_age_reduction' in summary
    assert 'digital_skills_growth' in summary
    assert 'operational_efficiency_growth' in summary
    assert 'total_transformation_cost' in summary 