#!/usr/bin/env python3
"""
Baseline Rule-Based Fertilizer Recommender for Sustainable Agriculture

WARNING: This is a baseline implementation for educational and development purposes only.
DO NOT use these recommendations for actual field applications without validation from
a qualified agronomist or agricultural expert. Real-world fertilizer recommendations
require comprehensive soil analysis, crop-specific requirements, and local expertise.

This system provides simplified NPK recommendations based on basic soil parameters
and general crop requirements. It serves as a starting point for more sophisticated
ML-based recommendation systems.
"""

from typing import Dict, Tuple, Optional
import warnings


class BaselineFertilizerRecommender:
    """
    Baseline rule-based fertilizer recommender system.
    
    This class implements simple rules for fertilizer recommendations based on:
    - Target NPK levels for different crops
    - Current soil NPK levels
    - pH-based warnings
    
    Note: This is a simplified baseline system and should not be used for
    actual farming decisions without professional agronomic validation.
    """
    
    def __init__(self):
        """Initialize the recommender with crop-specific target NPK levels."""
        
        # Target NPK levels in kg/ha for different crops
        # These are general guidelines and may vary by region, variety, and conditions
        self.crop_targets = {
            'rice': {
                'N': 120,  # kg/ha
                'P': 60,   # kg/ha
                'K': 60    # kg/ha
            },
            'wheat': {
                'N': 100,  # kg/ha
                'P': 50,   # kg/ha
                'K': 40    # kg/ha
            },
            'maize': {
                'N': 150,  # kg/ha
                'P': 70,   # kg/ha
                'K': 80    # kg/ha
            },
            'cotton': {
                'N': 80,   # kg/ha
                'P': 40,   # kg/ha
                'K': 50    # kg/ha
            },
            'sugarcane': {
                'N': 200,  # kg/ha
                'P': 100,  # kg/ha
                'K': 120   # kg/ha
            }
        }
        
        # Default targets for crops not in the specific list
        self.default_targets = {
            'N': 100,  # kg/ha
            'P': 50,   # kg/ha
            'K': 50    # kg/ha
        }
        
        # pH warning thresholds
        self.ph_warning_low = 5.5
        self.ph_warning_high = 7.5
        
        # NPK efficiency factors (how much of applied fertilizer is typically available)
        self.npk_efficiency = {
            'N': 0.6,  # 60% efficiency for nitrogen
            'P': 0.3,  # 30% efficiency for phosphorus
            'K': 0.7   # 70% efficiency for potassium
        }
    
    def get_crop_targets(self, crop: str) -> Dict[str, float]:
        """
        Get target NPK levels for a specific crop.
        
        Args:
            crop (str): Crop name (case-insensitive)
            
        Returns:
            Dict[str, float]: Target NPK levels in kg/ha
        """
        crop_lower = crop.lower()
        
        if crop_lower in self.crop_targets:
            return self.crop_targets[crop_lower]
        else:
            warnings.warn(f"Crop '{crop}' not found in specific targets. Using default values.")
            return self.default_targets
    
    def calculate_npk_deficiency(self, current_npk: Dict[str, float], 
                                target_npk: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate NPK deficiency based on current vs target levels.
        
        Args:
            current_npk (Dict[str, float]): Current soil NPK levels in mg/kg
            target_npk (Dict[str, float]): Target NPK levels in kg/ha
            
        Returns:
            Dict[str, float]: NPK deficiency in kg/ha
        """
        # Convert mg/kg to kg/ha (assuming 0-20cm soil depth and 1.4 g/cm³ bulk density)
        # 1 ha = 10,000 m², depth = 0.2 m, bulk density = 1.4 g/cm³ = 1,400 kg/m³
        # Conversion factor = 10,000 × 0.2 × 1,400 / 1,000,000 = 2.8
        conversion_factor = 2.8
        
        deficiency = {}
        for nutrient in ['N', 'P', 'K']:
            current_kg_ha = current_npk.get(nutrient, 0) * conversion_factor
            target_kg_ha = target_npk.get(nutrient, 0)
            
            # Calculate deficiency (how much more is needed)
            deficiency[nutrient] = max(0, target_kg_ha - current_kg_ha)
        
        return deficiency
    
    def adjust_for_ph(self, recommendations: Dict[str, float], ph: float) -> Tuple[Dict[str, float], str]:
        """
        Adjust recommendations based on pH levels and provide warnings.
        
        Args:
            recommendations (Dict[str, float]): NPK recommendations in kg/ha
            ph (float): Soil pH value
            
        Returns:
            Tuple[Dict[str, float], str]: Adjusted recommendations and pH warning
        """
        adjusted_recs = recommendations.copy()
        ph_warning = ""
        
        if ph < self.ph_warning_low:
            ph_warning = f"⚠️  WARNING: Low pH ({ph:.1f}) detected. "
            ph_warning += "Consider lime application to raise pH before fertilizer application. "
            ph_warning += "Low pH can reduce nutrient availability and crop response to fertilizers."
            
            # Reduce P recommendation for low pH (P becomes less available)
            adjusted_recs['P'] = adjusted_recs['P'] * 1.3
            
        elif ph > self.ph_warning_high:
            ph_warning = f"⚠️  WARNING: High pH ({ph:.1f}) detected. "
            ph_warning += "Consider sulfur application to lower pH if needed. "
            ph_warning += "High pH can reduce micronutrient availability."
            
            # Reduce P recommendation for high pH (P becomes less available)
            adjusted_recs['P'] = adjusted_recs['P'] * 1.2
        
        return adjusted_recs, ph_warning
    
    def recommend_for_row(self, row: Dict) -> Dict[str, float]:
        """
        Generate fertilizer recommendations for a single soil sample.
        
        Args:
            row (Dict): Dictionary containing soil sample data with keys:
                       - 'crop': Crop name
                       - 'N': Current nitrogen level (mg/kg)
                       - 'P': Current phosphorus level (mg/kg)
                       - 'K': Current potassium level (mg/kg)
                       - 'pH': Soil pH value
                       
        Returns:
            Dict[str, float]: Fertilizer recommendations with keys:
                             - 'N_need_kg_ha': Nitrogen needed (kg/ha)
                             - 'P_need_kg_ha': Phosphorus needed (kg/ha)
                             - 'K_need_kg_ha': Potassium needed (kg/ha)
                             - 'ph_warning': pH-based warning message
        """
        # Extract data from row
        crop = row.get('crop', 'unknown')
        current_npk = {
            'N': row.get('N', 0),
            'P': row.get('P', 0),
            'K': row.get('K', 0)
        }
        ph = row.get('pH', 7.0)
        
        # Get target NPK levels for the crop
        target_npk = self.get_crop_targets(crop)
        
        # Calculate NPK deficiency
        deficiency = self.calculate_npk_deficiency(current_npk, target_npk)
        
        # Adjust for pH and get warnings
        adjusted_recommendations, ph_warning = self.adjust_for_ph(deficiency, ph)
        
        # Apply efficiency factors to get final application rates
        final_recommendations = {}
        for nutrient in ['N', 'P', 'K']:
            if adjusted_recommendations[nutrient] > 0:
                # Account for fertilizer efficiency
                final_recommendations[f'{nutrient}_need_kg_ha'] = (
                    adjusted_recommendations[nutrient] / self.npk_efficiency[nutrient]
                )
            else:
                final_recommendations[f'{nutrient}_need_kg_ha'] = 0.0
        
        # Add pH warning to recommendations
        final_recommendations['ph_warning'] = ph_warning
        
        return final_recommendations
    
    def get_recommendation_summary(self, recommendations: Dict[str, float]) -> str:
        """
        Generate a human-readable summary of fertilizer recommendations.
        
        Args:
            recommendations (Dict[str, float]): NPK recommendations
            
        Returns:
            str: Formatted recommendation summary
        """
        summary = "🌱 FERTILIZER RECOMMENDATIONS:\n"
        summary += "=" * 40 + "\n"
        
        if recommendations['N_need_kg_ha'] > 0:
            summary += f"📊 Nitrogen (N): {recommendations['N_need_kg_ha']:.1f} kg/ha\n"
        else:
            summary += "✅ Nitrogen (N): Sufficient levels detected\n"
            
        if recommendations['P_need_kg_ha'] > 0:
            summary += f"📊 Phosphorus (P): {recommendations['P_need_kg_ha']:.1f} kg/ha\n"
        else:
            summary += "✅ Phosphorus (P): Sufficient levels detected\n"
            
        if recommendations['K_need_kg_ha'] > 0:
            summary += f"📊 Potassium (K): {recommendations['K_need_ha']:.1f} kg/ha\n"
        else:
            summary += "✅ Potassium (K): Sufficient levels detected\n"
        
        if recommendations.get('ph_warning'):
            summary += f"\n{recommendations['ph_warning']}\n"
        
        summary += "\n⚠️  IMPORTANT: These are baseline recommendations only.\n"
        summary += "   Always consult with a qualified agronomist before field application.\n"
        summary += "   Local conditions, crop variety, and timing may require adjustments."
        
        return summary


def main():
    """Example usage of the baseline fertilizer recommender."""
    print("🌾 Baseline Fertilizer Recommender - Example Usage")
    print("=" * 55)
    
    # Initialize recommender
    recommender = BaselineFertilizerRecommender()
    
    # Example soil sample
    sample_soil = {
        'crop': 'wheat',
        'N': 45.0,    # mg/kg
        'P': 18.0,    # mg/kg
        'K': 95.0,    # mg/kg
        'pH': 6.2     # pH value
    }
    
    print(f"📋 Sample Soil Data:")
    print(f"   Crop: {sample_soil['crop']}")
    print(f"   N: {sample_soil['N']} mg/kg")
    print(f"   P: {sample_soil['P']} mg/kg")
    print(f"   K: {sample_soil['K']} mg/kg")
    print(f"   pH: {sample_soil['pH']}")
    
    # Get recommendations
    recommendations = recommender.recommend_for_row(sample_soil)
    
    # Display recommendations
    print("\n" + recommender.get_recommendation_summary(recommendations))


if __name__ == "__main__":
    main()
