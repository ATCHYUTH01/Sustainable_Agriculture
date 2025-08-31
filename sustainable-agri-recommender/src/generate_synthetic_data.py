#!/usr/bin/env python3
"""
Generate synthetic soil testing data for the Sustainable Agriculture Recommender project.
Creates 500 soil samples with realistic agricultural parameters.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path


def generate_synthetic_soil_data(n_samples=500, random_seed=42):
    """
    Generate synthetic soil testing data.
    
    Args:
        n_samples (int): Number of soil samples to generate
        random_seed (int): Random seed for reproducibility
    
    Returns:
        pd.DataFrame: DataFrame containing synthetic soil data
    """
    # Set random seed for reproducibility
    np.random.seed(random_seed)
    
    # Generate sample IDs
    sample_ids = [f"SOIL_{i:04d}" for i in range(1, n_samples + 1)]
    
    # Generate realistic soil parameters
    # pH: typically ranges from 4.5 to 8.5 for agricultural soils
    ph_values = np.random.normal(6.5, 1.0, n_samples)
    ph_values = np.clip(ph_values, 4.5, 8.5)
    
    # Nitrogen (N) in mg/kg - typical range 10-200
    nitrogen = np.random.normal(80, 40, n_samples)
    nitrogen = np.clip(nitrogen, 10, 200)
    
    # Phosphorus (P) in mg/kg - typical range 5-100
    phosphorus = np.random.normal(30, 20, n_samples)
    phosphorus = np.clip(phosphorus, 5, 100)
    
    # Potassium (K) in mg/kg - typical range 50-300
    potassium = np.random.normal(150, 60, n_samples)
    potassium = np.clip(potassium, 50, 300)
    
    # Organic carbon in % - typical range 0.5-5.0
    organic_carbon = np.random.normal(2.0, 1.0, n_samples)
    organic_carbon = np.clip(organic_carbon, 0.5, 5.0)
    
    # Moisture content in % - typical range 10-40
    moisture = np.random.normal(25, 8, n_samples)
    moisture = np.clip(moisture, 10, 40)
    
    # Crop types with realistic distribution
    crops = ['wheat', 'corn', 'soybeans', 'rice', 'cotton', 'vegetables', 'fruits', 'legumes']
    crop_weights = [0.25, 0.20, 0.15, 0.10, 0.10, 0.10, 0.05, 0.05]  # Realistic crop distribution
    crop_values = np.random.choice(crops, n_samples, p=crop_weights)
    
    # Create DataFrame
    data = {
        'sample_id': sample_ids,
        'pH': np.round(ph_values, 2),
        'N': np.round(nitrogen, 1),
        'P': np.round(phosphorus, 1),
        'K': np.round(potassium, 1),
        'organic_carbon': np.round(organic_carbon, 2),
        'moisture': np.round(moisture, 1),
        'crop': crop_values
    }
    
    df = pd.DataFrame(data)
    
    return df


def save_data_to_csv(df, output_path):
    """
    Save the DataFrame to CSV file.
    
    Args:
        df (pd.DataFrame): DataFrame to save
        output_path (str): Path where to save the CSV file
    """
    # Ensure the directory exists
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"✅ Data saved successfully to: {output_path}")
    print(f"📊 Generated {len(df)} soil samples")
    print(f"📁 File size: {os.path.getsize(output_path) / 1024:.1f} KB")


def main():
    """Main function to generate and save synthetic soil data."""
    print("🌱 Generating synthetic soil testing data...")
    print("=" * 50)
    
    # Generate data
    soil_data = generate_synthetic_soil_data(n_samples=500, random_seed=42)
    
    # Display sample statistics
    print("\n📈 Data Summary:")
    print(f"Total samples: {len(soil_data)}")
    print(f"pH range: {soil_data['pH'].min():.2f} - {soil_data['pH'].max():.2f}")
    print(f"N range: {soil_data['N'].min():.1f} - {soil_data['N'].max():.1f} mg/kg")
    print(f"P range: {soil_data['P'].min():.1f} - {soil_data['P'].max():.1f} mg/kg")
    print(f"K range: {soil_data['K'].min():.1f} - {soil_data['K'].max():.1f} mg/kg")
    print(f"Organic carbon range: {soil_data['organic_carbon'].min():.2f} - {soil_data['organic_carbon'].max():.2f}%")
    print(f"Moisture range: {soil_data['moisture'].min():.1f} - {soil_data['moisture'].max():.1f}%")
    
    print("\n🌾 Crop distribution:")
    crop_counts = soil_data['crop'].value_counts()
    for crop, count in crop_counts.items():
        percentage = (count / len(soil_data)) * 100
        print(f"  {crop}: {count} samples ({percentage:.1f}%)")
    
    # Save to CSV
    output_path = "data/raw/soil_samples_synthetic_week1.csv"
    save_data_to_csv(soil_data, output_path)
    
    # Display first few rows
    print("\n🔍 First 5 samples:")
    print(soil_data.head().to_string(index=False))
    
    print("\n🎯 Data generation complete!")
    print("💡 Next step: Run notebooks/01_EDA_and_baseline.ipynb for analysis")


if __name__ == "__main__":
    main()
