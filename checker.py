import PyPDF2, os, re, datetime, operator

payStatements = []

for filename in os.listdir('./pay_statements/'):
    if filename.endswith('.pdf'):
        # collect all pay statements and extract text
        pdfFileObj = open('./pay_statements/' + filename, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0)
        text = pageObj.extractText()

        # collect pay dates
        dateRegex = re.compile(r'\d{4}-\d{2}-\d{2}')
        dateString = dateRegex.search(filename).group(0)

        # search for available sick time
        cleanCopy = re.sub(r'\n', ' ', text)
        sickTimeRegex = re.compile(r'(?<=Sick Available )\d{2} \d{2}')
        isSickTime = sickTimeRegex.search(cleanCopy)

        # sick time cannot be higher than 72, if it is the text extraction errored.
        # the error pattern seems to be that sick hours are trailing "Other Benefits and "
        if isSickTime.group(0) > '72 00':
            errorRegex = re.compile(r'(?<=Other Benefits and )\d{2} \d{2}')
            isSickTime = errorRegex.search(cleanCopy)

        payStatements.append({'date': dateString, 'sick hours': isSickTime.group(0)})

# sort by date
payStatements.sort(key = operator.itemgetter('date'))

# known bug: when sick hours are maxed, check that following pay period hours are not
# suspended below 72 consecutively.

print(payStatements)