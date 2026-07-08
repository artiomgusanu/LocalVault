import os


def find_pdfs(folder_path: str) -> list[str]:
    pdf_files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(".pdf"):
            pdf_files.append(file_path)

    return sorted(pdf_files)