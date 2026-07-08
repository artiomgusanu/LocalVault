from localvault.adapters.discovery import find_pdfs
from localvault.adapters.extractor import extract_text_from_pdf
from localvault.adapters.classifier import classify_document
from localvault.domain.analyze import analyze


def main():
    folder_path = r"C:\Users\artio\OneDrive\Área de Trabalho\LocalVault\data\organize"

    pdf_files = find_pdfs(folder_path)

    results = analyze(pdf_files, extract_text_from_pdf, classify_document)

    for result in results:
        print(result)


if __name__ == "__main__":
    main()