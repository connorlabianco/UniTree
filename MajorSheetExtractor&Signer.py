import json
import requests
from typing import Dict, List, Optional
import time
import os
import io
from datetime import datetime
def save_pdf(program_name: str, file_name: str, url: str, pdf_bytes: bytes, base_path: str):
    """Save downloaded PDF with metadata."""
    # Create directory if it doesn't exist
    os.makedirs(base_path, exist_ok=True)
    
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create filename
    safe_program_name = "".join(c for c in program_name if c.isalnum() or c in (' ', '-', '_')).strip()
    filename = f"{timestamp}_{safe_program_name}.pdf"
    full_path = os.path.join(base_path, filename)
    
    # Write PDF content
    with open(full_path, 'wb') as f:
        f.write(pdf_bytes)
        
def make_request() -> Dict:
    """Make HTTP request to coursedog API and return JSON response."""
    print("Making request to Coursedog API...")
    url = "https://app.coursedog.com/api/v1/cm/ucsb/programs/search/$filters"
    
    params = {
        "catalogId": "P3NC9cCaBC8bbttwtMvN",
        "skip": "0",
        "limit": "999",
        "sortBy": "catalogDisplayName,transcriptDescription,longName,name"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://catalog.ucsb.edu",
        "Referer": "https://catalog.ucsb.edu/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }
    
    payload = {
        "condition": "AND",
        "filters": [
            {
                "condition": "and",
                "filters": [
                    {
                        "id": "WkuYh-program",
                        "name": "WkuYh",
                        "inputType": "boolean",
                        "group": "program",
                        "type": "is",
                        "value": True,
                        "customField": True
                    },
                    {
                        "id": "status-program",
                        "name": "status",
                        "inputType": "select",
                        "group": "program",
                        "type": "is",
                        "value": "Active"
                    }
                ]
            },
            {
                "condition": "AND",
                "filters": [
                    {
                        "group": "program",
                        "id": "type-program",
                        "inputType": "select",
                        "name": "type",
                        "type": "is",
                        "value": "Bachelor's Degree"
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, params=params)
        response.raise_for_status()
        print("Successfully received data from API")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {str(e)}")
        return {"data": []}

def find_featured_courses_field(custom_fields: Dict) -> Optional[str]:
    """Find the field containing featured courses by checking array values."""
    for key, value in custom_fields.items():
        if (isinstance(value, list) and 
            len(value) > 0 and 
            isinstance(value[0], str) and 
            any(value[0].startswith(prefix) for prefix in ['PSTAT', 'MATH', 'CMPSC', 'ANTH'])):
            return key
    return None

def find_files_field(custom_fields: Dict) -> Optional[str]:
    """Find the field containing files by checking for array of objects with name and path."""
    for key, value in custom_fields.items():
        if (isinstance(value, list) and 
            len(value) > 0 and 
            isinstance(value[0], dict) and 
            'name' in value[0] and 
            'path' in value[0] and
            value[0]['name'].endswith(('.pdf', '.docx'))):
            return key
    return None

def parse_program_info(json_data: Dict) -> List[Dict]:
    """Parse program information from JSON data."""
    print("\nParsing program information...")
    programs = []
    
    try:
        data = json_data.get('data', [])
        total_programs = len(data)
        print(f"Found {total_programs} total programs to process")
        
        for i, program in enumerate(data, 1):
            if (program.get('type') == "Bachelor's Degree" and 
                program.get('status') == 'Active'):
                
                program_info = {
                    'name': program.get('name', ''),
                    'college': program.get('college', ''),
                    'featured_courses': [],
                    'files': []
                }
                
                if 'customFields' in program:
                    custom_fields = program['customFields']
                    
                    courses_field = find_featured_courses_field(custom_fields)
                    if courses_field:
                        program_info['featured_courses'] = custom_fields[courses_field]
                    
                    files_field = find_files_field(custom_fields)
                    if files_field:
                        files = custom_fields[files_field]
                        for file in files:
                            program_info['files'].append({
                                'name': file.get('name', ''),
                                'path': file.get('path', '')
                            })
                
                programs.append(program_info)
                
            if i % 10 == 0:  # Print progress every 10 programs
                print(f"Processed {i}/{total_programs} programs...")
    
    except Exception as e:
        print(f"Error parsing program information: {str(e)}")
        return []
    
    print(f"Successfully parsed {len(programs)} Bachelor's Degree programs")
    return programs

def get_signed_urls(programs: List[Dict]) -> List[Dict]:
    """Get signed URLs for all program files."""
    signed_urls = []
    total_files = sum(len(program['files']) for program in programs)
    processed_files = 0
    
    print(f"\nGetting signed URLs for {total_files} files...")
    
    post_headers = {
        "Host": "app.coursedog.com",
        "Content-Length": "0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "application/json, text/plain, */*",
        "Sec-Ch-Ua": '"Not A(Brand";v="8", "Chromium";v="132"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Sec-Ch-Ua-Mobile": "?0",
        "Origin": "https://catalog.ucsb.edu",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://catalog.ucsb.edu/",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i"
    }

    for program in programs:
        for file in program['files']:
            try:
                post_link = f"https://app.coursedog.com/api/v1/ucsb/files/signedUrl?fileName={file['path']}&type=get&bucketName=coursedog-static-public"
                post_response = requests.post(post_link, headers=post_headers)
                post_response.raise_for_status()
                
                url_data = {
                    'program_name': program['name'],
                    'file_name': file['name'],
                    'signed_url': post_response.json()
                }
                signed_urls.append(url_data)
                
                processed_files += 1
                if processed_files % 5 == 0:  # Print progress every 5 files
                    print(f"Retrieved signed URLs for {processed_files}/{total_files} files...")
                
                # Optional delay to avoid rate limiting
                time.sleep(0.5)  # Added small delay to avoid overwhelming the server
                
            except requests.exceptions.RequestException as e:
                print(f"Error getting signed URL for {file['name']}: {str(e)}")
                continue
    
    print(f"Successfully retrieved {len(signed_urls)} signed URLs")
    return signed_urls

def display_program_info(programs: List[Dict], signed_urls: List[Dict]) -> None:
    """Display formatted program information and signed URLs."""
    print("\nDisplaying program information...")
    
    if not programs:
        print("No programs found or error occurred during parsing.")
        return
        
    for i, program in enumerate(programs, 1):
        print(f"\nProgram {i}:")
        print(f"Name: {program['name']}")
        print(f"College: {program['college']}")
        
        if program['featured_courses']:
            print("\nFeatured Courses:")
            for course in program['featured_courses']:
                print(f"- {course}")
        
        if program['files']:
            print("\nFiles:")
            for file in program['files']:
                print(f"- Name: {file['name']}")
                print(f"  Path: {file['path']}")
                
                # Find and display corresponding signed URL
                for url_data in signed_urls:
                    if url_data['program_name'] == program['name'] and url_data['file_name'] == file['name']:
                        print(f"  Signed URL: {url_data['signed_url']}")
                        break
                
        print("-" * 50)



def download_pdf(url: str) -> bytes:
    """Download PDF from URL and return as bytes."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {str(e)}")
        return None

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF using PyPDF2 first, then OCR if needed."""
    if not pdf_bytes:
        return ""

    # Try PyPDF2 first
    try:
        pdf = PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        
        # If we got meaningful text, return it
        if len(text.strip()) > 50:  # Arbitrary threshold to check if we got real text
            return text
    except Exception as e:
        print(f"Error with PyPDF2 extraction: {str(e)}")

    # If PyPDF2 failed or didn't get enough text, try OCR
    try:
        print("Attempting OCR extraction...")
        images = convert_from_bytes(pdf_bytes)
        text = ""
        for i, image in enumerate(images):
            print(f"Processing page {i+1} with OCR...")
            text += pytesseract.image_to_string(image) + "\n"
        return text
    except Exception as e:
        print(f"Error with OCR extraction: {str(e)}")
        return ""

def save_to_file(program_name: str, file_name: str, url: str, text: str, base_path: str):
    """Save extracted text and metadata to file."""
    # Create directory if it doesn't exist
    os.makedirs(base_path, exist_ok=True)
    
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create filename
    safe_program_name = "".join(c for c in program_name if c.isalnum() or c in (' ', '-', '_')).strip()
    filename = f"{timestamp}_{safe_program_name}.txt"
    full_path = os.path.join(base_path, filename)
    
    # Write content to file
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(f"Program: {program_name}\n")
        f.write(f"File: {file_name}\n")
        f.write(f"URL: {url}\n")
        f.write("\n=== EXTRACTED TEXT ===\n\n")
        f.write(text)
        f.write("\n\n" + "="*50 + "\n")
    
    print(f"Saved content to: {full_path}")


def process_signed_urls(signed_urls: List[Dict], base_path: str):
    """Process each signed URL to download and save PDFs."""
    print(f"\nDownloading {len(signed_urls)} PDFs...")
    
    for i, url_data in enumerate(signed_urls, 1):
        print(f"\nDownloading PDF {i}/{len(signed_urls)}")
        print(f"Program: {url_data['program_name']}")
        print(f"File: {url_data['file_name']}")
        
        try:
            # Download PDF
            print("Downloading PDF...")
            response = requests.get(url_data['signed_url'])
            response.raise_for_status()
            
            # Save PDF and metadata
            save_pdf(
                url_data['program_name'],
                url_data['file_name'],
                url_data['signed_url'],
                response.content,
                base_path
            )
            
        except requests.exceptions.RequestException as e:
            print(f"Error downloading PDF: {str(e)}")
            continue
        
        print(f"Completed downloading PDF {i}/{len(signed_urls)}")
        time.sleep(1)  # Add delay between downloads

def main():
    """Main function to fetch and parse program data."""
    print("Starting program data collection...")
    
    # Make the HTTP request to get the data
    json_data = make_request()
    
    # Parse program information
    programs = parse_program_info(json_data)
    
    # Get signed URLs for all files
    signed_urls = get_signed_urls(programs)
    
    # Process and save PDFs
    pdf_path = r"C:\Users\bentu\Downloads\VulnTestResult\all PDF Major Sheets"
    process_signed_urls(signed_urls, pdf_path)
    
    print("\nProgram completed successfully!")

if __name__ == "__main__":
    main()
