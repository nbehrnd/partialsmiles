import unittest
from smiparser import ParseSmiles

class MolTest(unittest.TestCase):
    def testBonds(self):
        mol = ParseSmiles("CCO", False)
        self.assertTrue(mol.getBond(0, 1))
        self.assertTrue(mol.getBond(1, 2))
        self.assertFalse(mol.getBond(0, 2))

class RuleTests(unittest.TestCase):
    def testRuleOne(self):
        """Whether to allow empty molecules, like C..C"""
        smi = "C..C"
        self.assertRaises(Exception, ParseSmiles, smi, False)
        ParseSmiles(smi, False, 1)
    def testRuleTwo(self):
        "Whether to allow an empty branch like C()C"
        smi = "C()C"
        self.assertRaises(Exception, ParseSmiles, smi, False)
        ParseSmiles(smi, False, 2)
    def testRuleThree(self):
        """Whether to allow an open parenthesis without a preceding
        atom like (CC)"""
        smis = ["(CC)", "C.(CC)"]
        for smi in smis:
            self.assertRaises(Exception, ParseSmiles, smi, False)
            ParseSmiles(smi, False, 4)
    def testRuleFour(self):
        """Whether to allow a dot within parentheses"""
        smis = ["C(C.C)C"]
        for smi in smis:
            self.assertRaises(Exception, ParseSmiles, smi, False)
            ParseSmiles(smi, False, 8)
    def testRuleFive(self):
        """Whether to allow bond closures across disconnected components"""
        smis = ["C1.C1"]
        for smi in smis:
            self.assertRaises(Exception, ParseSmiles, smi, False)
            ParseSmiles(smi, False, 16)

class ParserTests(unittest.TestCase):
    def testParentheses(self):
        good = ["C(=O)Cl"]
        bad = ["C(", "C(C(", "C)", "CCC.)", "(C)", "C((C))",
               "C.(C)", ")C", "C(C))C"]
        for smi in good:
            ParseSmiles(smi, False)
        for smi in bad:
            self.assertRaises(Exception, ParseSmiles, smi, False)
    def testBondClosures(self):
        good = ["C1CCC1", "C%23CCC%23", "C-1OC1", "C-1OC-1"]
        bad = ["C1CC", "C11C", "1C", "%12C", "C.1C", "C-1OC=1", "C1C1"]
        for smi in good:
            ParseSmiles(smi, False)
        for smi in bad:
            self.assertRaises(Exception, ParseSmiles, smi, False)
    def testDots(self):
        good = ["C.C"]
        bad = [".C", "C..C", "C-."]
        for smi in good:
            ParseSmiles(smi, False)
        for smi in bad:
            self.assertRaises(Exception, ParseSmiles, smi, False)
    def testBondChar(self):
        good = ["C-C#C", "C/C=C/Cl"]
        bad = ["-C", "C.-C", "C-=C", "C--C", "C-(C)"]
        for smi in good:
            ParseSmiles(smi, False)
        for smi in bad:
            self.assertRaises(Exception, ParseSmiles, smi, False)
    def testIsotope(self):
        good = ["[12CH4]"]
        bad = ["[0CH4]"]
        for smi in good:
            ParseSmiles(smi, False)
        for smi in bad:
            self.assertRaises(Exception, ParseSmiles, smi, False)
    def testBrackets(self):
        good = ["[16CH4]", "[NH4+]", "[C@@H]"]
        bad = ["[16C)", "C(C-)Cl"]
        for smi in good:
            ParseSmiles(smi, False)
        for smi in bad:
            self.assertRaises(Exception, ParseSmiles, smi, False)

if __name__ == "__main__":
    unittest.main()