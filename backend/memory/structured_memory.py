import json
from pathlib import Path
from typing import Dict, Optional, List, Any
from backend.models.candidate import CandidateProfile
from backend.core.logger import logger

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CANDIDATE_FILE = DATA_DIR / "candidates.json"


class StructuredMemory:
    """
    Tier 1 — Structured Memory (PostgreSQL / JSON file persistence).
    Stores Candidate Profiles, Skills, Experience, Target Companies, and Test Scores.
    """
    def __init__(self):
        self._db: Dict[str, dict] = {}
        self._load()

    def _load(self):
        if CANDIDATE_FILE.exists():
            try:
                with open(CANDIDATE_FILE, "r", encoding="utf-8") as f:
                    self._db = json.load(f)
            except Exception as e:
                logger.error(f"Error loading structured memory: {e}")
                self._db = {}

    def _save(self):
        try:
            with open(CANDIDATE_FILE, "w", encoding="utf-8") as f:
                json.dump(self._db, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving structured memory: {e}")

    def save_candidate(self, profile: CandidateProfile) -> CandidateProfile:
        self._db[profile.candidate_id] = profile.model_dump(mode="json")
        self._save()
        logger.info(f"Saved candidate {profile.candidate_id} to Structured Memory.")
        return profile

    def get_candidate(self, candidate_id: str) -> Optional[CandidateProfile]:
        data = self._db.get(candidate_id)
        if not data:
            # Return default profile if candidate does not exist yet
            default_profile = CandidateProfile(
                candidate_id=candidate_id,
                name="Default Candidate",
                target_role="AI Engineer",
                target_companies=["Google", "OpenAI", "Meta"],
                skills=[],
                weaknesses=["OOP", "System Design"],
                strengths=["Python", "SQL"],
            )
            self.save_candidate(default_profile)
            return default_profile
        return CandidateProfile(**data)

    def list_candidates(self) -> List[dict]:
        return list(self._db.values())


structured_memory = StructuredMemory()
