
import fitz
pdf_filename = "static/a.pdf"
doc = fitz.open(pdf_filename)
for i in range(len(doc)):
    print(i, doc.getPageImageList(i))
    for img in doc.getPageImageList(i):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        print(doc, img, f"{i}.png")
        #if pix.n < 5:       # this is GRAY or RGB
        #    pix.writePNG(f"{i}.png")
        #else:               # CMYK: convert to RGB first
        if 1:
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            pix1.writePNG(f"{i}.png")
            pix1 = None
        pix = None