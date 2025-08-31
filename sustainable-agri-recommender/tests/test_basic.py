"""
Basic tests for the Sustainable Agriculture Recommender project.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestBasicFunctionality(unittest.TestCase):
    """Test basic project functionality."""
    
    def test_imports(self):
        """Test that basic imports work."""
        try:
            import numpy as np
            import pandas as pd
            import sklearn
            self.assertTrue(True, "Basic imports successful")
        except ImportError as e:
            self.fail(f"Failed to import required packages: {e}")
    
    def test_project_structure(self):
        """Test that project structure is correct."""
        project_root = os.path.join(os.path.dirname(__file__), '..')
        
        # Check required directories exist
        required_dirs = ['src', 'data', 'data/raw', 'results', 'notebooks', 'tests']
        for dir_name in required_dirs:
            dir_path = os.path.join(project_root, dir_name)
            self.assertTrue(os.path.exists(dir_path), f"Directory {dir_name} does not exist")
        
        # Check required files exist
        required_files = ['README.md', 'project_goal.md', 'requirements.txt', '.gitignore', 'LICENSE']
        for file_name in required_files:
            file_path = os.path.join(project_root, file_name)
            self.assertTrue(os.path.exists(file_path), f"File {file_name} does not exist")
    
    def test_python_version(self):
        """Test that Python version is compatible."""
        version = sys.version_info
        self.assertGreaterEqual(version.major, 3, "Python 3.x required")
        self.assertGreaterEqual(version.minor, 8, "Python 3.8+ required")
    
    def test_working_directory(self):
        """Test that we can read and write to working directory."""
        test_file = "test_temp_file.txt"
        test_content = "Test content"
        
        try:
            # Test write
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            # Test read
            with open(test_file, 'r') as f:
                read_content = f.read()
            
            self.assertEqual(read_content, test_content, "File read/write test failed")
            
        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)


class TestDataStructures(unittest.TestCase):
    """Test basic data structures and operations."""
    
    def test_numpy_operations(self):
        """Test basic numpy operations."""
        import numpy as np
        
        # Test array creation
        arr = np.array([1, 2, 3, 4, 5])
        self.assertEqual(len(arr), 5, "Array length incorrect")
        self.assertEqual(arr.sum(), 15, "Array sum incorrect")
        
        # Test array operations
        arr_squared = arr ** 2
        expected = np.array([1, 4, 9, 16, 25])
        np.testing.assert_array_equal(arr_squared, expected, "Array squaring failed")
    
    def test_pandas_operations(self):
        """Test basic pandas operations."""
        import pandas as pd
        
        # Test DataFrame creation
        data = {'crop': ['wheat', 'corn', 'soybeans'], 'yield': [100, 150, 80]}
        df = pd.DataFrame(data)
        
        self.assertEqual(len(df), 3, "DataFrame length incorrect")
        self.assertEqual(df['yield'].sum(), 330, "DataFrame sum incorrect")
        
        # Test basic operations
        df['yield_per_acre'] = df['yield'] / 10
        expected_yields = [10.0, 15.0, 8.0]
        np.testing.assert_array_almost_equal(df['yield_per_acre'].values, expected_yields)


class TestAgriculturalData(unittest.TestCase):
    """Test agricultural data handling."""
    
    def test_soil_data_structure(self):
        """Test soil data structure validation."""
        # Mock soil data
        soil_data = {
            'ph': 6.5,
            'nitrogen': 25,
            'phosphorus': 15,
            'potassium': 120,
            'organic_matter': 2.5
        }
        
        # Test data types
        self.assertIsInstance(soil_data['ph'], float, "pH should be float")
        self.assertIsInstance(soil_data['nitrogen'], int, "Nitrogen should be int")
        
        # Test value ranges
        self.assertGreaterEqual(soil_data['ph'], 0, "pH should be >= 0")
        self.assertLessEqual(soil_data['ph'], 14, "pH should be <= 14")
        self.assertGreaterEqual(soil_data['nitrogen'], 0, "Nitrogen should be >= 0")
    
    def test_crop_data_structure(self):
        """Test crop data structure validation."""
        # Mock crop data
        crop_data = {
            'name': 'wheat',
            'optimal_ph_min': 6.0,
            'optimal_ph_max': 7.5,
            'growing_season': 'winter',
            'water_requirement': 'medium'
        }
        
        # Test required fields
        required_fields = ['name', 'optimal_ph_min', 'optimal_ph_max', 'growing_season']
        for field in required_fields:
            self.assertIn(field, crop_data, f"Required field {field} missing")
        
        # Test logical constraints
        self.assertLess(crop_data['optimal_ph_min'], crop_data['optimal_ph_max'], 
                       "pH min should be less than pH max")


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
