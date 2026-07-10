import os

from localvault.domain.models import NeedsReview, Proposal


def present(results):
    for result in results:
        if isinstance(result, Proposal):
            print(f"Proposal: {os.path.basename(result.source_path)} -> {result.classification.category}")
        elif isinstance(result, NeedsReview):
            print(f"Needs Review: {os.path.basename(result.source_path)} -> {result.reason.value}")  
