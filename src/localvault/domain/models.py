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

class Decision(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    REVIEW = "review"
    QUIT = "quit"

class ResultStatus(str, Enum):
    SIMULATED = "simulated"
    MOVED = "moved"
    FAILED = "failed"
    SKIPPED = "skipped"
    SENT_TO_REVIEW = "sent_to_review"
    CANCELLED = "cancelled"

class DecidedProposal(BaseModel):
    proposal: Proposal
    decision: Decision

class OrganizeResult(BaseModel):
    source_path: str
    destination_path: str | None = None
    status: ResultStatus
    error: str | None = None