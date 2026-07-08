from enum import Enum
from pydantic import BaseModel

class Classification(BaseModel):
    document_type: str
    category: str
    title: str
    suggested_filename: str
    reasoning_summary: str | None = None

class ReviewReason(str, Enum):
    EXTRACTION_FAILED = "extraction_failed"
    INVALID_OUTPUT = "invalid_output"
    UNKNOWN_CATEGORY = "unknown_category"

class Proposal(BaseModel):
    source_path: str
    classification: Classification

class NeedsReview(BaseModel):
    source_path: str
    reason : ReviewReason