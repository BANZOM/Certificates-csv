from bs4 import BeautifulSoup
import csv

def extract_certificate_info(li_element):
    """
    Extract certificate information from a single li element
    
    Args:
        li_element (BeautifulSoup): BeautifulSoup element for a single certificate
        
    Returns:
        dict: Dictionary containing certificate information
    """
    try:
        name_element = li_element.find('span', {'aria-hidden': 'true'}, recursive=True)
        certificate_name = ' '.join(name_element.text.strip().split()) if name_element else None
        
        link_element = li_element.find('a', {
            'class': 'optional-action-target-wrapper',
            'aria-label': lambda x: x and 'Show credential for' in x if x else False
        })
        certificate_link = link_element.get('href') if link_element else None
        
        org_element = li_element.find('span', {'class': 't-14 t-normal'})
        organization = ' '.join(org_element.text.strip().split()) if org_element else None
        
        date_element = li_element.find('span', {'class': 'pvs-entity__caption-wrapper'})
        issue_date = ' '.join(date_element.text.strip().split()) if date_element else None
        
        return {
            'name': certificate_name,
            'link': certificate_link,
            'organization': organization,
            'issue_date': issue_date
        }
    except Exception as e:
        return {
            'error': f'Failed to parse certificate info: {str(e)}',
            'name': None,
            'link': None,
            'organization': None,
            'issue_date': None
        }

def process_certificates_file(input_file, output_file):
    """
    Process certificates from input file and save to CSV
    
    Args:
        input_file (str): Path to input text file containing certificates HTML
        output_file (str): Path to output CSV file
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        certificates = soup.find_all('li', {'class': 'pvs-list__paged-list-item'})
        
        cert_data = []
        for cert in certificates:
            cert_info = extract_certificate_info(cert)
            if cert_info['name'] is not None:  # Only add if we successfully extracted a name
                cert_data.append(cert_info)
        
        if cert_data:
            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['name', 'link', 'organization', 'issue_date'])
                writer.writeheader()
                writer.writerows(cert_data)
            print(f"Successfully processed {len(cert_data)} certificates and saved to {output_file}")
        else:
            print("No valid certificates found to process")
            
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found")
    except Exception as e:
        print(f"Error processing certificates: {str(e)}")

if __name__ == "__main__":
    process_certificates_file("certificate.txt", "certificates.csv")