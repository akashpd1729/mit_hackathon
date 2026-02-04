"""
Data Generator Module
Generates synthetic water pressure and flow data for the Smart Water Management System
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os


class WaterDataGenerator:
    """Generate synthetic water pressure and flow data"""
    
    def __init__(self, zones_config_path='data/zones_config.json'):
        """Initialize with zones configuration"""
        with open(zones_config_path, 'r') as f:
            self.config = json.load(f)
        self.zones = self.config['zones']
    
    def generate_pressure_data(self, days=30, interval_minutes=15):
        """
        Generate synthetic pressure data for all zones
        
        Args:
            days: Number of days to generate data for
            interval_minutes: Time interval between readings
        
        Returns:
            DataFrame with pressure readings
        """
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for zone in self.zones:
            zone_id = zone['zone_id']
            zone_name = zone['zone_name']
            base_pressure = zone['base_pressure']
            elevation = zone['elevation']
            num_sensors = zone['num_sensors']
            
            # Generate timestamps
            timestamps = pd.date_range(
                start=start_date,
                periods=int(days * 24 * 60 / interval_minutes),
                freq=f'{interval_minutes}min'
            )
            
            for sensor_id in range(1, num_sensors + 1):
                for timestamp in timestamps:
                    hour = timestamp.hour
                    
                    # Simulate daily patterns (peak hours: 6-9 AM, 6-9 PM)
                    if 6 <= hour <= 9 or 18 <= hour <= 21:
                        demand_factor = 0.85  # High demand = lower pressure
                    elif 0 <= hour <= 5:
                        demand_factor = 1.15  # Low demand = higher pressure
                    else:
                        demand_factor = 1.0
                    
                    # Base pressure with variations
                    pressure = base_pressure * demand_factor
                    
                    # Add random noise
                    pressure += np.random.normal(0, 2)
                    
                    # Simulate occasional anomalies (leaks, bursts)
                    if np.random.random() < 0.02:  # 2% chance of anomaly
                        pressure *= np.random.uniform(0.5, 0.8)  # Pressure drop
                    
                    # Elevation impact
                    elevation_impact = -0.1 * (elevation - 100) / 10
                    pressure += elevation_impact
                    
                    # Ensure pressure is positive
                    pressure = max(pressure, 5.0)
                    
                    data.append({
                        'timestamp': timestamp,
                        'zone_id': zone_id,
                        'zone_name': zone_name,
                        'sensor_id': f'{zone_id}_S{sensor_id:02d}',
                        'pressure_psi': round(pressure, 2),
                        'elevation': elevation,
                        'status': 'normal' if pressure > base_pressure * 0.7 else 'low'
                    })
        
        return pd.DataFrame(data)
    
    def generate_flow_data(self, days=30, interval_minutes=15):
        """
        Generate synthetic flow rate data
        
        Args:
            days: Number of days to generate data for
            interval_minutes: Time interval between readings
        
        Returns:
            DataFrame with flow readings
        """
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for zone in self.zones:
            zone_id = zone['zone_id']
            zone_name = zone['zone_name']
            population = zone['population']
            
            # Base flow rate (liters per minute) - proportional to population
            base_flow = population / 100  # Rough estimate
            
            timestamps = pd.date_range(
                start=start_date,
                periods=int(days * 24 * 60 / interval_minutes),
                freq=f'{interval_minutes}min'
            )
            
            for timestamp in timestamps:
                hour = timestamp.hour
                
                # Daily consumption patterns
                if 6 <= hour <= 9:
                    flow_factor = 1.5  # Morning peak
                elif 18 <= hour <= 21:
                    flow_factor = 1.4  # Evening peak
                elif 0 <= hour <= 5:
                    flow_factor = 0.3  # Night low
                else:
                    flow_factor = 0.8
                
                flow_rate = base_flow * flow_factor
                flow_rate += np.random.normal(0, base_flow * 0.1)
                
                # Simulate leakage (constant unexpected flow)
                if np.random.random() < 0.01:  # 1% chance of leak
                    flow_rate *= np.random.uniform(1.3, 1.8)
                
                flow_rate = max(flow_rate, 0)
                
                data.append({
                    'timestamp': timestamp,
                    'zone_id': zone_id,
                    'zone_name': zone_name,
                    'flow_rate_lpm': round(flow_rate, 2),
                    'population': population
                })
        
        return pd.DataFrame(data)
    
    def generate_leak_events(self, num_events=20):
        """Generate synthetic leak event data"""
        data = []
        
        for i in range(num_events):
            zone = np.random.choice(self.zones)
            event_date = datetime.now() - timedelta(days=np.random.randint(1, 30))
            
            severity = np.random.choice(['minor', 'moderate', 'severe'], p=[0.6, 0.3, 0.1])
            
            data.append({
                'event_id': f'LEAK_{i+1:03d}',
                'timestamp': event_date,
                'zone_id': zone['zone_id'],
                'zone_name': zone['zone_name'],
                'severity': severity,
                'estimated_loss_liters': np.random.randint(1000, 50000),
                'status': np.random.choice(['detected', 'resolved'], p=[0.3, 0.7]),
                'response_time_hours': round(np.random.uniform(0.5, 24), 2)
            })
        
        return pd.DataFrame(data)
    
    def save_all_data(self, output_dir='data'):
        """Generate and save all synthetic data"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("Generating pressure data...")
        pressure_df = self.generate_pressure_data(days=30)
        pressure_df.to_csv(f'{output_dir}/pressure_data.csv', index=False)
        print(f"✓ Saved {len(pressure_df)} pressure records")
        
        print("Generating flow data...")
        flow_df = self.generate_flow_data(days=30)
        flow_df.to_csv(f'{output_dir}/flow_data.csv', index=False)
        print(f"✓ Saved {len(flow_df)} flow records")
        
        print("Generating leak events...")
        leak_df = self.generate_leak_events(num_events=20)
        leak_df.to_csv(f'{output_dir}/leak_events.csv', index=False)
        print(f"✓ Saved {len(leak_df)} leak events")
        
        return pressure_df, flow_df, leak_df


if __name__ == '__main__':
    generator = WaterDataGenerator()
    generator.save_all_data()
