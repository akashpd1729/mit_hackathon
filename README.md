# 💧 Smart Water Pressure Management System

## 📖 What is This Project?

This is a **Smart Water Pressure Management System** developed for the MIT Vishwaprayag University Hackathon. It's a comprehensive solution designed to help Solapur Municipal Corporation (SMC) monitor, analyze, and optimize water distribution across the city.

### The Problem
Solapur Municipal Corporation serves over **10 lakh (1 million) residents** but faces several challenges:
- 💧 Low water pressure in elevated areas
- ⚖️ Uneven distribution across zones
- 🕐 Irregular supply timings
- 💸 Water loss due to leakages and aging pipelines
- 📊 Lack of real-time monitoring data

### Our Solution
This system provides:
- **📊 Real-time Monitoring Dashboard** - Track water pressure and flow across 6 zones with 28 sensors
- **🚨 Anomaly Detection** - Automatically detect leaks, bursts, and pressure issues
- **📈 Predictive Analytics** - Forecast demand patterns and identify problem areas
- **💡 Smart Recommendations** - Get actionable insights for maintenance and optimization
- **📄 Comprehensive Reports** - Generate detailed system performance reports

### Key Features
✅ Monitors 6 distribution zones covering 10+ lakh population  
✅ Tracks 28 sensors with 15-minute interval data  
✅ Detects pressure anomalies, leaks, and burst events  
✅ Analyzes consumption patterns and peak demand times  
✅ Provides automated recommendations for municipal engineers  
✅ Interactive web dashboard built with Streamlit  
✅ All data stored locally (no cloud dependencies)

## 📁 Project Structure & File Descriptions

```
mit_hackathon/
├── data/                          # All data files stored here (NO database needed!)
│   ├── zones_config.json         # Configuration for 6 water distribution zones
│   ├── pressure_data.csv         # 80,640 pressure readings (30 days, 15-min intervals)
│   ├── flow_data.csv             # 17,280 flow rate measurements
│   ├── leak_events.csv           # 20 historical leak events with severity
│   └── system_report.json        # Auto-generated system analysis report
│
├── utils/                         # Utility modules for data processing
│   ├── __init__.py               # Package initializer
│   ├── data_generator.py         # Generates realistic synthetic water data
│   ├── analytics.py              # Statistical analysis & zone comparisons
│   └── anomaly_detection.py      # ML-based leak & burst detection
│
├── main.py                        # Core system - Run this for CLI analysis
├── streamlit_ui.py               # Web dashboard - Run this for interactive UI
├── requirements.txt              # Python dependencies (pandas, streamlit, etc.)
└── README.md                     # This documentation file
```

### 📄 Detailed File Functionality

#### **Data Files (data/ folder)**
- **`zones_config.json`** - Defines 6 zones with elevation, population, sensor count, and GPS coordinates
- **`pressure_data.csv`** - Contains timestamp, zone, sensor ID, pressure (PSI), elevation, and status
- **`flow_data.csv`** - Contains timestamp, zone, flow rate (LPM), and population data
- **`leak_events.csv`** - Records leak events with severity, estimated loss, and response time
- **`system_report.json`** - Comprehensive JSON report with metrics, health status, and recommendations

#### **Python Modules (utils/ folder)**
- **`data_generator.py`** - Creates synthetic data with realistic patterns:
  - Daily consumption cycles (morning/evening peaks)
  - Elevation-based pressure variations
  - Random anomalies (2% leak probability)
  - Population-proportional flow rates

- **`analytics.py`** - Provides analytical functions:
  - Zone statistics (avg, min, max pressure)
  - Hourly consumption patterns
  - Low pressure zone identification
  - Water loss estimation
  - Per capita consumption calculations

- **`anomaly_detection.py`** - Detects issues using statistical methods:
  - Pressure anomalies (z-score based)
  - Flow anomalies (pattern analysis)
  - Leak detection (night-time flow analysis)
  - Burst detection (sudden pressure drops)

#### **Main Application Files**
- **`main.py`** - Core system with CLI interface:
  - Initializes the water management system
  - Loads and processes all data
  - Generates system overview and metrics
  - Detects anomalies and creates recommendations
  - Exports comprehensive JSON reports
  - **Run this to see system analysis in terminal**

