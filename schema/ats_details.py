from pydantic import BaseModel, Field


class ScoreDetail(BaseModel):
    score: int = Field(..., description="Score achieved in this category")
    max_score: int = Field(..., description="Maximum possible score for this category")
    reason: str = Field(..., description="Reason for the given score")


class Breakdown(BaseModel):
    skills_competencies: ScoreDetail
    experience_career_progression: ScoreDetail
    education_certifications: ScoreDetail
    achievements_impact: ScoreDetail
    formatting_ats_readiness: ScoreDetail
    professional_tone_clarity: ScoreDetail


class ResumeScore(BaseModel):
    total_score: int = Field(..., description="Total score across all categories")
    breakdown: Breakdown