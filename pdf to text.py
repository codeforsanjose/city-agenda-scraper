#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Krammy
#
# Created:     26/01/2021
# Copyright:   (c) Krammy 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import io
import pikepdf
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(path):
    '''Convert pdf content from a file path to text

    :path the file path
    '''
    rsrcmgr = PDFResourceManager()
    codec = 'utf-8'
    laparams = LAParams()

    with io.StringIO() as retstr:
        with TextConverter(rsrcmgr, retstr, codec=codec,
                           laparams=laparams) as device:
            with open(path,'rb') as fp:
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                password = ""
                maxpages = 0
                caching = True
                pagenos = set()

                for page in PDFPage.get_pages(fp,
                                              pagenos,
                                              maxpages=maxpages,
                                              password=password,
                                              caching=caching,
                                              check_extractable=True):
                    interpreter.process_page(page)

                return retstr.getvalue()


#change filename to be full directory
path = './city-agenda-scraper/Report_samples/'
for filename in os.listdir(path):
    if filename.endswith(".pdf"):
        pdf = pikepdf.open(path+filename)
        pdf.save(path+'EXTRACT_'+filename)
        output_file = open(path + 'text_files/' + filename.replace('.pdf', '.txt'), 'w')
        try:
            output_file.write(convert_pdf_to_txt(path+'EXTRACT_'+filename))
        except Exception as e:
            print(filename + " unsuccessful")
            print(str(type(e)))
            print(str(e.args))
            continue
        output_file.close()
        continue
    else:
        continue
