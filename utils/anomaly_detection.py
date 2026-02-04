"""
Anomaly Detection Module
Detects anomalies in water pressure and flow data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats


class AnomalyDetector:
    """Detect anomalies in water pressure and flow data"""
    
    def __init__(self, pressure_data_path='data/pressure_data.csv',
                 flow_data_path='data/flow_data.csv'):
        """Initialize with data paths"""
        self.pressure_df = pd.read_csv(pressure_data_path)
        self.pressure_df['timestamp'] = pd.to_datetime(self.pressure_df['timestamp'])
        
        self.flow_df = pd.read_csv(flow_data_path)
        self.flow_df['timestamp'] = pd.to_datetime(self.flow_df['timestamp'])
    
    def detect_pressure_anomalies(self, threshold_std=2.5):
        """
        Detect pressure anomalies using statistical methods
        
        Args:
            threshold_std: Number of standard deviations for anomaly threshold
        
        Returns:
            DataFrame with detected anomalies
        """
        anomalies = []
        
        for zone_id in self.pressure_df['zone_id'].unique():
            zone_data = self.pressure_df[self.pressure_df['zone_id'] == zone_id].copy()
            
            # Calculate z-scores
            mean_pressure = zone_data['pressure_psi'].mean()
            std_pressure = zone_data['pressure_psi'].std()
            
            zone_data['z_score'] = np.abs(
                (zone_data['pressure_psi'] - mean_pressure) / std_pressure
            )
            
            # Identify anomalies
            zone_anomalies = zone_data[zone_data['z_score'] > threshold_std]
            
            for _, row in zone_anomalies.iterrows():
                anomalies.append({
                    'timestamp': row['timestamp'],
                    'zone_id': row['zone_id'],
                    'zone_name': row['zone_name'],
                    'sensor_id': row['sensor_id'],
                    'pressure_psi': row['pressure_psi'],
                    'expected_pressure': round(mean_pressure, 2),
                    'deviation': round(row['pressure_psi'] - mean_pressure, 2),
                    'z_score': round(row['z_score'], 2),
                    'anomaly_type': 'pressure_drop' if row['pressure_psi'] < mean_pressure else 'pressure_spike',
                    'severity': self._classify_severity(row['z_score'])
                })
        
        return pd.DataFrame(anomalies)
    
    def detect_flow_anomalies(self, threshold_std=2.0):
        """
        Detect flow rate anomalies
        
        Args:
            threshold_std: Number of standard deviations for anomaly threshold
        
        Returns:
            DataFrame with detected flow anomalies
        """
        anomalies = []
        
        # Add hour for pattern analysis
        self.flow_df['hour'] = self.flow_df['timestamp'].dt.hour
        
        for zone_id in self.flow_df['zone_id'].unique():
            zone_data = self.flow_df[self.flow_df['zone_id'] == zone_id].copy()
            
            # Analyze by hour to account for daily patterns
            for hour in range(24):
                hour_data = zone_data[zone_data['hour'] == hour]
                
                if len(hour_data) < 5:
                    continue
                
                mean_flow = hour_data['flow_rate_lpm'].mean()
                std_flow = hour_data['flow_rate_lpm'].std()
                
                if std_flow == 0:
                    continue
                
                hour_data['z_score'] = np.abs(
                    (hour_data['flow_rate_lpm'] - mean_flow) / std_flow
                )
                
                hour_anomalies = hour_data[hour_data['z_score'] > threshold_std]
                
                for _, row in hour_anomalies.iterrows():
                    anomalies.append({
                        'timestamp': row['timestamp'],
                        'zone_id': row['zone_id'],
                        'zone_name': row['zone_name'],
                        'flow_rate_lpm': row['flow_rate_lpm'],
                        'expected_flow': round(mean_flow, 2),
                        'deviation': round(row['flow_rate_lpm'] - mean_flow, 2),
                        'z_score': round(row['z_score'], 2),
                        'anomaly_type': 'excessive_flow' if row['flow_rate_lpm'] > mean_flow else 'low_flow',
                        'severity': self._classify_severity(row['z_score']),
                        'potential_cause': self._identify_cause(row['flow_rate_lpm'], mean_flow, row['hour'])
                    })
        
        return pd.DataFrame(anomalies)
    
    def detect_leaks(self, night_flow_threshold=300):
        """
        Detect potential leaks based on night-time flow patterns
        
        Args:
            night_flow_threshold: Flow rate threshold during night hours
        
        Returns:
            DataFrame with potential leak locations
        """
        # Filter night hours (0-5 AM)
        self.flow_df['hour'] = self.flow_df['timestamp'].dt.hour
        night_data = self.flow_df[
            (self.flow_df['hour'] >= 0) & (self.flow_df['hour'] <= 5)
        ]
        
        leaks = []
        
        for zone_id in night_data['zone_id'].unique():
            zone_night = night_data[night_data['zone_id'] == zone_id]
            avg_night_flow = zone_night['flow_rate_lpm'].mean()
            
            if avg_night_flow > night_flow_threshold:
                # Potential leak detected
                zone_name = zone_night['zone_name'].iloc[0]
                population = zone_night['population'].iloc[0]
                
                # Estimate daily water loss
                daily_loss = avg_night_flow * 60 * 24  # liters per day
                
                leaks.append({
                    'zone_id': zone_id,
                    'zone_name': zone_name,
                    'avg_night_flow_lpm': round(avg_night_flow, 2),
                    'estimated_daily_loss_liters': round(daily_loss, 0),
                    'estimated_monthly_loss_liters': round(daily_loss * 30, 0),
                    'severity': 'high' if avg_night_flow > 500 else 'moderate',
                    'confidence': 'high' if avg_night_flow > 400 else 'medium',
                    'recommended_action': 'Immediate inspection required' if avg_night_flow > 500 else 'Schedule inspection'
                })
        
        return pd.DataFrame(leaks)
    
    def detect_burst_events(self, pressure_drop_threshold=15):
        """
        Detect sudden pressure drops that may indicate burst pipes
        
        Args:
            pressure_drop_threshold: Minimum pressure drop to consider as burst
        
        Returns:
            DataFrame with potential burst events
        """
        bursts = []
        
        for sensor_id in self.pressure_df['sensor_id'].unique():
            sensor_data = self.pressure_df[
                self.pressure_df['sensor_id'] == sensor_id
            ].sort_values('timestamp')
            
            # Calculate pressure changes
            sensor_data['pressure_change'] = sensor_data['pressure_psi'].diff()
            
            # Detect sudden drops
            sudden_drops = sensor_data[
                sensor_data['pressure_change'] < -pressure_drop_threshold
            ]
            
            for _, row in sudden_drops.iterrows():
                bursts.append({
                    'timestamp': row['timestamp'],
                    'zone_id': row['zone_id'],
                    'zone_name': row['zone_name'],
                    'sensor_id': row['sensor_id'],
                    'pressure_before': round(row['pressure_psi'] - row['pressure_change'], 2),
                    'pressure_after': round(row['pressure_psi'], 2),
                    'pressure_drop': round(abs(row['pressure_change']), 2),
                    'severity': 'critical' if abs(row['pressure_change']) > 25 else 'high',
                    'event_type': 'potential_burst',
                    'recommended_action': 'Emergency response required'
                })
        
        return pd.DataFrame(bursts)
    
    def _classify_severity(self, z_score):
        """Classify anomaly severity based on z-score"""
        if z_score > 4:
            return 'critical'
        elif z_score > 3:
            return 'high'
        elif z_score > 2.5:
            return 'moderate'
        else:
            return 'low'
    
    def _identify_cause(self, actual_flow, expected_flow, hour):
        """Identify potential cause of flow anomaly"""
        if actual_flow > expected_flow * 1.5:
            if 0 <= hour <= 5:
                return 'Potential leak (high night flow)'
            else:
                return 'Unusual high demand or unauthorized usage'
        else:
            return 'Supply interruption or valve issue'
    
    def get_anomaly_summary(self):
        """Get summary of all detected anomalies"""
        pressure_anomalies = self.detect_pressure_anomalies()
        flow_anomalies = self.detect_flow_anomalies()
        leaks = self.detect_leaks()
        bursts = self.detect_burst_events()
        
        summary = {
            'total_pressure_anomalies': len(pressure_anomalies),
            'total_flow_anomalies': len(flow_anomalies),
            'potential_leaks': len(leaks),
            'potential_bursts': len(bursts),
            'critical_events': len(pressure_anomalies[pressure_anomalies['severity'] == 'critical']) + 
                             len(bursts[bursts['severity'] == 'critical'])
        }
        
        return summary, pressure_anomalies, flow_anomalies, leaks, bursts


if __name__ == '__main__':
    detector = AnomalyDetector()
    summary, _, _, leaks, _ = detector.get_anomaly_summary()
    print("Anomaly Summary:", summary)
    print("\nPotential Leaks:")
    print(leaks)
