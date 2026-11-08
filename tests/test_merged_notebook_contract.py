import subprocess
import sys
from pathlib import Path
import unittest


class MergedNotebookContractTest(unittest.TestCase):
    def test_smoke_gate(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, str(root / "evals" / "run_merged_notebook_smoke.py")],
            cwd=root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
