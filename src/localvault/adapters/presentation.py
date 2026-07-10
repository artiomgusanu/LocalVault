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