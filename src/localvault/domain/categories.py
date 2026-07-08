KNOWN_CATEGORIES: frozenset[str] = frozenset(
    {
        "work",
        "university",
        "finance",
        "shopping",
        "personal",
        "projects"
    }
)

def normalize(raw: str) -> str:
    return raw.strip().casefold()

def is_known(raw: str | None) -> bool:
    if not raw:
        return False

    return normalize(raw) in KNOWN_CATEGORIES