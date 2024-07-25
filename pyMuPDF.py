# ##premier exemple avec pyMuPdf

# import fitz  # PyMuPDF
# import glob
# import spacy
# from spacy import displacy
# # nlp = spacy.load('fr')
# nlp = spacy.blank("fr")
# # nlp = spacy.load("fr_core_news_sm")

# def recuper_text(chemin):
#     document = fitz.open(chemin)
#     for page_num in range(len(document)):
#         page = document.load_page(page_num)
#         text = page.get_text()
#         # text_nlp=nlp(text)
#         # for token in text_nlp:
#         #     print(token.text)
#         print(f"page N° {page_num + 1}")
#         print(text)

# path_corpora = "dataset/*.pdf"
# model = "fr_core_news_sm"

# for chemin in glob.glob(path_corpora):
#     print("***************************premier pdf ",chemin,"*****************************************")
#     recuper_text(chemin)



import fitz  # PyMuPDF
import regex as re
import glob
import spacy
import json

nlp = spacy.load("fr_core_news_sm")

def extract_information_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""

    # Extract text from each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
        
    doc_spacy = nlp(text)
    names = [ent.text for ent in doc_spacy.ents if ent.label_ == "PER"]

    # Filter out non-personal names (e.g., verbs, incorrect detections)
    filtered_names = [name for name in names if len(name.split()) > 1]  # Filter out single-word names

    # Patterns for extracting relevant sections
    patterns = {
        "email": r"[\w.-]+@[^\s]+",
        "phone": r"\+?\d{2}[-.\s]?\d{2,3}[-.\s]?\d{2,3}[-.\s]?\d{2,3}",
        "address": r"\b\d{5}\b\s[\w\s,.-]+",
        "experience": r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}\s*–\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}[\s\S]*?(?=\n\n[\w\s]+:)",
        # Pattern for extracting experience sections
    }

    extracted_data = {}

    for key, pattern in patterns.items():
        matches = re.findall(pattern, text, re.MULTILINE)
        if matches:
            if key == "experience":
                # Clean up experience section by splitting into individual job entries
                jobs = re.split(r"(\d{4}\s*–\s*\d{4})", text)[1:]
                jobs = ["".join(group) for group in zip(jobs[0::2], jobs[1::2])]
                extracted_data[key] = jobs
            else:
                extracted_data[key] = matches

    # Extracting contact information if email and phone are found
    contact_info = {}
    if "email" in extracted_data:
        contact_info["email"] = extracted_data["email"][0]  # Assuming there's only one email
    if "phone" in extracted_data:
        contact_info["phone"] = extracted_data["phone"][0]  # Assuming there's only one phone number
    # Additional fields like mobile_phone, linkedin can be extracted similarly if present

    # Structuring the final data in JSON-like format
    json_data = {
        "contact": contact_info,
        "name": filtered_names,
        "address": extracted_data.get("address", ""),
        "experience": extracted_data.get("experience", [])
    }

    return json_data

# path_corpora = "dataset/*.pdf"
# # Example usage
# for chemin in glob.glob(path_corpora):
#     print("***************************premier pdf ",chemin,"*****************************************")
#     data = extract_information_from_pdf(chemin)

# # Print extracted data
#     print(data)

def main():
    path_corpora = "dataset/*.pdf"
    output_file = "extracted_data.json"

    # List to store data from all PDFs
    all_data = []

    for pdf_file in glob.glob(path_corpora):
        print(f"Extracting data from {pdf_file}...")
        data = extract_information_from_pdf(pdf_file)
        all_data.append(data)

    # Write all extracted data to a JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print(f"Extraction completed. Results saved to {output_file}")

if __name__ == "__main__":
    main()