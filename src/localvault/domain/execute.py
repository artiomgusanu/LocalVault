from localvault.domain.models import OrganizeResult, ResultStatus


def execute(proposal, dry_run=True) -> OrganizeResult:
    if dry_run:
        return OrganizeResult(
            source_path=proposal.source_path,
            destination_path=proposal.destination_path,
            status=ResultStatus.SIMULATED,
        )

    raise NotImplementedError("Real file movement not implemented yet")