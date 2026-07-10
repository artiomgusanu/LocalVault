class ExtractionError(Exception):
    """Raised when a document's text cannot be extracted
    (corrupt, encrypted, or image-only PDF with no text layer)."""


class ClassificationError(Exception):
    """Raised when the LLM response cannot be parsed or validated
    into a Classification."""


class PathValidationError(Exception):
    """Raised when a resolved destination path escapes the target root."""