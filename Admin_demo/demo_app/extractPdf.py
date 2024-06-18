



import pdfplumber
import json

json_data = []
def extract(file_path):
    json_data =[]

    with pdfplumber.open(file_path) as pdf:

        total_pages = len(pdf.pages)
        for i in range(total_pages):
            page = pdf.pages[i]
            tables = page.extract_tables()
            for table_data in tables:
        
                for row in table_data:
                    policy_data = {}

                    for cell in row:

                        if cell is not None:
                            lines = cell.split('\n')
                            for line in lines:
                                key_value = line.split(':',1)

                                if len(key_value) ==2:
                                    key ,value = key_value
                                    key = key.strip()
                                    value = value.strip()

                                    if key in ['Policy Number', 'Invoice Number', 'Reverse Charge', 'Name of Insured/Proposer', 'Address', 'Place of Supply', 'GSTIN / UIN Number', 'Pan Number', 'Period of Insurance','Address of Service Provider', 'Area Code', 'FGI State Code', 'FGI GSTIN Number', 'FGI Pan Number', 'Intermediary Name/Code', 'Date of Issue/Invoice date', 'HSN', 'Nature of Service']:
                                        policy_data[key] = value
            
                if len(policy_data)>0:
                    
                    json_data.append(policy_data)


    return json_data







