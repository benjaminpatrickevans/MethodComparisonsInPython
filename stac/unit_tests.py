# -*- coding: utf-8 -*-

import unittest
import nonparametric_tests as npt
import parametric_tests as pt

test_data = {
    "A": [3, 4, 5, 6, 1, 5],
    "B": [4, 3, 2, 1, 2, 6],
    "C": [4, 3, 5, 6, 3, 7],
}

test_data2 = {
    "Tr.1": [5, 1, 16, 5, 10, 19, 10],
    "Tr.2": [4, 3, 12, 4, 9, 18, 7],
    "Tr.3": [7, 1, 22, 3, 7, 28, 6],
    "Tr.4": [10, 0, 22, 5, 13, 37, 8],
    "Tr.5": [12, 2, 35, 4, 10, 58, 7]
}

class TestRankings(unittest.TestCase):        
    def test_friedman(self):
        statistic, p_value, ranking, rank_cmp = npt.friedman_test(*test_data.values())
        self.assertListEqual([round(v, 4) for v in ranking], [1.8333, 2.5000, 1.6667])
        self.assertAlmostEqual(statistic, 1.2068965517241395, 4)
        self.assertAlmostEqual(p_value, 0.3392, 4)
    
    def test_aligned_ranks(self):
        statistic, p_value, ranking, rank_cmp = npt.friedman_aligned_ranks_test(*test_data.values())
        self.assertListEqual([round(v, 4) for v in ranking], [9.3333, 13.0000, 6.1667])
        self.assertAlmostEqual(statistic, 3.702455111762549, 4)
        self.assertAlmostEqual(p_value, 0.1570, 4)
        
    def test_quade(self):
        statistic, p_value, ranking, rank_cmp = npt.quade_test(*test_data.values())
        self.assertListEqual([round(v, 4) for v in ranking], [1.9286, 2.5952, 1.4762])
        self.assertAlmostEqual(statistic, 2.31374172185, 4)
        self.assertAlmostEqual(p_value, 0.1493, 4)
        
class TestControlPosthoc(unittest.TestCase):
    def setUp(self):
        _,_,_,rank_cmp = npt.friedman_test(*test_data.values())
        self.ranks = {key: rank_cmp[i] for i,key in enumerate(test_data.keys())}
        
    def test_bonferroni_dunn(self):
        npt.bonferroni_dunn_test(self.ranks)
        
    def test_holm(self):
        npt.holm_test(self.ranks)
        
    def test_hochberg(self):
        npt.hochberg_test(self.ranks)
        
    def test_li(self):
        npt.li_test(self.ranks)
        
    def test_finner(self):
        npt.finner_test(self.ranks)
        
class TestMultiPosthoc(unittest.TestCase):
    def setUp(self):
        _,_,_,rank_cmp = npt.friedman_test(*test_data.values())
        self.ranks = {key: rank_cmp[i] for i,key in enumerate(test_data.keys())}
        
    def test_nemenyi(self):
        npt.nemenyi_multitest(self.ranks)
        
    def test_shaffer(self):
        npt.shaffer_multitest(self.ranks)
        
class TestAnova(unittest.TestCase):
    def test_anova(self):
        pt.anova_test(*test_data.values())
        
    def test_bonferroni(self):
        _,_,pivots = pt.anova_test(*test_data.values())
        pivots = {key: pivots[i] for i,key in enumerate(test_data.keys())}
        pt.bonferroni_test(pivots, len(test_data.values()[0]))

if __name__ == '__main__':
    unittest.main()