- **`streamlit_ui.py`** - Interactive web dashboard:
  - 6-page dashboard (Dashboard, Zone Analysis, Anomaly Detection, Flow Analysis, Recommendations, Reports)
  - Real-time data visualizations with Plotly
  - Interactive charts and graphs
  - Zone health status monitoring
  - Downloadable reports
  - **Run this to launch the web interface**

## 🚀 How to Run This Project

### Prerequisites
- **Python 3.8 or higher** installed on your system
- **pip** package manager (comes with Python)

### Quick Start Guide

Follow these steps to get the system running:

#### **Step 1: Navigate to Project Directory**
```bash
cd mit_hackathon
```

#### **Step 2: Install Required Python Packages**
```bash
pip install -r requirements.txt
```
This installs: pandas, numpy, streamlit, plotly, scipy

#### **Step 3: Generate Synthetic Data (First Time Only)**
```bash
python utils/data_generator.py
```
**What this does:**
- Creates 80,640 pressure readings across 6 zones
- Generates 17,280 flow measurements
- Creates 20 leak events
- Saves all data to the `data/` folder
- Takes about 10-30 seconds to complete

**Output:** You'll see messages like:
```
Generating pressure data...
✓ Saved 80640 pressure records
Generating flow data...
✓ Saved 17280 flow records
Generating leak events...
✓ Saved 20 leak events
```

#### **Step 4: Run the System**

You have **TWO options** to run the system:

##### **Option A: Web Dashboard (Recommended) 🌐**
```bash
streamlit run streamlit_ui.py
```
**What happens:**
- Opens your web browser automatically
- Shows interactive dashboard at `http://localhost:8501`
- Navigate through 6 pages using the sidebar
- View charts, graphs, and real-time analytics
- **Best for:** Visual analysis and presentations

##### **Option B: Command Line Analysis 💻**
```bash
python main.py
```
**What happens:**
- Runs analysis in the terminal
- Displays system overview, metrics, and recommendations
- Generates `system_report.json` in the `data/` folder
- **Best for:** Quick checks and automated reporting

### 🎯 What to Expect After Running

#### **When you run `streamlit run streamlit_ui.py`:**
1. Browser opens automatically to `http://localhost:8501`
2. You'll see the main dashboard with:
   - System metrics (zones, population, sensors)
   - Zone health status with color-coded alerts
   - Pressure trends over the last 7 days
   - Anomaly summary

3. **Navigate using the sidebar:**
   - 📊 **Dashboard** - Overview and key metrics
   - 🏙️ **Zone Analysis** - Deep dive into each zone
   - 🚨 **Anomaly Detection** - View detected issues
   - 💧 **Flow Analysis** - Consumption patterns
   - 💡 **Recommendations** - Actionable insights
   - 📄 **System Reports** - Generate & download reports

#### **When you run `python main.py`:**
You'll see terminal output like:
```
============================================================
Smart Water Pressure Management System
Solapur Municipal Corporation
============================================================

📊 System Overview:
Total Zones: 6
Total Population Served: 750,000
Total Sensors: 28

📈 Performance Metrics:
Avg System Pressure: 42.5
System Efficiency: 85.3%

🏥 Zone Health Status:
[Table showing each zone's status]

💡 Recommendations:
[List of actionable recommendations]

✓ System check complete!
```

## 💻 Advanced Usage

### Using the System Programmatically
You can import and use the system in your own Python scripts:

```python
from main import SmartWaterManagementSystem

# Initialize the system
system = SmartWaterManagementSystem()

# Get system overview (zones, population, sensors)
overview = system.get_system_overview()
print(f"Total Zones: {overview['total_zones']}")
print(f"Population Served: {overview['total_population']:,}")

# Get zone health status
health = system.get_zone_health_status()
print(health)

# Detect all anomalies
anomalies = system.detect_all_anomalies()
print(f"Pressure Anomalies: {anomalies['summary']['total_pressure_anomalies']}")
print(f"Potential Leaks: {anomalies['summary']['potential_leaks']}")

# Get automated recommendations
recommendations = system.get_recommendations()
print(recommendations)

# Export comprehensive report to JSON
system.export_report('data/system_report.json')
```

### Regenerating Data
If you want to generate fresh data with different patterns:
```bash
python utils/data_generator.py
```
This will overwrite existing data files with new synthetic data.

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
