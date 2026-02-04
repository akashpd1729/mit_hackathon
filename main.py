"""
Main Module for Smart Water Pressure Management System
Core functionality and data processing
"""

import os
import sys
import pandas as pd
import json
from datetime import datetime

# Add utils to path
sys.path.append(os.path.dirname(__file__))

from utils.data_generator import WaterDataGenerator
from utils.analytics import WaterAnalytics
from utils.anomaly_detection import AnomalyDetector


class SmartWaterManagementSystem:
    """Main system class for water pressure management"""
    
    def __init__(self, data_dir='data'):
        """Initialize the system"""
        self.data_dir = data_dir
        self.zones_config_path = os.path.join(data_dir, 'zones_config.json')
        self.pressure_data_path = os.path.join(data_dir, 'pressure_data.csv')
        self.flow_data_path = os.path.join(data_dir, 'flow_data.csv')
        
        # Load zones configuration
        with open(self.zones_config_path, 'r') as f:
            self.zones_config = json.load(f)
        
        # Initialize components
        self.analytics = None
        self.anomaly_detector = None
        
        # Check if data exists
        self._check_data()
    
    def _check_data(self):
        """Check if data files exist, generate if not"""
        if not os.path.exists(self.pressure_data_path) or \
           not os.path.exists(self.flow_data_path):
            print("Data files not found. Generating synthetic data...")
            self.generate_data()
        else:
            print("Data files found. Loading existing data...")
            self._load_components()
    
    def generate_data(self, days=30):
        """Generate synthetic data"""
        generator = WaterDataGenerator(self.zones_config_path)
        generator.save_all_data(self.data_dir)
        print("✓ Data generation complete")
        self._load_components()
    
    def _load_components(self):
        """Load analytics and anomaly detection components"""
        self.analytics = WaterAnalytics(
            self.pressure_data_path,
            self.flow_data_path
        )
        self.anomaly_detector = AnomalyDetector(
            self.pressure_data_path,
            self.flow_data_path
        )
    
    def get_system_overview(self):
        """Get overall system overview"""
        zones = self.zones_config['zones']
        
        overview = {
            'total_zones': len(zones),
            'total_population': sum(z['population'] for z in zones),
            'total_sensors': sum(z['num_sensors'] for z in zones),
            'zones': zones
        }
        
        return overview
    
    def get_zone_health_status(self):
        """Get health status for all zones"""
        stats = self.analytics.get_zone_statistics()
        low_pressure_zones = self.analytics.get_low_pressure_zones()
        
        # Merge data
        health_status = []
        for _, zone in stats.iterrows():
            zone_name = zone['zone_name']
            
            # Check if zone has low pressure issues
            low_pressure_info = low_pressure_zones[
                low_pressure_zones['zone_name'] == zone_name
            ]
            
            if len(low_pressure_info) > 0:
                status = 'critical' if low_pressure_info['low_pressure_count'].iloc[0] > 100 else 'warning'
            elif zone['avg_pressure'] < 35:
                status = 'warning'
            elif zone['avg_pressure'] < 40:
                status = 'attention'
            else:
                status = 'healthy'
            
            health_status.append({
                'zone_name': zone_name,
                'avg_pressure': zone['avg_pressure'],
                'status': status,
                'num_sensors': zone['num_sensors']
            })
        
        return pd.DataFrame(health_status)
    
    def detect_all_anomalies(self):
        """Detect all types of anomalies"""
        summary, pressure_anomalies, flow_anomalies, leaks, bursts = \
            self.anomaly_detector.get_anomaly_summary()
        
        return {
            'summary': summary,
            'pressure_anomalies': pressure_anomalies,
            'flow_anomalies': flow_anomalies,
            'leaks': leaks,
            'bursts': bursts
        }
    
    def get_recommendations(self):
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Check for low pressure zones
        low_pressure = self.analytics.get_low_pressure_zones()
        for _, zone in low_pressure.iterrows():
            if zone['low_pressure_count'] > 50:
                recommendations.append({
                    'priority': 'high',
                    'zone': zone['zone_name'],
                    'issue': 'Frequent low pressure',
                    'recommendation': 'Install booster pumps or check for leaks',
                    'impact': f"{zone['low_pressure_count']} low pressure events detected"
                })
        
        # Check for potential leaks
        leaks = self.anomaly_detector.detect_leaks()
        for _, leak in leaks.iterrows():
            recommendations.append({
                'priority': leak['severity'],
                'zone': leak['zone_name'],
                'issue': 'Potential water leak',
                'recommendation': leak['recommended_action'],
                'impact': f"Estimated loss: {leak['estimated_daily_loss_liters']:,.0f} liters/day"
            })
        
        # Check for burst events
        bursts = self.anomaly_detector.detect_burst_events()
        for _, burst in bursts.iterrows():
            recommendations.append({
                'priority': 'critical',
                'zone': burst['zone_name'],
                'issue': 'Potential pipe burst',
                'recommendation': burst['recommended_action'],
                'impact': f"Pressure drop: {burst['pressure_drop']} PSI"
            })
        
        return pd.DataFrame(recommendations) if recommendations else pd.DataFrame()
    
    def get_performance_metrics(self):
        """Calculate system performance metrics"""
        stats = self.analytics.get_zone_statistics()
        flow_stats = self.analytics.get_flow_statistics()
        water_loss = self.analytics.calculate_water_loss()
        
        metrics = {
            'avg_system_pressure': round(stats['avg_pressure'].mean(), 2),
            'total_water_flow': round(flow_stats['total_flow'].sum(), 2),
            'zones_with_issues': len(stats[stats['avg_pressure'] < 40]),
            'estimated_water_loss_percent': round(
                (water_loss['estimated_daily_loss_liters'].sum() / 
                 flow_stats['total_flow'].sum()) * 100, 2
            ),
            'system_efficiency': round(
                100 - (water_loss['estimated_daily_loss_liters'].sum() / 
                       flow_stats['total_flow'].sum()) * 100, 2
            )
        }
        
        return metrics
    
    def export_report(self, output_path='data/system_report.json'):
        """Export comprehensive system report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'overview': self.get_system_overview(),
            'performance_metrics': self.get_performance_metrics(),
            'zone_health': self.get_zone_health_status().to_dict('records'),
            'anomalies': {
                'summary': self.anomaly_detector.get_anomaly_summary()[0]
            },
            'recommendations': self.get_recommendations().to_dict('records')
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"✓ Report exported to {output_path}")
        return report


def main():
    """Main execution function"""
    print("=" * 60)
    print("Smart Water Pressure Management System")
    print("Solapur Municipal Corporation")
    print("=" * 60)
    
    # Initialize system
    system = SmartWaterManagementSystem()
    
    # Get overview
    print("\n📊 System Overview:")
    overview = system.get_system_overview()
    print(f"Total Zones: {overview['total_zones']}")
    print(f"Total Population Served: {overview['total_population']:,}")
    print(f"Total Sensors: {overview['total_sensors']}")
    
    # Get performance metrics
    print("\n📈 Performance Metrics:")
    metrics = system.get_performance_metrics()
    for key, value in metrics.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    # Get zone health
    print("\n🏥 Zone Health Status:")
    health = system.get_zone_health_status()
    print(health.to_string(index=False))
    
    # Get recommendations
    print("\n💡 Recommendations:")
    recommendations = system.get_recommendations()
    if len(recommendations) > 0:
        print(recommendations[['priority', 'zone', 'issue', 'recommendation']].to_string(index=False))
    else:
        print("No critical issues detected.")
    
    # Export report
    print("\n📄 Exporting comprehensive report...")
    system.export_report()
    
    print("\n✓ System check complete!")


if __name__ == '__main__':
    main()
