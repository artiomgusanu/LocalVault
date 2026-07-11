from pathlib import Path

from localvault.adapters.discovery import find_pdfs
from localvault.adapters.extractor import extract_text_from_pdf
from localvault.adapters.classifier import classify_document
from localvault.adapters.confirmation import confirm
from localvault.adapters.presentation import present_results
from localvault.domain.analyze import analyze
from localvault.domain.organizer import organize
from localvault.domain.execute import execute
from localvault.domain.paths import resolve_destination


def main():
    folder_path = r"C:\Users\artio\OneDrive\Área de Trabalho\LocalVault\data\organize"
    target_root = Path(r"C:\Users\artio\OneDrive\Área de Trabalho\LocalVault\data\vault")

    pdf_files = find_pdfs(folder_path)

    results = analyze(
        pdf_files, extract_text_from_pdf, classify_document, resolve_destination, target_root
    )

    execute_fn = lambda proposal: execute(proposal, dry_run=True)
    final_results = organize(results, confirm, execute_fn)

    present_results(final_results)


if __name__ == "__main__":
    main()