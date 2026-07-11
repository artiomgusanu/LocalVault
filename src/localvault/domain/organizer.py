from localvault.domain.models import Decision, DecidedProposal, NeedsReview, OrganizeResult, Proposal, ResultStatus


def organize(results, confirm_fn, execute_fn) -> list[OrganizeResult]:
    proposals = [r for r in results if isinstance(r, Proposal)]
    reviews = [r for r in results if isinstance(r, NeedsReview)]

    decided = []
    cancelled = []
    quit_flag = False

    for proposal in proposals:
        if quit_flag:
            cancelled.append(proposal)
            continue

        decision = confirm_fn(proposal)
        if decision == Decision.QUIT:
            quit_flag = True
            cancelled.append(proposal)
        else:
            decided.append(DecidedProposal(proposal=proposal, decision=decision))

    final = []
    for d in decided:
        if d.decision == Decision.ACCEPT:
            final.append(execute_fn(d.proposal))
        elif d.decision == Decision.REJECT:
            final.append(OrganizeResult(
                source_path=d.proposal.source_path,
                destination_path=d.proposal.destination_path,
                status=ResultStatus.SKIPPED,
            ))
        elif d.decision == Decision.REVIEW:
            final.append(OrganizeResult(
                source_path=d.proposal.source_path,
                destination_path=d.proposal.destination_path,
                status=ResultStatus.SENT_TO_REVIEW,
            ))

    for proposal in cancelled:
        final.append(OrganizeResult(
            source_path=proposal.source_path,
            destination_path=proposal.destination_path,
            status=ResultStatus.CANCELLED,
        ))

    for review in reviews:
        final.append(OrganizeResult(
            source_path=review.source_path,
            destination_path=None,
            status=ResultStatus.SENT_TO_REVIEW,
        ))

    return final
