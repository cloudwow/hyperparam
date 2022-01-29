import unittest

from hyperparamlib.hyper_parameter import HyperParameter, HyperParameters
class TestStuff(unittest.TestCase):
  def test_smoke(self):
    target = HyperParameters()
    target.add_param("arg_1",[1,2,3,4])
    result = target.get_likely_values()
    self.assertIn('arg_1', result)
    self.assertIn(result['arg_1'], [1,2,3,4])

if __name__ == '__main__':
    unittest.main()