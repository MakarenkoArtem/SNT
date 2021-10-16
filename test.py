'''from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run()''''''
from PyPDF2 import PdfFileReader, PdfFileWriter
pdf_document = "a.pdf"
pdf = PdfFileReader(pdf_document)
for page in range(pdf.getNumPages()):
    pdf_writer = PdfFileWriter()
    current_page = pdf.getPage(page)
    pdf_writer.addPage(current_page)
    print(pdf_writer)
    outputFilename = "dist/Computer-Vision-Resources-page-{}.png".format(page + 1)
    with open(outputFilename, "wb") as out:
        pdf_writer.write(out)
        print("created", outputFilename)
        
from pdf2image import convert_from_path


images = convert_from_path(open('a.pdf', 'rb').read())

for page_no, image in enumerate(images):
    image.save(f'page-{page_no}.jpeg')
import pip

pip.main(['install', 'pdf2image'])
pip.main(['install', 'poppler-utils'])
from pdf2image import convert_from_path

images = convert_from_path('a.pdf', 500)

for page_no, image in enumerate(images):
    image.save(f'static/img/page-{page_no}.jpeg')'''
import fitz

pdffile = "a.pdf"
doc = fitz.open(pdffile)
for i in range(len(doc)):
    page = doc.loadPage(i)  # number of page
    pix = page.getPixmap()
    output = f"outfile{i}.png"
    pix.writePNG(output)