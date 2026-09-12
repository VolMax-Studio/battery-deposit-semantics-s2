"""
Constructive witness test for E8a joint scope and unit assignment.
Explicitly demonstrates that:
1. The zero-slack (4, 6) case is satisfiable (exactly 2 A, 2 mA; V/mV >= 2).
2. The balanced (5, 5) case is satisfiable.
3. The zero-slack (6, 4) case is satisfiable (exactly 2 V, 2 mV; A/mA >= 2).
"""

import sys
import os
import unittest

# Ensure implementation is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from f2_corpus.e8a_joint_solver import solve_e8a_joint, verify_e8a_witness


class TestE8aJointWitness(unittest.TestCase):
    def test_case_4_6_zero_slack_current(self):
        """Test the zero-slack (4, 6) allocation."""
        witness = solve_e8a_joint(target_standalone_split=(4, 6))
        res = verify_e8a_witness(witness)
        self.assertTrue(res["valid"], msg=res.get("reason"))
        
        # Verify exact zero slack: current has 4 cells, exactly 2 A and 2 mA
        standalone_details = witness.to_dict()["standalone_details"]
        curr_units = [d["assigned_unit"] for d in standalone_details if d["scope"] == "current"]
        volt_units = [d["assigned_unit"] for d in standalone_details if d["scope"] == "voltage"]
        
        self.assertEqual(len(curr_units), 4)
        self.assertEqual(len(volt_units), 6)
        self.assertEqual(curr_units.count("A"), 2)
        self.assertEqual(curr_units.count("mA"), 2)
        self.assertGreaterEqual(volt_units.count("V"), 2)
        self.assertGreaterEqual(volt_units.count("mV"), 2)

    def test_case_5_5_balanced(self):
        """Test the balanced (5, 5) allocation."""
        witness = solve_e8a_joint(target_standalone_split=(5, 5))
        res = verify_e8a_witness(witness)
        self.assertTrue(res["valid"], msg=res.get("reason"))
        
        standalone_details = witness.to_dict()["standalone_details"]
        curr_units = [d["assigned_unit"] for d in standalone_details if d["scope"] == "current"]
        volt_units = [d["assigned_unit"] for d in standalone_details if d["scope"] == "voltage"]
        
        self.assertEqual(len(curr_units), 5)
        self.assertEqual(len(volt_units), 5)
        self.assertGreaterEqual(curr_units.count("A"), 2)
        self.assertGreaterEqual(curr_units.count("mA"), 2)
        self.assertGreaterEqual(volt_units.count("V"), 2)
        self.assertGreaterEqual(volt_units.count("mV"), 2)

    def test_case_6_4_zero_slack_voltage(self):
        """Test the zero-slack (6, 4) allocation."""
        witness = solve_e8a_joint(target_standalone_split=(6, 4))
        res = verify_e8a_witness(witness)
        self.assertTrue(res["valid"], msg=res.get("reason"))
        
        standalone_details = witness.to_dict()["standalone_details"]
        curr_units = [d["assigned_unit"] for d in standalone_details if d["scope"] == "current"]
        volt_units = [d["assigned_unit"] for d in standalone_details if d["scope"] == "voltage"]
        
        self.assertEqual(len(curr_units), 6)
        self.assertEqual(len(volt_units), 4)
        self.assertGreaterEqual(curr_units.count("A"), 2)
        self.assertGreaterEqual(curr_units.count("mA"), 2)
        self.assertEqual(volt_units.count("V"), 2)
        self.assertEqual(volt_units.count("mV"), 2)


if __name__ == "__main__":
    unittest.main()
