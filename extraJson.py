import fitz  # PyMuPDF
import spacy
import json
import glob
from pdf2image import convert_from_path
import pytesseract

def ocr_image(image):
    return pytesseract.image_to_string(image, lang='fra')

def extract_text_from_pdf(path):
    text = ""
    document = fitz.open(path)
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def extract_text_from_scanned_pdf(path):
    images = convert_from_path(path)
    text = ""
    for image in images:
        text += ocr_image(image)
    return text

def analyze_text(text, nlp):
    doc = nlp(text)
    data = {
        "academic": [],
        "career": [],
        "skills": {
            "technical_skills": [],
            "soft_skills": []
        },
        "consultant": {},
        "commercial": {}
    }

    # Extraction logic based on the structure of the text
    # Placeholder logic for example purposes
    for ent in doc.ents:
        if ent.label_ == "FORMATION":
            data["academic"].append(ent.text)
        elif ent.label_ == "EXPERIENCE":
            data["career"].append(ent.text)
        elif ent.label_ == "SKILL":
            data["skills"]["technical_skills"].append(ent.text)
        elif ent.label_ == "CONSULTANT":
            data["consultant"]["info"] = ent.text
        elif ent.label_ == "COMMERCIAL":
            data["commercial"]["info"] = ent.text

    return data

def process_pdfs(path_corpora, model):
    nlp = spacy.load(model)
    all_data = []
    
    for path in glob.glob(path_corpora):
        if fitz.open(path).is_encrypted:
            text = extract_text_from_scanned_pdf(path)
        else:
            text = extract_text_from_pdf(path)
            print(text)
        
        analyzed_data = analyze_text(text, nlp)
        all_data.append(analyzed_data)

    return all_data

path_corpora = "dataset/*.pdf"
model = "fr_core_news_sm"

all_data = process_pdfs(path_corpora, model)

# Convert the extracted data to JSON format
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print("Extraction completed and data saved to output.json")
