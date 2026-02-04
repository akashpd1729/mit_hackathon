"""
Analytics Module
Provides analytical functions for water pressure and flow data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class WaterAnalytics:
    """Analytics for water pressure and flow data"""
    
    def __init__(self, pressure_data_path='data/pressure_data.csv', 
                 flow_data_path='data/flow_data.csv'):
        """Initialize with data paths"""
        self.pressure_df = pd.read_csv(pressure_data_path)
        self.pressure_df['timestamp'] = pd.to_datetime(self.pressure_df['timestamp'])
        
        self.flow_df = pd.read_csv(flow_data_path)
        self.flow_df['timestamp'] = pd.to_datetime(self.flow_df['timestamp'])
    
    def get_zone_statistics(self):
        """Calculate statistics for each zone"""
        stats = self.pressure_df.groupby('zone_name').agg({
            'pressure_psi': ['mean', 'min', 'max', 'std'],
            'sensor_id': 'nunique'
        }).round(2)
        
        stats.columns = ['avg_pressure', 'min_pressure', 'max_pressure', 
                        'std_pressure', 'num_sensors']
        stats = stats.reset_index()
        
        return stats
    
    def get_hourly_patterns(self):
        """Analyze hourly consumption patterns"""
        self.pressure_df['hour'] = self.pressure_df['timestamp'].dt.hour
        
        hourly = self.pressure_df.groupby('hour').agg({
            'pressure_psi': 'mean'
        }).round(2).reset_index()
        
        return hourly
    
    def get_zone_comparison(self):
        """Compare zones by average pressure"""
        comparison = self.pressure_df.groupby('zone_name').agg({
            'pressure_psi': 'mean',
            'elevation': 'first'
        }).round(2).reset_index()
        
        comparison = comparison.sort_values('pressure_psi', ascending=False)
        return comparison
    
    def get_low_pressure_zones(self, threshold=35):
        """Identify zones with low pressure issues"""
        recent_data = self.pressure_df[
            self.pressure_df['timestamp'] >= 
            (datetime.now() - timedelta(days=7))
        ]
        
        low_pressure = recent_data[recent_data['pressure_psi'] < threshold]
        
        summary = low_pressure.groupby('zone_name').agg({
            'pressure_psi': ['count', 'mean'],
            'zone_id': 'first'
        }).round(2)
        
        summary.columns = ['low_pressure_count', 'avg_low_pressure', 'zone_id']
        summary = summary.reset_index()
        summary = summary.sort_values('low_pressure_count', ascending=False)
        
        return summary
    
    def get_flow_statistics(self):
        """Calculate flow statistics by zone"""
        flow_stats = self.flow_df.groupby('zone_name').agg({
            'flow_rate_lpm': ['mean', 'min', 'max', 'sum'],
            'population': 'first'
        }).round(2)
        
        flow_stats.columns = ['avg_flow', 'min_flow', 'max_flow', 
                             'total_flow', 'population']
        flow_stats = flow_stats.reset_index()
        
        # Calculate per capita consumption
        flow_stats['per_capita_flow'] = (
            flow_stats['avg_flow'] / flow_stats['population'] * 1000
        ).round(4)
        
        return flow_stats
    
    def get_peak_demand_times(self):
        """Identify peak demand times"""
        self.flow_df['hour'] = self.flow_df['timestamp'].dt.hour
        
        hourly_flow = self.flow_df.groupby('hour').agg({
            'flow_rate_lpm': 'mean'
        }).round(2).reset_index()
        
        hourly_flow = hourly_flow.sort_values('flow_rate_lpm', ascending=False)
        return hourly_flow
    
    def get_recent_trends(self, days=7):
        """Get recent pressure trends"""
        recent_data = self.pressure_df[
            self.pressure_df['timestamp'] >= 
            (datetime.now() - timedelta(days=days))
        ]
        
        recent_data['date'] = recent_data['timestamp'].dt.date
        
        trends = recent_data.groupby(['date', 'zone_name']).agg({
            'pressure_psi': 'mean'
        }).round(2).reset_index()
        
        return trends
    
    def calculate_water_loss(self):
        """Estimate water loss based on flow anomalies"""
        # Calculate expected vs actual flow
        self.flow_df['hour'] = self.flow_df['timestamp'].dt.hour
        
        # Expected flow during night hours (0-5 AM) should be low
        night_flow = self.flow_df[
            (self.flow_df['hour'] >= 0) & (self.flow_df['hour'] <= 5)
        ]
        
        loss_estimate = night_flow.groupby('zone_name').agg({
            'flow_rate_lpm': 'mean'
        }).round(2).reset_index()
        
        loss_estimate.columns = ['zone_name', 'night_flow_lpm']
        
        # High night flow indicates potential leakage
        loss_estimate['potential_leak'] = loss_estimate['night_flow_lpm'] > 200
        loss_estimate['estimated_daily_loss_liters'] = (
            loss_estimate['night_flow_lpm'] * 60 * 24 * 0.3
        ).round(0)
        
        return loss_estimate
    
    def get_pressure_distribution(self):
        """Get pressure distribution across all zones"""
        distribution = self.pressure_df.groupby(
            pd.cut(self.pressure_df['pressure_psi'], 
                   bins=[0, 30, 40, 50, 60, 100],
                   labels=['Very Low (<30)', 'Low (30-40)', 
                          'Normal (40-50)', 'Good (50-60)', 'High (>60)'])
        ).size().reset_index()
        
        distribution.columns = ['pressure_range', 'count']
        return distribution


if __name__ == '__main__':
    analytics = WaterAnalytics()
    print("Zone Statistics:")
    print(analytics.get_zone_statistics())
