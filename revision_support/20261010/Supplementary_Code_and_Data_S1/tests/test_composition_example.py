from pathlib import Path
import unittest,sys,math,copy
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from composition_example import parse_formula,load_matrix,summarize,FEATURES
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=load_matrix(ROOT/'data/element_data_interpretable.csv')
 def test_weights(self):self.assertEqual(parse_formula('Fe2O3',set(self.data)),{'Fe':0.4,'O':0.6})
 def test_reference_atomic_number(self):
  r=summarize({'Fe':.4,'O':.6},self.data,FEATURES[0][0]);self.assertAlmostEqual(r['mean'],15.2);self.assertAlmostEqual(r['weighted_sd'],math.sqrt(77.76))
 def test_pauling_mean(self):self.assertAlmostEqual(summarize({'Fe':.4,'O':.6},self.data,FEATURES[1][0])['mean'],2.796)
 def test_stoichiometric_scaling(self):self.assertEqual(parse_formula('Fe4O6',set(self.data)),parse_formula('Fe2O3',set(self.data)))
 def test_single_element(self):self.assertEqual(summarize({'Fe':1.0},self.data,FEATURES[0][0])['weighted_sd'],0.0)
 def test_missing_propagation(self):
  d=copy.deepcopy(self.data);d['O'][FEATURES[1][0]]='';r=summarize({'Fe':.4,'O':.6},d,FEATURES[1][0]);self.assertIsNone(r['mean']);self.assertIsNone(r['minimum']);self.assertEqual(r['atomic_fraction_coverage'],.4)
 def test_zero_is_valid(self):
  d=copy.deepcopy(self.data);d['O'][FEATURES[1][0]]='0';r=summarize({'Fe':.4,'O':.6},d,FEATURES[1][0]);self.assertEqual(r['atomic_fraction_coverage'],1.0);self.assertAlmostEqual(r['mean'],.732)
 def test_unsupported_formula(self):
  for formula in ['Ca(OH)2','CuSO4·5H2O','Fe3+','XxO2','Fe0O','']:
   with self.subTest(formula=formula):
    with self.assertRaises(ValueError):parse_formula(formula,set(self.data))
if __name__=='__main__':unittest.main()
