from dataclasses import dataclass


@dataclass
class CalculateLevelAndSocialRank:
    current_level: int
    calculated_level: int
    current_rank: str
    calculated_rank: str
