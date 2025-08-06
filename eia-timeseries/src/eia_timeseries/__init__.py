from .data_collector import EnergyWeatherCollector
from .analyzer import EnergyWeatherAnalyzer
from .config import REGIONS, get_date_range

def main() -> None:
    """Main application entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EIA Energy-Weather Analysis Tool")
    parser.add_argument("--region", choices=list(REGIONS.keys()), 
                       default="ciso_pgae", help="Energy region to analyze")
    parser.add_argument("--days", type=int, default=7, 
                       help="Number of days of data to collect")
    parser.add_argument("--output", help="Output file for results (optional)")
    
    args = parser.parse_args()
    
    # Get date range
    start_date, end_date = get_date_range(args.days)
    
    try:
        # Collect data
        collector = EnergyWeatherCollector(args.region)
        eia_data, weather_data = collector.collect_data(start_date, end_date)
        
        # Merge datasets
        merged_data = collector.merge_datasets(eia_data, weather_data)
        print(f"Merged dataset shape: {merged_data.shape}")
        
        # Analyze
        analyzer = EnergyWeatherAnalyzer(merged_data)
        report = analyzer.generate_report()
        
        print("\n" + report)
        
        # Save if requested
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"\nReport saved to {args.output}")
        
        # Save data
        data_file = f"energy_weather_data_{args.region}_{start_date}_to_{end_date}.csv"
        merged_data.to_csv(data_file, index=False)
        print(f"Data saved to {data_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())