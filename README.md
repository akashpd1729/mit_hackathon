# 💧 Smart Water Pressure Management System

## Problem Statement
**Smart Water Pressure Management for Equitable Water Supply in Solapur**

### Background
Solapur Municipal Corporation (SMC) provides drinking water to more than 10 lakh residents across multiple distribution zones. Despite continuous efforts, several challenges persist:
- Low water pressure in elevated or tail-end areas
- Uneven distribution across zones
- Irregular supply timings
- Significant water loss due to leakages, aging pipelines, and manual valve operations
- Lack of real-time data, causing delayed response and inefficient planning

### Challenge
Develop a technological solution that enables SMC to monitor, analyze, and maintain optimal water pressure across its distribution network to ensure fair, transparent, and efficient water supply.

## 🎯 Solution Overview
This project provides a comprehensive Smart Water Pressure Management System with:
- **Real-time monitoring** of water pressure and flow across 6 distribution zones
- **Anomaly detection** for leaks, bursts, and pressure variations
- **Predictive analytics** for demand forecasting and resource optimization
- **Interactive dashboard** for municipal engineers and decision-makers
- **Automated recommendations** for maintenance and operational improvements

## 📁 Project Structure
```
mit_hackathon/
├── data/                          # All data files stored here
│   ├── zones_config.json         # Zone configuration
│   ├── pressure_data.csv         # Synthetic pressure readings
│   ├── flow_data.csv             # Synthetic flow data
│   ├── leak_events.csv           # Leak event records
│   └── system_report.json        # Generated system reports
├── utils/                         # Utility modules
│   ├── __init__.py
│   ├── data_generator.py         # Generate synthetic data
│   ├── analytics.py              # Analytics functions
│   └── anomaly_detection.py      # Anomaly detection algorithms
├── main.py                        # Core system functionality
├── streamlit_ui.py               # Streamlit dashboard UI
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or navigate to the repository**
```bash
cd mit_hackathon
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Generate synthetic data**
```bash
python utils/data_generator.py
```

4. **Run the main system (optional)**
```bash
python main.py
```

5. **Launch the Streamlit dashboard**
```bash
streamlit run streamlit_ui.py
```

## 💻 Usage

### Running the Dashboard
The Streamlit UI provides an interactive dashboard with multiple pages:

1. **Dashboard** - System overview, zone health status, and recent trends
2. **Zone Analysis** - Detailed analysis of individual zones
3. **Anomaly Detection** - Detection of pressure/flow anomalies, leaks, and bursts
4. **Flow Analysis** - Water flow patterns and consumption analysis
5. **Recommendations** - Automated recommendations based on detected issues
6. **System Reports** - Generate and download comprehensive reports

### Using the Main System
The `main.py` file provides core functionality:
```python
from main import SmartWaterManagementSystem

# Initialize system
system = SmartWaterManagementSystem()

# Get system overview
overview = system.get_system_overview()

# Get zone health status
health = system.get_zone_health_status()

# Detect anomalies
anomalies = system.detect_all_anomalies()

# Get recommendations
recommendations = system.get_recommendations()

# Export report
system.export_report()
```

## 🔧 Features

### 1. Real-time Monitoring
- Monitor pressure and flow across 6 zones with 28 sensors
- Track 10+ lakh population served
- Visualize real-time data with interactive charts

### 2. Anomaly Detection
- **Pressure Anomalies**: Statistical detection using z-scores
- **Flow Anomalies**: Pattern-based detection with hourly analysis
- **Leak Detection**: Night-time flow analysis for leak identification
- **Burst Detection**: Sudden pressure drop detection

### 3. Predictive Analytics
- Hourly consumption patterns
- Peak demand forecasting
- Water loss estimation
- Zone-wise performance metrics

### 4. Automated Recommendations
- Priority-based issue classification
- Actionable recommendations for each detected issue
- Impact assessment and resource allocation guidance

## 📊 Data

All data is stored in the `data/` folder:
- **zones_config.json**: Configuration for 6 distribution zones
- **pressure_data.csv**: 30 days of pressure readings (15-minute intervals)
- **flow_data.csv**: 30 days of flow rate data
- **leak_events.csv**: Historical leak events
- **system_report.json**: Generated system analysis reports

### Synthetic Data Generation
The system includes a data generator that creates realistic synthetic data:
- Daily consumption patterns (morning/evening peaks)
- Elevation-based pressure variations
- Random anomalies (leaks, bursts, pressure drops)
- Population-proportional flow rates

## 🎨 Technologies Used
- **Python 3.8+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Streamlit**: Interactive web dashboard
- **Plotly**: Interactive visualizations
- **SciPy**: Statistical analysis

## 📈 Key Metrics
The system tracks and displays:
- Average system pressure
- System efficiency percentage
- Water loss estimation
- Zones with issues
- Anomaly counts by severity
- Per capita water consumption

## 🏆 Expected Outcomes Delivered

✅ **Smart water pressure monitoring dashboard** - Interactive Streamlit UI with real-time data visualization

✅ **Predictive analytics model** - Statistical models for anomaly detection and demand forecasting

✅ **User-friendly web interface** - Intuitive dashboard for municipal engineers

✅ **Policy and operational recommendations** - Automated recommendations based on data analysis

## 📝 Evaluation Criteria Addressed

- **Innovation**: Advanced anomaly detection algorithms and predictive analytics
- **Technical Feasibility**: Built with proven Python libraries, easily deployable
- **Cost-effectiveness**: No external database dependencies, runs on standard hardware
- **Scalability**: Modular architecture, easy to add more zones and sensors
- **Integration**: File-based data storage compatible with existing systems
- **Impact**: Identifies leaks, optimizes distribution, ensures equitable supply
- **User Experience**: Clean, intuitive Streamlit interface with multiple views

## 🤝 Contributing
This project was developed for the MIT Vishwaprayag University Hackathon.

## 📧 Contact
**Organization**: MIT Vishwaprayag University  
**Department**: Computer Science  
**Category**: Smart Water  
**Theme**: General

## 📄 License
MIT License
