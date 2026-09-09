from typing import List
from pydantic import BaseModel, Field

class ReplyCritique(BaseModel):
    ok: bool = Field(
        description="True if the draft is faithful to the researched answer, appropriately "
        "hedged, and reasonable in tone; False if it needs another pass."
    )
    issues: List[str] = Field(
        default_factory=list,
        description="Short, specific problems: unsupported claims, missing caveats, wrong tone, "
        "invented details. Empty when ok is True.",
    )


class QueryAnalysis(BaseModel):
    is_clear: bool = Field(
        description="Indicates if the user's question is clear and answerable."
    )
    questions: List[str] = Field(
        description="List of rewritten, self-contained questions."
    )
    clarification_needed: str = Field(
        description="Explanation if the question is unclear."
    )