import pandas as pd
from fpdf import FPDF
import csv
import os

class Certificate(FPDF):
    def header(self):
        # Set up the certificate header
        self.set_font('Arial', 'B', 18)
        self.cell(0, 10, 'CERTIFICADO', 0, 1, 'C')
        self.ln(20)

    def add_certificate(self,text):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, f'{text}')

def get_formated_string(text,row):

    new_text = text

    # Replace 'var' for each item of the list/row. The '1' parameter in replace specifies that 1 'var' substring should be replace each time
    for item in row:
        new_text = new_text.replace('var',item,1)

    #print(new_text)

    return new_text

def generate_certificate(text,row):

    # Replace var with the data in the rows
    f_text = get_formated_string(text,row)

    
    # Generate certificate

    # Create an instance of the Certificate class
    certificate = Certificate()
    # Add a page and generate the certificate
    certificate.add_page()
    certificate.add_certificate(f_text)
    # Output the generated PDF with the receiver name as the prefix
    certificate.output('processed/'+row[0]+'-certificado.pdf')

def main(file_path):

    # Text for testing. In prod version, the text will be a parameter from the application
    #text = 'var participou em var de var em var'
    with open(file_path, newline='') as f:
            reader = csv.reader(f)

            text = next(reader) # first row
            text = text[0]
            #print('text',text)
            for row in reader:
                #generate_certificate_v1(row)
                generate_certificate(text,row)

if __name__=="__main__":
    main(file_path="")