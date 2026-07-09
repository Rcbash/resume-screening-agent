from pathlib import Path
import subprocess
import sys


def test_sample_data_exists():
    assert Path("data/job_description.txt").exists()
    assert Path("data/resumes").exists()
    assert len(list(Path("data/resumes").glob("*"))) >= 10


def test_agent_runs_successfully():
    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            "--jd",
            "data/job_description.txt",
            "--resumes",
            "data/resumes",
            "--output",
            "outputs",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0
    assert Path("outputs/ranked_candidates.csv").exists()
    assert Path("outputs/ranked_candidates.json").exists()
