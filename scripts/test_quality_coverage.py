"""Regression tests for the LCOV evidence reporter: run with unittest discover -s scripts."""
import unittest

from quality_coverage import markdown, package, parse_lcov, summarise


class CoverageParsingTests(unittest.TestCase):
    def test_native_and_runner_paths_group_correctly(self):
        self.assertEqual(package('/home/runner/work/a/a/crates/color/src/lib.rs'), 'crates/color')
        self.assertEqual(package('D:\\a\\lightcraft\\crates\\engine\\src\\lib.rs'), 'crates/engine')
        self.assertEqual(package('apps/lightcraft-web/src/lib.rs'), 'apps/lightcraft-web')
        self.assertEqual(package('/work/project/xtask/src/main.rs'), 'xtask')
        self.assertEqual(package('/elsewhere/generated.rs'), '(other)')

    def test_unions_repeated_records_instead_of_double_counting(self):
        lcov = '\n'.join([
            'SF:/tmp/project/crates/color/src/lib.rs', 'DA:1,2', 'DA:2,0', 'FNDA:1,myfunc',
            'BRDA:1,0,0,3', 'BRDA:1,0,1,-', 'end_of_record',
            'SF:/tmp/project/crates/color/src/lib.rs', 'DA:1,0', 'DA:2,1', 'FNDA:2,myfunc',
            'BRDA:1,0,0,0', 'BRDA:1,0,1,4', 'end_of_record',
        ])
        self.assertEqual(summarise(parse_lcov(lcov))['total'], {
            'files': 1, 'lines': 2, 'lines_hit': 2,
            'functions': 1, 'functions_hit': 1, 'branches': 2, 'branches_hit': 2,
        })

    def test_llvm_region_totals_are_authoritative(self):
        lcov = 'SF:crates/color/src/lib.rs\nDA:1,3\nDA:2,4\nLF:3\nLH:3\nFNF:2\nFNH:2\nend_of_record'
        total = summarise(parse_lcov(lcov))['total']
        self.assertEqual((total['lines'], total['lines_hit']), (3, 3))
        self.assertEqual((total['functions'], total['functions_hit']), (2, 2))

    def test_missing_branch_data_does_not_mean_full_coverage(self):
        report = summarise(parse_lcov(
            'SF:crates/color/src/lib.rs\nDA:1,1\nDA:2,0\nend_of_record'
        ))
        rendered = markdown(report)
        self.assertIn('1/2 (50.00%)', rendered)
        self.assertIn('not measured', rendered)
        self.assertNotIn('100.00%', rendered)


if __name__ == '__main__':
    unittest.main()
