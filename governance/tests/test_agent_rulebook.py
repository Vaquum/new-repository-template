"""Pin the posted Vaquum agent rulebook artifact."""

from hashlib import sha256
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RULEBOOK = REPO_ROOT / 'VAQUUM_AGENT_RULEBOOK.md'
EXPECTED_SHA256 = 'ade2c1ae42cfb92f50fdfc93720dcb62ad3a7442c8a511bf6da3bcf7c606dd58'


def test_vaquum_agent_rulebook_is_posted_unchanged() -> None:
    """Verify the org-wide rulebook exists with the canonical digest."""
    assert RULEBOOK.is_file()
    assert sha256(RULEBOOK.read_bytes()).hexdigest() == EXPECTED_SHA256
