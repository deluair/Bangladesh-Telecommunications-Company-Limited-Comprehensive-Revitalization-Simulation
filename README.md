# BTCL Revitalization Simulation

A comprehensive simulation framework for Bangladesh Telecommunications Company Limited (BTCL) revitalization.

## Project Overview

This simulation models BTCL's transformation from a declining state-owned telecommunications operator to a modern, competitive digital infrastructure and services provider. The framework includes:

- Market position and financial analysis
- Infrastructure modernization scenarios
- Operational efficiency improvements
- Organizational transformation models
- Financial sustainability projections
- Digital services development

## Project Structure

```
btcl-simulation/
├── data/                  # Data files and configurations
├── models/               # Core simulation models
├── scenarios/            # Different transformation scenarios
├── analysis/             # Analysis tools and visualizations
├── utils/               # Utility functions and helpers
└── tests/               # Test cases
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Configure simulation parameters in `data/config.yaml`
2. Run specific scenarios:
```bash
python -m scenarios.run_scenario <scenario_name>
```

3. Generate analysis reports:
```bash
python -m analysis.generate_report
```

## Key Features

- Realistic market simulation
- Financial modeling
- Infrastructure modernization planning
- Operational efficiency analysis
- Workforce transformation modeling
- Digital services development simulation

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 