"""Pin the posted Vaquum PR guideline artifacts."""

from hashlib import sha256
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PR_GUIDELINE = REPO_ROOT / 'VAQUUM_PR_GUIDELINE.md'
REPO_SPECIFICS = REPO_ROOT / 'VAQUUM_REPO_SPECIFICS.md'
EXPECTED_PR_GUIDELINE_SHA256 = 'ecb4e817e148c64e11a20b7fc34b5a0e5a2025abfa5f8c4b6693553681aa0276'
EXPECTED_REPO_SPECIFICS_SHA256 = '10a78b80a01d8df1a408608da089338f828fdc98e40ca5aab5a37d6c4c5b9fff'


def test_vaquum_pr_guideline_is_posted_unchanged() -> None:
    """Verify the universal PR guideline exists with the canonical digest."""
    assert PR_GUIDELINE.is_file()
    assert sha256(PR_GUIDELINE.read_bytes()).hexdigest() == EXPECTED_PR_GUIDELINE_SHA256


def test_vaquum_repo_specifics_are_posted_unchanged() -> None:
    """Verify the repo-specific appendix exists with the canonical digest."""
    assert REPO_SPECIFICS.is_file()
    assert sha256(REPO_SPECIFICS.read_bytes()).hexdigest() == EXPECTED_REPO_SPECIFICS_SHA256
