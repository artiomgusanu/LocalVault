from localvault.domain.categories import is_known
from localvault.domain.models import Proposal, NeedsReview, ReviewReason
from localvault.domain.errors import ExtractionError, ClassificationError


def analyze(pdf_paths, extract, classify) -> list[Proposal | NeedsReview]:
    responses = []
    for pdf_file in pdf_paths:
        responses.append(analyze_one(pdf_file, extract, classify))
    return responses


def analyze_one(pdf_path, extract, classify) -> Proposal | NeedsReview:
    try:
        text = extract(pdf_path)
    except ExtractionError:
        return NeedsReview(source_path=pdf_path, reason=ReviewReason.EXTRACTION_FAILED)

    try:
        classification = classify(text)
    except ClassificationError:
        return NeedsReview(source_path=pdf_path, reason=ReviewReason.INVALID_OUTPUT)

    if not is_known(classification.category):
        return NeedsReview(source_path=pdf_path, reason=ReviewReason.UNKNOWN_CATEGORY)

    return Proposal(source_path=pdf_path, classification=classification)