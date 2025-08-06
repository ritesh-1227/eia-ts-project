# src/eia_timeseries/analyzer.py
import pandas as pd
import numpy as np
from typing import Dict, Any

class EnergyWeatherAnalyzer:
    """Analyzes correlations between energy demand and weather patterns"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.analysis_results = {}
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare data for analysis by handling data types"""
        # Convert timestamp to datetime if not already
        if 'timestamp' in self.data.columns:
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        
        # Ensure numeric columns are properly typed
        numeric_candidates = ['value', 'temperature_2m', 'relative_humidity_2m', 
                            'wind_speed_10m', 'shortwave_radiation']
        
        for col in numeric_candidates:
            if col in self.data.columns:
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
        
        # Remove rows with all NaN values in numeric columns
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        self.data = self.data.dropna(subset=numeric_cols, how='all')
        
        print(f"Data prepared: {len(self.data)} rows, {len(numeric_cols)} numeric columns")
    
    def basic_stats(self) -> Dict[str, Any]:
        """Calculate basic statistics for energy and weather variables"""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return {'error': 'No numeric columns found for analysis'}
        
        try:
            stats = {
                'summary': self.data[numeric_cols].describe(),
                'correlations': self.data[numeric_cols].corr(),
                'energy_weather_corr': self._energy_weather_correlations()
            }
            
            self.analysis_results['basic_stats'] = stats
            return stats
            
        except Exception as e:
            return {'error': f'Error calculating basic stats: {str(e)}'}
    
    def _energy_weather_correlations(self) -> Dict[str, float]:
        """Calculate correlations between energy value and weather variables"""
        if 'value' not in self.data.columns:
            return {'error': 'No energy value column found'}
        
        # Convert value column to numeric if not already
        energy_values = pd.to_numeric(self.data['value'], errors='coerce')
        
        weather_cols = [col for col in self.data.columns 
                       if any(w in col.lower() for w in ['temperature', 'humidity', 'wind', 'shortwave', 'radiation'])]
        
        correlations = {}
        for col in weather_cols:
            if col in self.data.columns:
                try:
                    weather_values = pd.to_numeric(self.data[col], errors='coerce')
                    corr = energy_values.corr(weather_values)
                    if not np.isnan(corr):
                        correlations[col] = round(corr, 4)
                except Exception as e:
                    correlations[col] = f'Error: {str(e)}'
        
        return correlations
    
    def hourly_patterns(self) -> Dict[str, Any]:
        """Analyze hourly patterns in energy demand and weather"""
        if 'timestamp' not in self.data.columns:
            return {'error': 'No timestamp column found'}
        
        try:
            self.data['hour'] = self.data['timestamp'].dt.hour
            
            hourly_stats = {}
            
            # Energy patterns by hour
            if 'value' in self.data.columns:
                energy_values = pd.to_numeric(self.data['value'], errors='coerce')
                hourly_stats['energy_by_hour'] = self.data.groupby('hour')['value'].agg(['mean', 'std', 'count'])
            
            # Temperature patterns by hour if available
            temp_cols = [col for col in self.data.columns if 'temperature' in col.lower()]
            if temp_cols and len(temp_cols) > 0:
                temp_col = temp_cols[0]
                temp_values = pd.to_numeric(self.data[temp_col], errors='coerce')
                hourly_stats['temp_by_hour'] = self.data.groupby('hour')[temp_col].mean()
            
            self.analysis_results['hourly_patterns'] = hourly_stats
            return hourly_stats
            
        except Exception as e:
            return {'error': f'Error calculating hourly patterns: {str(e)}'}
    
    def data_quality_check(self) -> Dict[str, Any]:
        """Check data quality and completeness"""
        quality_info = {
            'total_rows': len(self.data),
            'columns': list(self.data.columns),
            'missing_data': {},
            'data_types': {},
            'time_range': {}
        }
        
        # Missing data analysis
        for col in self.data.columns:
            missing_count = self.data[col].isnull().sum()
            quality_info['missing_data'][col] = {
                'count': int(missing_count),
                'percentage': round((missing_count / len(self.data)) * 100, 2)
            }
        
        # Data types
        for col in self.data.columns:
            quality_info['data_types'][col] = str(self.data[col].dtype)
        
        # Time range analysis
        if 'timestamp' in self.data.columns:
            timestamps = pd.to_datetime(self.data['timestamp'])
            quality_info['time_range'] = {
                'start': str(timestamps.min()),
                'end': str(timestamps.max()),
                'duration_hours': (timestamps.max() - timestamps.min()).total_seconds() / 3600
            }
        
        return quality_info
    
    def generate_report(self) -> str:
        """Generate a summary report of the analysis"""
        report = []
        report.append("=== Energy-Weather Analysis Report ===\n")
        
        # Data quality check
        quality = self.data_quality_check()
        report.append(f"Dataset: {quality['total_rows']} rows, {len(quality['columns'])} columns")
        
        if 'time_range' in quality and quality['time_range']:
            report.append(f"Time range: {quality['time_range'].get('start', 'Unknown')} to {quality['time_range'].get('end', 'Unknown')}")
            report.append(f"Duration: {quality['time_range'].get('duration_hours', 0):.1f} hours")
        
        if 'region' in self.data.columns and len(self.data) > 0:
            report.append(f"Region: {self.data['region'].iloc[0]}")
        
        report.append("")
        
        # Basic statistics
        try:
            stats = self.basic_stats()
            if 'error' not in stats and 'energy_weather_corr' in stats:
                corr_data = stats['energy_weather_corr']
                if corr_data and 'error' not in corr_data:
                    report.append("Energy-Weather Correlations:")
                    for var, corr in corr_data.items():
                        if isinstance(corr, (int, float)):
                            report.append(f"  {var}: {corr:.3f}")
                        else:
                            report.append(f"  {var}: {corr}")
                    report.append("")
        except Exception as e:
            report.append(f"Error in correlation analysis: {str(e)}\n")
        
        # Key insights
        try:
            report.append("Key Insights:")
            if 'value' in self.data.columns:
                energy_values = pd.to_numeric(self.data['value'], errors='coerce').dropna()
                if len(energy_values) > 0:
                    avg_demand = energy_values.mean()
                    peak_demand = energy_values.max()
                    min_demand = energy_values.min()
                    report.append(f"  Average energy demand: {avg_demand:.2f}")
                    report.append(f"  Peak energy demand: {peak_demand:.2f}")
                    report.append(f"  Minimum energy demand: {min_demand:.2f}")
            
            # Weather insights
            temp_cols = [col for col in self.data.columns if 'temperature' in col.lower()]
            if temp_cols:
                temp_col = temp_cols[0]
                temp_values = pd.to_numeric(self.data[temp_col], errors='coerce').dropna()
                if len(temp_values) > 0:
                    avg_temp = temp_values.mean()
                    report.append(f"  Average temperature: {avg_temp:.1f}°C")
        
        except Exception as e:
            report.append(f"Error generating insights: {str(e)}")
        
        # Data quality summary
        report.append("\nData Quality:")
        missing_summary = []
        for col, info in quality['missing_data'].items():
            if info['count'] > 0:
                missing_summary.append(f"{col}: {info['percentage']:.1f}% missing")
        
        if missing_summary:
            report.append("  Missing data: " + ", ".join(missing_summary))
        else:
            report.append("  No missing data detected")
        
        return "\n".join(report)