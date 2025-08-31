# Sustainable Agriculture — Soil Testing & Fertilizer Recommender

A machine learning system that provides personalized fertilizer recommendations based on soil testing results and environmental conditions.

## 🎯 Project Goal

This project aims to help farmers optimize fertilizer usage by analyzing soil composition data and providing data-driven recommendations. The system reduces environmental impact while improving crop yields through precise nutrient management.

## 🚀 Quick Start

### 1. Generate Synthetic Dataset

First, create the synthetic soil testing dataset:

```bash
python src/generate_synthetic_data.py
```

This will create sample soil data with various parameters like pH, nitrogen, phosphorus, potassium, and organic matter content.

### 2. Run Baseline Recommender

Explore the data and run the baseline recommendation system:

```bash
jupyter lab
```

Then navigate to `notebooks/01_EDA_and_baseline.ipynb` to:
- Perform exploratory data analysis
- Understand soil-fertilizer relationships
- Run baseline recommendation algorithms
- Evaluate initial model performance

## 📋 Week-1 Deliverables

- [ ] **Synthetic Dataset Generation**
  - Soil composition data (pH, N, P, K, organic matter)
  - Fertilizer types and application rates
  - Environmental conditions (temperature, humidity, season)
  - Historical yield data

- [ ] **Data Exploration & Analysis**
  - Statistical summary of soil parameters
  - Correlation analysis between soil and fertilizer needs
  - Visualization of key relationships
  - Data quality assessment

- [ ] **Baseline Recommendation System**
  - Simple rule-based recommendations
  - Basic ML model (e.g., decision tree)
  - Performance metrics calculation
  - Comparison with expert knowledge

- [ ] **Documentation & Reporting**
  - Data dictionary and schema
  - Baseline model documentation
  - Initial findings and insights
  - Next steps and improvements

## 📁 Project Structure

```
sustainable-agri-recommender/
├── src/                     # Source code
│   └── generate_synthetic_data.py
├── data/                    # Data files
│   └── raw/                # Raw data files
├── notebooks/               # Jupyter notebooks
│   └── 01_EDA_and_baseline.ipynb
├── results/                 # Output results
└── tests/                   # Unit tests
```

## 🛠️ Installation

1. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔬 Technology Stack

- **Data Processing**: pandas, numpy
- **Machine Learning**: scikit-learn
- **Visualization**: matplotlib
- **Testing**: pytest
- **Model Persistence**: joblib

## 📊 Expected Outcomes

By the end of Week 1, you should have:
- A working synthetic dataset generator
- Comprehensive data exploration insights
- A baseline recommendation system
- Clear understanding of soil-fertilizer relationships
- Foundation for advanced ML models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python -m pytest`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.
