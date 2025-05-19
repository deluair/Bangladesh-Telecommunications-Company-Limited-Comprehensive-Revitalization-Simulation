# Bangladesh Telecommunications Company Limited (BTCL) Revitalization Simulation

A comprehensive simulation framework for revitalizing Bangladesh Telecommunications Company Limited (BTCL), modeling its transformation into a modern, competitive digital infrastructure and services provider.

Repository: [GitHub - BTCL Revitalization Simulation](https://github.com/deluair/Bangladesh-Telecommunications-Company-Limited-Comprehensive-Revitalization-Simulation)

---

## Overview

This project simulates BTCL's journey from a legacy state-owned operator to a digitally empowered, efficient, and financially sustainable telecom company. The simulation covers:
- Market position and competitive dynamics
- Financial performance and sustainability
- Infrastructure modernization
- Organizational transformation
- Scenario-based analysis and visualization

## Features
- **Market, Financial, Infrastructure, and Organizational Models**: Modular, extensible Python classes for each transformation pillar.
- **Configurable Simulation**: All parameters are set in a single YAML file (`btcl_simulation/data/config.yaml`).
- **Comprehensive Results**: Outputs detailed CSVs, YAML summaries, and human-readable summaries.
- **Visualization**: Generates insightful plots for all key metrics.
- **Testing & Coverage**: Full pytest suite and coverage configuration.

## Project Structure
```
.
├── btcl_simulation/
│   ├── __init__.py
│   ├── data/
│   │   └── config.yaml           # Main simulation configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── market_position.py
│   │   ├── financial.py
│   │   ├── infrastructure.py
│   │   └── organizational.py
│   ├── simulation.py             # Main simulation runner
│   └── visualization.py          # Visualization module
├── results/                      # (Created after running simulation)
├── tests/                        # Pytest test suite
├── run_simulation.py             # Script to run the simulation
├── requirements.txt
├── setup.py
├── .coveragerc
├── .gitignore
├── README.md
└── ...
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/deluair/Bangladesh-Telecommunications-Company-Limited-Comprehensive-Revitalization-Simulation.git
   cd Bangladesh-Telecommunications-Company-Limited-Comprehensive-Revitalization-Simulation
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Configure simulation parameters:**
   - Edit `btcl_simulation/data/config.yaml` to set market, financial, infrastructure, and organizational parameters.

2. **Run the simulation:**
   ```bash
   python run_simulation.py
   ```
   - Results will be saved in the `results/` directory.
   - Visualizations will be saved in `results/plots/`.

3. **Outputs:**
   - `results/combined_results.csv`: All key metrics per year.
   - `results/market_position.csv`, `results/financial.csv`, etc.: Per-model results.
   - `results/simulation_summary.yaml`: Machine-readable summary.
   - `results/summary.txt`: Human-readable summary.
   - `results/plots/`: PNG visualizations for all major metrics.

## Configuration
- All simulation parameters are set in `btcl_simulation/data/config.yaml`.
- You can adjust:
  - Number of years (`time_periods` or `years`)
  - Market share, growth/decline rates
  - Financial ratios, debt, revenue growth
  - Infrastructure expansion rates and costs
  - Workforce, skills, efficiency, and cost parameters

## Testing & Coverage
- **Run all tests:**
  ```bash
  pytest --cov=btcl_simulation --cov-report=term-missing
  ```
- **Test files:** Located in the `tests/` directory, covering all models, simulation runner, and visualization.
- **Coverage config:** See `.coveragerc` for exclusions and reporting.

## Contributing
Contributions are welcome! Please open issues or pull requests for improvements, bug fixes, or new features.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details. 