cffi==1.16.0
charset-normalizer==3.3.2
cryptography==42.0.8
pdfminer.six==20240706
pycparser==2.22
pypdf==4.2.0

#!/bin/bash

# Mettre à jour la liste des paquets
sudo apt update

# Installer Tesseract OCR
sudo apt install -y tesseract-ocr

# Installer les langues supplémentaires pour Tesseract OCR (optionnel)
sudo apt install -y tesseract-ocr-fra  # Pour le support du français

# Installer pip si nécessaire
sudo apt install -y python3-pip

# Installer les dépendances Python à partir de requirements.txt
pip install -r requirements.txt

# Installer le model de langauge SpaCy
python -m spacy download fr_core_news_sm
