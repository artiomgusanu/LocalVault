from localvault.domain.models import Decision
from localvault.adapters.presentation import show_proposal_details

KEY_MAP = {
    "y": Decision.ACCEPT,
    "n": Decision.REJECT,
    "r": Decision.REVIEW,
    "q": Decision.QUIT,
}


def parse_decision(raw: str) -> Decision | None:
    key = raw.strip().lower()
    return KEY_MAP.get(key)

def confirm(proposal, reader=input) -> Decision:
    show_proposal_details(proposal)
    while True:
        decision = parse_decision(reader())
        if decision is not None:
            return decision
        print("Invalid option. Try again: [y] yes  [n] no  [r] review  [q] quit")
