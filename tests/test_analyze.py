from localvault.domain.analyze import analyze_one, analyze
from localvault.domain.models import Proposal, NeedsReview, ReviewReason, Classification
from localvault.domain.errors import ExtractionError, ClassificationError, PathValidationError


# --- Fakes felizes ---

def fake_extract_ok(path):
    return "texto extraído"


def fake_classify_ok(text):
    return Classification(
        document_type="invoice",
        category="finance",
        title="Fatura",
        suggested_filename="fatura",
    )


def fake_resolve_ok(root, category, name, source):
    return f"{root}/{category}/{name}.pdf"


# --- Fakes que falham ---

def fake_extract_raise(path):
    raise ExtractionError("boom")


def fake_classify_raise(text):
    raise ClassificationError("boom")


def fake_classify_unknown_category(text):
    return Classification(
        document_type="invoice",
        category="xpto",          # não está nas KNOWN_CATEGORIES
        title="Fatura",
        suggested_filename="fatura",
    )


def fake_resolve_raise(root, category, name, source):
    raise PathValidationError("boom")


# --- Testes: um por ramo ---

def test_happy_path_returns_proposal():
    result = analyze_one(
        "C:/origem/fatura.pdf",
        fake_extract_ok, fake_classify_ok, fake_resolve_ok, "C:/vault",
    )
    assert isinstance(result, Proposal)
    assert result.destination_path == "C:/vault/finance/fatura.pdf"


def test_extraction_failure_returns_needs_review():
    result = analyze_one(
        "C:/origem/fatura.pdf",
        fake_extract_raise, fake_classify_ok, fake_resolve_ok, "C:/vault",
    )
    assert isinstance(result, NeedsReview)
    assert result.reason == ReviewReason.EXTRACTION_FAILED


def test_classification_failure_returns_needs_review():
    result = analyze_one(
        "C:/origem/fatura.pdf",
        fake_extract_ok, fake_classify_raise, fake_resolve_ok, "C:/vault",
    )
    assert isinstance(result, NeedsReview)
    assert result.reason == ReviewReason.INVALID_OUTPUT


def test_unknown_category_returns_needs_review():
    result = analyze_one(
        "C:/origem/fatura.pdf",
        fake_extract_ok, fake_classify_unknown_category, fake_resolve_ok, "C:/vault",
    )
    assert isinstance(result, NeedsReview)
    assert result.reason == ReviewReason.UNKNOWN_CATEGORY


def test_path_validation_failure_returns_needs_review():
    result = analyze_one(
        "C:/origem/fatura.pdf",
        fake_extract_ok, fake_classify_ok, fake_resolve_raise, "C:/vault",
    )
    assert isinstance(result, NeedsReview)
    assert result.reason == ReviewReason.PATH_VALIDATION_FAILED


def test_batch_isolates_failures():
    paths = ["C:/origem/ok.pdf", "C:/origem/mau.pdf"]

    def extract_by_path(path):
        if "mau" in path:
            raise ExtractionError("boom")
        return "texto"

    results = analyze(
        paths, extract_by_path, fake_classify_ok, fake_resolve_ok, "C:/vault",
    )
    assert len(results) == 2
    assert isinstance(results[0], Proposal)
    assert isinstance(results[1], NeedsReview)