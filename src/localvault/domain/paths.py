import unicodedata

from pathlib import Path
from localvault.domain.errors import PathValidationError

RESERVED_NAMES: frozenset[str] = frozenset(
    {
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
    }
)

FALLBACK = "document"
MAX_LENGTH = 200

def sanitize(raw: str) -> str:
    text = raw.strip()
    text = text.replace("/", "").replace("\\", "")

    while ".." in text:
        text = text.replace("..", "")

    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C")

    if "." in text:
        text = text.rpartition(".")[0]

    text = text.strip()

    if not text:
        return FALLBACK

    if text.upper() in RESERVED_NAMES:
        return FALLBACK

    return text[:MAX_LENGTH]

def is_within(candidate: Path, root: Path) -> bool:
    return candidate.is_relative_to(root)

def resolve_destination(target_root, category, suggested_filename, source_path):
    stem = sanitize(suggested_filename)
    extension = Path(source_path).suffix
    final_name = stem + extension

    candidate = (target_root / category / final_name).resolve()
    root = target_root.resolve()

    if not is_within(candidate, root):
        raise PathValidationError(f"Destination escapes target root: {candidate}")

    return candidate