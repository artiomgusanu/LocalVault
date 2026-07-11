from localvault.domain.execute import execute
from localvault.domain.models import Classification, Proposal, OrganizeResult, ResultStatus


def make_proposal():
    return Proposal(
        source_path="C:/origem/fatura.pdf",
        classification=Classification(
            document_type="invoice",
            category="finance",
            title="Fatura",
            suggested_filename="fatura",
        ),
        destination_path="C:/vault/finance/fatura.pdf",
    )


def test_dry_run_returns_simulated_status():
    result = execute(make_proposal(), dry_run=True)
    assert result.status == ResultStatus.SIMULATED


def test_dry_run_preserves_source_and_destination():
    result = execute(make_proposal(), dry_run=True)
    assert result.source_path == "C:/origem/fatura.pdf"
    assert result.destination_path == "C:/vault/finance/fatura.pdf"


def test_dry_run_returns_organize_result():
    result = execute(make_proposal(), dry_run=True)
    assert isinstance(result, OrganizeResult)