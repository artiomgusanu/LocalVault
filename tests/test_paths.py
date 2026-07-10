from pathlib import Path

from localvault.domain.paths import is_within, sanitize, resolve_destination
from localvault.domain.errors import PathValidationError

def test_json_extension_is_removed():
    resultado = sanitize("artiom_work.json")
    assert resultado == "artiom_work"

def test_empty_input_falls_back_to_document():
    resultado = sanitize("")
    assert resultado == "document"

def test_input_that_collapses_to_empty_falls_back_to_document():
    resultado = sanitize("...")
    assert resultado == "document"

def test_only_separators_falls_back_to_document():
    resultado = sanitize("///")
    assert resultado == "document"

def test_only_whitespace_falls_back_to_document():
    resultado = sanitize("   ")
    assert resultado == "document"

def test_only_extension_falls_back_to_document():
    resultado = sanitize(".pdf")
    assert resultado == "document"

def test_forward_slash_separator_is_removed():
    resultado = sanitize("report/final")
    assert "/" not in resultado

def test_backslash_separator_is_removed():
    resultado = sanitize("report\\final")
    assert "\\" not in resultado

def test_path_traversal_is_neutralized():
    resultado = sanitize("../../etc/passwd")
    assert "/" not in resultado
    assert ".." not in resultado

def test_double_dot_alone_is_neutralized():
    resultado = sanitize("..")
    assert ".." not in resultado

def test_reserved_name_falls_back_to_document():
    resultado = sanitize("CON")
    assert resultado == "document"

def test_reserved_name_with_extension_falls_back_to_document():
    resultado = sanitize("CON.pdf")
    assert resultado == "document"

def test_reserved_name_lowercase_falls_back_to_document():
    resultado = sanitize("con")
    assert resultado == "document"

def test_sanitize_is_idempotent():
    entradas = ["CON", "../../etc/passwd", "report/final", "...", "artiom_work.json"]
    for entrada in entradas:
        primeira = sanitize(entrada)
        segunda = sanitize(primeira)
        assert segunda == primeira

def test_clean_name_is_unchanged():
    resultado = sanitize("relatorio_junho")
    assert resultado == "relatorio_junho"

def test_unicode_accents_are_preserved():
    resultado = sanitize("relatório_técnico")
    assert resultado == "relatório_técnico"

def test_control_characters_are_removed():
    resultado = sanitize("file\u0000name")
    assert "\u0000" not in resultado
    assert resultado == "filename"

def test_bidi_override_is_removed():
    resultado = sanitize("safe\u202ename")
    assert "\u202e" not in resultado

def test_long_name_is_truncated():
    resultado = sanitize("a" * 400)
    assert len(resultado) <= 255

def test_idempotent_on_clean_name():
    limpo = "relatorio_junho"
    assert sanitize(sanitize(limpo)) == sanitize(limpo)

def test_root_is_within_itself():
    root = Path("C:/vault")
    assert is_within(root, root) is True

def test_direct_file_is_within_root():
    root = Path("C:/vault")
    candidato = Path("C:/vault/file.pdf")
    assert is_within(candidato, root) is True

def test_file_in_subfolder_is_within_root():
    root = Path("C:/vault")
    candidato = Path("C:/vault/finance/file.pdf")
    assert is_within(candidato, root) is True

def test_sibling_with_similar_prefix_is_not_within_root():
    root = Path("C:/vault")
    candidato = Path("C:/vault-secreto/file.pdf")
    assert is_within(candidato, root) is False

def test_parent_is_not_within_child():
    root = Path("C:/vault/finance")
    candidato = Path("C:/vault")
    assert is_within(candidato, root) is False

def test_unrelated_path_is_not_within_root():
    root = Path("C:/vault")
    candidato = Path("C:/Windows/System32")
    assert is_within(candidato, root) is False

def test_destination_is_inside_target_root(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    dest = resolve_destination(vault, "finance", "fatura", "C:/origem/fatura.pdf")
    assert is_within(dest, vault.resolve()) is True


def test_llm_json_extension_is_replaced_by_pdf(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    dest = resolve_destination(vault, "finance", "fatura.json", "C:/origem/fatura.pdf")
    assert dest.suffix == ".pdf"


def test_suggested_name_is_sanitized(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    dest = resolve_destination(vault, "finance", "../../etc/passwd", "C:/origem/x.pdf")
    assert ".." not in str(dest)