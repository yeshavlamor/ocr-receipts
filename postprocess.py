from rapidfuzz import process
import json
import re

def clean_text(text):
    # remove unwanted characters but keep currency symbols and some special characters
    text = re.sub(r'[^\w\s.,:/()-]', '', text)
    return text

def fuzzy_term_correction(ocr_results, known_terms, threshold=80):
    corrected_results = []

    for result in ocr_results:
        corrected_text = []
        lines = result['text'].splitlines()

        for line in lines:
            # Match each line against known terms
            match, score, index = process.extractOne(line, known_terms)

            # If a match is found above the threshold
            if score >= threshold:
                if "TAX ID" in match.upper():
                    # Special handling for TAX ID: preserve numbers following the corrected term
                    corrected_line = f"TAX ID: {''.join(filter(str.isdigit, line))}"
                else:
                    # For other terms, replace the known term while preserving the rest
                    corrected_term = match
                    for known_term in known_terms:
                        if known_term.lower() in line.lower():
                            line = line.lower().replace(known_term.lower(), corrected_term)
                            break
                    corrected_line = line

                corrected_text.append(corrected_line)
            else:
                corrected_text.append(line)

        corrected_results.append({
            'file': result['file'],
            'corrected_text': '\n'.join(corrected_text)
        })

    return corrected_results

def extract_fields(data):
    extracted_data = []

    for entry in data:
        corrected_text = entry.get('corrected_text', '')
        file_name = entry.get('file', 'unknown_file')

        # Patterns for field extraction
        company_name_match = re.search(r'(big\s*c\s*supercenter\s*public\s*co\.?\s*,?\s*ltd\.?)', corrected_text, re.IGNORECASE)
        tax_id_match = re.search(r'TAX ID:\s*(\d+)', corrected_text)
        transaction_date_match = re.search(r'Date:?\s*(\d{2}/\d{2}/\d{4})', corrected_text)
        card_no_match = re.search(r'Card No:\s*(\d+)', corrected_text)
        sale_amount_match = re.search(r'Sale Amount [A-Z]*:\s*([\d.,]+)', corrected_text)
        card_balance_match = re.search(r'Card Balance [A-Z]*:\s*([\d.,]+)', corrected_text)
        net_balance_match = re.search(r'Card Net Balance [A-Z]*:\s*([\d.,]+)', corrected_text)

        # Append extracted fields
        extracted_data.append({
            "file": file_name,
            "company_name": company_name_match.group(1) if company_name_match else None,
            "tax_id": tax_id_match.group(1) if tax_id_match else None,
            "transaction_date": transaction_date_match.group(1) if transaction_date_match else None,
            "card_no": card_no_match.group(1) if card_no_match else None,
            "sale_amount": sale_amount_match.group(1) if sale_amount_match else None,
            "card_balance": card_balance_match.group(1) if card_balance_match else None,
            "net_balance": net_balance_match.group(1) if net_balance_match else None
        })

    return extracted_data

def postprocess_images(json_file_path, known_terms):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        ocr_results = json.load(file)

    # Modify to pass the entire ocr_results list to fuzzy_term_correction
    ocr_results = fuzzy_term_correction(ocr_results, known_terms)

    # Step 2: Extract fields
    extracted_data = extract_fields(ocr_results) # Pass the modified ocr_results

    return extracted_data