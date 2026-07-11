import os

from localvault.domain.models import NeedsReview, Proposal


def present(results):
    for result in results:
        if isinstance(result, Proposal):
            source = os.path.basename(result.source_path)
            destination = os.path.basename(result.destination_path)
            print(f"Proposal: {source} -> {result.classification.category}/{destination}")
        elif isinstance(result, NeedsReview):
            print(f"Needs Review: {os.path.basename(result.source_path)} -> {result.reason.value}")


def show_proposal_details(proposal):
    source = os.path.basename(proposal.source_path)
    destination = os.path.basename(proposal.destination_path)

    print(f"Origin: {source}")
    print(f"Destination: {proposal.classification.category}/{destination}")
    print(f"Type: {proposal.classification.document_type}")
    print(f"Title: {proposal.classification.title}")
    print("[y] yes  [n] no  [r] review  [q] quit")

