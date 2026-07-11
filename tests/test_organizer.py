from localvault.domain.organizer import organize
from localvault.domain.models import (
    Decision, Classification, NeedsReview, Proposal, OrganizeResult, ResultStatus, ReviewReason,
)

def make_proposal(name):
    return Proposal(
        source_path=f"C:/origem/{name}.pdf",
        classification=Classification(
            document_type="invoice", category="finance",
            title=name, suggested_filename=name,
        ),
        destination_path=f"C:/vault/finance/{name}.pdf",
    )

def make_confirm(*decisions):
    it = iter(decisions)
    return lambda proposal: next(it)

def fake_execute(proposal):
    return OrganizeResult(
        source_path=proposal.source_path,
        destination_path=proposal.destination_path,
        status=ResultStatus.SIMULATED,
    )

def test_accept_produces_simulated():
    results = [make_proposal("a")]
    final = organize(results, make_confirm(Decision.ACCEPT), fake_execute)
    assert final[0].status == ResultStatus.SIMULATED

def test_reject_produces_skipped():
    final = organize([make_proposal("a")], make_confirm(Decision.REJECT), fake_execute)
    assert final[0].status == ResultStatus.SKIPPED

def test_review_produces_sent_to_review():
    final = organize([make_proposal("a")], make_confirm(Decision.REVIEW), fake_execute)
    assert final[0].status == ResultStatus.SENT_TO_REVIEW

def test_quit_cancels_current_and_remaining():
    results = [make_proposal("a"), make_proposal("b"), make_proposal("c")]
    # aceita a primeira, faz quit na segunda
    final = organize(results, make_confirm(Decision.ACCEPT, Decision.QUIT), fake_execute)

    statuses = [r.status for r in final]
    assert ResultStatus.SIMULATED in statuses      # a "a" foi processada
    assert statuses.count(ResultStatus.CANCELLED) == 2  # "b" e "c" canceladas

def make_review(name):
    return NeedsReview(
        source_path=f"C:/origem/{name}.pdf",
        reason=ReviewReason.UNKNOWN_CATEGORY,
    )

def test_needs_review_becomes_sent_to_review():
    results = [make_review("x")]
    final = organize(results, make_confirm(), fake_execute)
    assert len(final) == 1
    assert final[0].status == ResultStatus.SENT_TO_REVIEW
    assert final[0].source_path == "C:/origem/x.pdf"