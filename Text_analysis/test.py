import pickle

raw = pickle.load(open("./meeting_minutes_html.pkl", "rb"))
articles = [a for k, a in raw.items()]

with open("sj1.txt", "w") as f:
    f.write(raw["SanJose_Legistar_01-05-2021.pdf"])

with open("sj1_rogc_minutes.txt", "w") as f:
    f.write(raw["(a) 9232020 ROGC Minutes.pdf"])


# Testing different ways of extracting pdf content
filename = "../Agenda_samples/SanJose_Legistar_01-05-2021.pdf"
import PyPDF2
import textract

pdfFileObj = open(filename, "rb")  # open allows you to read the file
pdfReader = PyPDF2.PdfFileReader(
    pdfFileObj
)  # The pdfReader variable is a readable object that will be parsed
count = 0
original_text = ""
num_pages = (
    pdfReader.numPages
)  # discerning the number of pages will allow us to parse through all the pages

while count < num_pages:  # The while loop will read each page
    pageObj = pdfReader.getPage(count)
    count += 1
    original_text += pageObj.extractText()

print(original_text)
with open("sj1_pypdf.txt", "w") as f:
    f.write(original_text)
