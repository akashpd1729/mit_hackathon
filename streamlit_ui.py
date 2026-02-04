"""
Streamlit UI for Smart Water Pressure Management System
Interactive dashboard for monitoring and analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import sys

# Add utils to path
sys.path.append(os.path.dirname(__file__))

from main import SmartWaterManagementSystem
from utils.analytics import WaterAnalytics
from utils.anomaly_detection import AnomalyDetector


# Page configuration
st.set_page_config(
    page_title="Smart Water Management - Solapur",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .status-healthy {
        color: #28a745;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .status-critical {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_system():
    """Load the water management system"""
    return SmartWaterManagementSystem()


@st.cache_data
def load_pressure_data():
    """Load pressure data"""
    df = pd.read_csv('data/pressure_data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


@st.cache_data
def load_flow_data():
    """Load flow data"""
    df = pd.read_csv('data/flow_data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<div class="main-header">💧 Smart Water Pressure Management System<br>Solapur Municipal Corporation</div>', 
                unsafe_allow_html=True)
    
    # Initialize system
    try:
        system = load_system()
        pressure_df = load_pressure_data()
        flow_df = load_flow_data()
    except Exception as e:
        st.error(f"Error loading system: {e}")
        st.info("Please run the data generator first: `python utils/data_generator.py`")
        return
    
    # Sidebar
    st.sidebar.title("🎛️ Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Dashboard", "Zone Analysis", "Anomaly Detection", "Flow Analysis", 
         "Recommendations", "System Reports"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "**About:**\n\n"
        "This system monitors water pressure and flow across Solapur's "
        "distribution network to ensure equitable water supply."
    )
    
    # Page routing
    if page == "Dashboard":
        show_dashboard(system, pressure_df, flow_df)
    elif page == "Zone Analysis":
        show_zone_analysis(system, pressure_df, flow_df)
    elif page == "Anomaly Detection":
        show_anomaly_detection(system)
    elif page == "Flow Analysis":
        show_flow_analysis(system, flow_df)
    elif page == "Recommendations":
        show_recommendations(system)
    elif page == "System Reports":
        show_reports(system)


def show_dashboard(system, pressure_df, flow_df):
    """Show main dashboard"""
    st.header("📊 System Dashboard")
    
    # Performance metrics
    metrics = system.get_performance_metrics()
    overview = system.get_system_overview()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Zones", overview['total_zones'])
    with col2:
        st.metric("Population Served", f"{overview['total_population']:,}")
    with col3:
        st.metric("Avg Pressure (PSI)", metrics['avg_system_pressure'])
    with col4:
        st.metric("System Efficiency", f"{metrics['system_efficiency']}%")
    with col5:
        st.metric("Active Sensors", overview['total_sensors'])
    
    st.markdown("---")
    
    # Zone health status
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🗺️ Zone Health Status")
        health_df = system.get_zone_health_status()
        
        # Create color map
        color_map = {
            'healthy': '#28a745',
            'attention': '#17a2b8',
            'warning': '#ffc107',
            'critical': '#dc3545'
        }
        
        fig = px.bar(
            health_df,
            x='zone_name',
            y='avg_pressure',
            color='status',
            color_discrete_map=color_map,
            title='Average Pressure by Zone',
            labels={'avg_pressure': 'Avg Pressure (PSI)', 'zone_name': 'Zone'}
        )
        fig.add_hline(y=40, line_dash="dash", line_color="red", 
                     annotation_text="Minimum Threshold")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📋 Zone Status")
        for _, row in health_df.iterrows():
            status_class = f"status-{row['status']}"
            st.markdown(
                f"**{row['zone_name']}**  \n"
                f"<span class='{status_class}'>{row['status'].upper()}</span>  \n"
                f"Pressure: {row['avg_pressure']} PSI",
                unsafe_allow_html=True
            )
            st.markdown("---")
    
    # Recent pressure trends
    st.subheader("📈 Recent Pressure Trends (Last 7 Days)")
    recent_data = pressure_df[
        pressure_df['timestamp'] >= (datetime.now() - timedelta(days=7))
    ]
    
    # Aggregate by hour
    recent_data['hour'] = recent_data['timestamp'].dt.floor('H')
    hourly_avg = recent_data.groupby(['hour', 'zone_name'])['pressure_psi'].mean().reset_index()
    
    fig = px.line(
        hourly_avg,
        x='hour',
        y='pressure_psi',
        color='zone_name',
        title='Hourly Average Pressure by Zone',
        labels={'pressure_psi': 'Pressure (PSI)', 'hour': 'Time'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Anomaly summary
    st.subheader("⚠️ Anomaly Summary")
    anomalies = system.detect_all_anomalies()
    summary = anomalies['summary']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pressure Anomalies", summary['total_pressure_anomalies'])
    with col2:
        st.metric("Flow Anomalies", summary['total_flow_anomalies'])
    with col3:
        st.metric("Potential Leaks", summary['potential_leaks'])
    with col4:
        st.metric("Critical Events", summary['critical_events'])


def show_zone_analysis(system, pressure_df, flow_df):
    """Show detailed zone analysis"""
    st.header("🏙️ Zone Analysis")
    
    # Zone selector
    zones = pressure_df['zone_name'].unique()
    selected_zone = st.selectbox("Select Zone", zones)
    
    # Filter data for selected zone
    zone_pressure = pressure_df[pressure_df['zone_name'] == selected_zone]
    zone_flow = flow_df[flow_df['zone_name'] == selected_zone]
    
    # Zone statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Pressure", f"{zone_pressure['pressure_psi'].mean():.2f} PSI")
    with col2:
        st.metric("Min Pressure", f"{zone_pressure['pressure_psi'].min():.2f} PSI")
    with col3:
        st.metric("Max Pressure", f"{zone_pressure['pressure_psi'].max():.2f} PSI")
    with col4:
        st.metric("Std Deviation", f"{zone_pressure['pressure_psi'].std():.2f}")
    
    st.markdown("---")
    
    # Pressure distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Pressure Distribution")
        fig = px.histogram(
            zone_pressure,
            x='pressure_psi',
            nbins=30,
            title=f'Pressure Distribution - {selected_zone}',
            labels={'pressure_psi': 'Pressure (PSI)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Pressure Over Time")
        # Sample data for better visualization
        sampled = zone_pressure.sample(min(1000, len(zone_pressure)))
        fig = px.scatter(
            sampled,
            x='timestamp',
            y='pressure_psi',
            color='sensor_id',
            title=f'Pressure Readings - {selected_zone}',
            labels={'pressure_psi': 'Pressure (PSI)', 'timestamp': 'Time'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Hourly patterns
    st.subheader("🕐 Daily Pressure Patterns")
    zone_pressure['hour'] = zone_pressure['timestamp'].dt.hour
    hourly_avg = zone_pressure.groupby('hour')['pressure_psi'].mean().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hourly_avg['hour'],
        y=hourly_avg['pressure_psi'],
        mode='lines+markers',
        name='Avg Pressure',
        line=dict(color='#1f77b4', width=3)
    ))
    fig.update_layout(
        title=f'Average Pressure by Hour - {selected_zone}',
        xaxis_title='Hour of Day',
        yaxis_title='Pressure (PSI)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Sensor comparison
    st.subheader("🔍 Sensor Comparison")
    sensor_stats = zone_pressure.groupby('sensor_id')['pressure_psi'].agg(['mean', 'min', 'max']).reset_index()
    sensor_stats.columns = ['Sensor ID', 'Avg Pressure', 'Min Pressure', 'Max Pressure']
    st.dataframe(sensor_stats, use_container_width=True)


def show_anomaly_detection(system):
    """Show anomaly detection results"""
    st.header("🚨 Anomaly Detection")
    
    anomalies = system.detect_all_anomalies()
    
    # Tabs for different anomaly types
    tab1, tab2, tab3, tab4 = st.tabs(["Pressure Anomalies", "Flow Anomalies", "Leak Detection", "Burst Events"])
    
    with tab1:
        st.subheader("⚠️ Pressure Anomalies")
        pressure_anomalies = anomalies['pressure_anomalies']
        
        if len(pressure_anomalies) > 0:
            # Severity distribution
            severity_counts = pressure_anomalies['severity'].value_counts()
            fig = px.pie(
                values=severity_counts.values,
                names=severity_counts.index,
                title='Anomalies by Severity'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Recent anomalies
            st.subheader("Recent Pressure Anomalies")
            recent = pressure_anomalies.sort_values('timestamp', ascending=False).head(20)
            st.dataframe(recent[['timestamp', 'zone_name', 'sensor_id', 'pressure_psi', 
                                'expected_pressure', 'deviation', 'severity']], 
                        use_container_width=True)
        else:
            st.success("No pressure anomalies detected!")
    
    with tab2:
        st.subheader("💧 Flow Anomalies")
        flow_anomalies = anomalies['flow_anomalies']
        
        if len(flow_anomalies) > 0:
            # Anomaly types
            type_counts = flow_anomalies['anomaly_type'].value_counts()
            fig = px.bar(
                x=type_counts.index,
                y=type_counts.values,
                title='Flow Anomalies by Type',
                labels={'x': 'Anomaly Type', 'y': 'Count'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Recent flow anomalies
            st.subheader("Recent Flow Anomalies")
            recent = flow_anomalies.sort_values('timestamp', ascending=False).head(20)
            st.dataframe(recent[['timestamp', 'zone_name', 'flow_rate_lpm', 
                                'expected_flow', 'anomaly_type', 'potential_cause']], 
                        use_container_width=True)
        else:
            st.success("No flow anomalies detected!")
    
    with tab3:
        st.subheader("🔧 Leak Detection")
        leaks = anomalies['leaks']
        
        if len(leaks) > 0:
            st.warning(f"⚠️ {len(leaks)} potential leak(s) detected!")
            
            # Leak severity
            fig = px.bar(
                leaks,
                x='zone_name',
                y='estimated_daily_loss_liters',
                color='severity',
                title='Estimated Daily Water Loss by Zone',
                labels={'estimated_daily_loss_liters': 'Daily Loss (Liters)', 
                       'zone_name': 'Zone'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Leak details
            st.dataframe(leaks, use_container_width=True)
        else:
            st.success("No leaks detected!")
    
    with tab4:
        st.subheader("💥 Burst Events")
        bursts = anomalies['bursts']
        
        if len(bursts) > 0:
            st.error(f"🚨 {len(bursts)} potential burst event(s) detected!")
            
            # Burst locations
            fig = px.scatter(
                bursts,
                x='timestamp',
                y='pressure_drop',
                color='severity',
                size='pressure_drop',
                hover_data=['zone_name', 'sensor_id'],
                title='Burst Events Timeline',
                labels={'pressure_drop': 'Pressure Drop (PSI)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Burst details
            st.dataframe(bursts[['timestamp', 'zone_name', 'sensor_id', 
                                'pressure_before', 'pressure_after', 'pressure_drop', 
                                'severity', 'recommended_action']], 
                        use_container_width=True)
        else:
            st.success("No burst events detected!")


def show_flow_analysis(system, flow_df):
    """Show flow analysis"""
    st.header("💧 Flow Analysis")
    
    analytics = WaterAnalytics()
    
    # Flow statistics
    st.subheader("📊 Flow Statistics by Zone")
    flow_stats = analytics.get_flow_statistics()
    st.dataframe(flow_stats, use_container_width=True)
    
    # Flow comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Average Flow Rate by Zone")
        fig = px.bar(
            flow_stats,
            x='zone_name',
            y='avg_flow',
            title='Average Flow Rate',
            labels={'avg_flow': 'Flow Rate (LPM)', 'zone_name': 'Zone'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Per Capita Flow")
        fig = px.bar(
            flow_stats,
            x='zone_name',
            y='per_capita_flow',
            title='Per Capita Flow Rate',
            labels={'per_capita_flow': 'Flow per 1000 people (LPM)', 'zone_name': 'Zone'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Peak demand analysis
    st.subheader("⏰ Peak Demand Analysis")
    peak_times = analytics.get_peak_demand_times()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=peak_times['hour'],
        y=peak_times['flow_rate_lpm'],
        marker_color='lightblue'
    ))
    fig.update_layout(
        title='Average Flow Rate by Hour',
        xaxis_title='Hour of Day',
        yaxis_title='Flow Rate (LPM)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Water loss estimation
    st.subheader("💸 Water Loss Estimation")
    water_loss = analytics.calculate_water_loss()
    
    if len(water_loss[water_loss['potential_leak']]) > 0:
        st.warning("⚠️ Zones with potential leakage detected!")
        leak_zones = water_loss[water_loss['potential_leak']]
        
        fig = px.bar(
            leak_zones,
            x='zone_name',
            y='estimated_daily_loss_liters',
            title='Estimated Daily Water Loss',
            labels={'estimated_daily_loss_liters': 'Daily Loss (Liters)', 
                   'zone_name': 'Zone'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(water_loss, use_container_width=True)


def show_recommendations(system):
    """Show recommendations"""
    st.header("💡 Recommendations")
    
    recommendations = system.get_recommendations()
    
    if len(recommendations) > 0:
        # Priority filter
        priorities = ['All'] + list(recommendations['priority'].unique())
        selected_priority = st.selectbox("Filter by Priority", priorities)
        
        if selected_priority != 'All':
            filtered = recommendations[recommendations['priority'] == selected_priority]
        else:
            filtered = recommendations
        
        # Display recommendations
        for _, rec in filtered.iterrows():
            priority_color = {
                'critical': '🔴',
                'high': '🟠',
                'moderate': '🟡',
                'low': '🟢'
            }
            
            with st.expander(f"{priority_color.get(rec['priority'], '⚪')} {rec['zone']} - {rec['issue']}"):
                st.markdown(f"**Priority:** {rec['priority'].upper()}")
                st.markdown(f"**Zone:** {rec['zone']}")
                st.markdown(f"**Issue:** {rec['issue']}")
                st.markdown(f"**Recommendation:** {rec['recommendation']}")
                st.markdown(f"**Impact:** {rec['impact']}")
    else:
        st.success("✅ No critical issues detected. System is operating normally!")


def show_reports(system):
    """Show system reports"""
    st.header("📄 System Reports")
    
    # Generate report button
    if st.button("Generate Comprehensive Report"):
        with st.spinner("Generating report..."):
            report = system.export_report()
            st.success("✅ Report generated successfully!")
            
            # Display report summary
            st.subheader("Report Summary")
            st.json(report['performance_metrics'])
            
            # Download button
            report_json = json.dumps(report, indent=2, default=str)
            st.download_button(
                label="📥 Download Report (JSON)",
                data=report_json,
                file_name=f"water_system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Display existing report if available
    report_path = 'data/system_report.json'
    if os.path.exists(report_path):
        st.subheader("Latest Report")
        with open(report_path, 'r') as f:
            report = json.load(f)
        
        st.markdown(f"**Generated at:** {report['generated_at']}")
        
        # Performance metrics
        st.subheader("Performance Metrics")
        metrics_df = pd.DataFrame([report['performance_metrics']])
        st.dataframe(metrics_df, use_container_width=True)
        
        # Zone health
        st.subheader("Zone Health Status")
        health_df = pd.DataFrame(report['zone_health'])
        st.dataframe(health_df, use_container_width=True)


if __name__ == '__main__':
    main()
