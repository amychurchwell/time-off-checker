import PyPDF2, os

pdfFiles = []

for filename in os.listdir('./pay_statements/'):
    if filename.endswith('.pdf'):
        pdfFileObj = open('./pay_statements/' + filename, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0)
        text = pageObj.extractText()
        pdfFiles.append(text)
        print(pdfFiles)