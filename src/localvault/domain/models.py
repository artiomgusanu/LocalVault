from enum import Enum
from pydantic import BaseModel

class Classification(BaseModel):
    document_type: str
    category: str
    title: str
    suggested_filename: str

class ReviewReason(str, Enum):
    EXTRACTION_FAILED = "extraction_failed"
    INVALID_OUTPUT = "invalid_output"
    UNKNOWN_CATEGORY = "unknown_category"
    PATH_VALIDATION_FAILED = "path_validation_failed"

class Proposal(BaseModel):
    source_path: str
    classification: Classification
    destination_path: str

class NeedsReview(BaseModel):
    source_path: str
    reason : ReviewReason