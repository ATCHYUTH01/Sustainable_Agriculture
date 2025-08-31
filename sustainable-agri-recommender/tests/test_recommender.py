#!/usr/bin/env python3
"""
Tests for the Baseline Fertilizer Recommender system.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from recommender import BaselineFertilizerRecommender


class TestBaselineFertilizerRecommender(unittest.TestCase):
    """Test cases for the BaselineFertilizerRecommender class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.recommender = BaselineFertilizerRecommender()
    
    def test_rice_sample_recommendations(self):
        """
        Test fertilizer recommendations for a rice sample with specific NPK and pH values.
        
        Test case: rice sample with N=50, P=10, K=20, pH=6.5
        Expected: N_need_kg_ha >= 0 and no pH warning
        """
        # Test soil sample data
        rice_sample = {
            'crop': 'rice',
            'N': 50.0,    # mg/kg
            'P': 10.0,    # mg/kg
            'K': 20.0,    # mg/kg
            'pH': 6.5     # pH value
        }
        
        # Get recommendations
        recommendations = self.recommender.recommend_for_row(rice_sample)
        
        # Test that N_need_kg_ha >= 0
        self.assertGreaterEqual(
            recommendations['N_need_kg_ha'], 
            0, 
            "Nitrogen recommendation should be >= 0"
        )
        
        # Test that P_need_kg_ha >= 0
        self.assertGreaterEqual(
            recommendations['P_need_kg_ha'], 
            0, 
            "Phosphorus recommendation should be >= 0"
        )
        
        # Test that K_need_kg_ha >= 0
        self.assertGreaterEqual(
            recommendations['K_need_kg_ha'], 
            0, 
            "Potassium recommendation should be >= 0"
        )
        
        # Test that pH warning is empty (no pH adjustment needed)
        self.assertEqual(
            recommendations['ph_warning'], 
            "", 
            "pH warning should be empty for pH=6.5 (within normal range)"
        )
        
        # Test that all required keys are present
        required_keys = ['N_need_kg_ha', 'P_need_kg_ha', 'K_need_ha', 'ph_warning']
        for key in required_keys:
            self.assertIn(
                key, 
                recommendations, 
                f"Recommendations should contain key: {key}"
            )
        
        # Test that recommendations are numeric values
        self.assertIsInstance(
            recommendations['N_need_kg_ha'], 
            (int, float), 
            "N_need_kg_ha should be numeric"
        )
        self.assertIsInstance(
            recommendations['P_need_kg_ha'], 
            (int, float), 
            "P_need_kg_ha should be numeric"
        )
        self.assertIsInstance(
            recommendations['K_need_ha'], 
            (int, float), 
            "K_need_ha should be numeric"
        )
        
        # Test that pH warning is a string
        self.assertIsInstance(
            recommendations['ph_warning'], 
            str, 
            "ph_warning should be a string"
        )
    
    def test_crop_targets_retrieval(self):
        """Test that crop-specific target NPK levels are correctly retrieved."""
        # Test rice targets
        rice_targets = self.recommender.get_crop_targets('rice')
        self.assertEqual(rice_targets['N'], 120, "Rice N target should be 120 kg/ha")
        self.assertEqual(rice_targets['P'], 60, "Rice P target should be 60 kg/ha")
        self.assertEqual(rice_targets['K'], 60, "Rice K target should be 60 kg/ha")
        
        # Test wheat targets
        wheat_targets = self.recommender.get_crop_targets('wheat')
        self.assertEqual(wheat_targets['N'], 100, "Wheat N target should be 100 kg/ha")
        self.assertEqual(wheat_targets['P'], 50, "Wheat P target should be 50 kg/ha")
        self.assertEqual(wheat_targets['K'], 40, "Wheat K target should be 40 kg/ha")
    
    def test_ph_warning_thresholds(self):
        """Test pH warning thresholds for extreme pH values."""
        # Test low pH warning
        low_ph_sample = {
            'crop': 'rice',
            'N': 50.0,
            'P': 10.0,
            'K': 20.0,
            'pH': 5.0  # Below 5.5 threshold
        }
        low_ph_recs = self.recommender.recommend_for_row(low_ph_sample)
        self.assertNotEqual(
            low_ph_recs['ph_warning'], 
            "", 
            "Low pH should generate a warning"
        )
        self.assertIn("Low pH", low_ph_recs['ph_warning'])
        
        # Test high pH warning
        high_ph_sample = {
            'crop': 'rice',
            'N': 50.0,
            'P': 10.0,
            'K': 20.0,
            'pH': 8.0  # Above 7.5 threshold
        }
        high_ph_recs = self.recommender.recommend_for_row(high_ph_sample)
        self.assertNotEqual(
            high_ph_recs['ph_warning'], 
            "", 
            "High pH should generate a warning"
        )
        self.assertIn("High pH", high_ph_recs['ph_warning'])
    
    def test_unknown_crop_defaults(self):
        """Test that unknown crops use default target values."""
        unknown_crop_sample = {
            'crop': 'unknown_crop',
            'N': 50.0,
            'P': 10.0,
            'K': 20.0,
            'pH': 6.5
        }
        
        # This should not raise an error and should use default targets
        recommendations = self.recommender.recommend_for_row(unknown_crop_sample)
        
        # Check that recommendations are still generated
        self.assertIn('N_need_kg_ha', recommendations)
        self.assertIn('P_need_kg_ha', recommendations)
        self.assertIn('K_need_ha', recommendations)
        self.assertIn('ph_warning', recommendations)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
