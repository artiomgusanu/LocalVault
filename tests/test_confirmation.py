from localvault.adapters.confirmation import parse_decision, confirm
from localvault.domain.models import Decision, Classification, Proposal


def test_y_maps_to_accept():
    assert parse_decision("y") == Decision.ACCEPT

def test_n_maps_to_reject():
    assert parse_decision("n") == Decision.REJECT

def test_r_maps_to_review():
    assert parse_decision("r") == Decision.REVIEW

def test_q_maps_to_quit():
    assert parse_decision("q") == Decision.QUIT

def test_uppercase_is_accepted():
    assert parse_decision("Y") == Decision.ACCEPT

def test_surrounding_whitespace_is_trimmed():
    assert parse_decision("  y  ") == Decision.ACCEPT

def test_full_word_is_not_accepted():
    assert parse_decision("yes") is None

def test_unknown_key_returns_none():
    assert parse_decision("x") is None

def test_empty_string_returns_none():
    assert parse_decision("") is None

def make_proposal():
    return Proposal(
        source_path="C:/origem/fatura.pdf",
        classification=Classification(
            document_type="invoice",
            category="finance",
            title="Fatura",
            suggested_filename="fatura",
        ),
        destination_path="C:/vault/finance/fatura.pdf",
    )

def make_reader(*respostas):
    it = iter(respostas)
    return lambda: next(it)

def test_confirm_returns_accept_on_y():
    result = confirm(make_proposal(), reader=make_reader("y"))
    assert result == Decision.ACCEPT

def test_confirm_returns_quit_on_q():
    result = confirm(make_proposal(), reader=make_reader("q"))
    assert result == Decision.QUIT

def test_confirm_reprompts_on_invalid_then_accepts():
    result = confirm(make_proposal(), reader=make_reader("x", "y"))
    assert result == Decision.ACCEPT