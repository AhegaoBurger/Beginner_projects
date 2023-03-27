def docx_replace_regex(doc_obj, regex, replace):
    for p in doc_obj.paragraphs:
        if regex.search(p.text):
            inline = p.runs
            # Loop added to work with runs (strings with same style)
            for i in range(len(inline)):
                if regex.search(inline[i].text):
                    text = regex.sub(replace, inline[i].text)
                    inline[i].text = text
    for table in doc_obj.tables:
        for row in table.rows:
            for cell in row.cells:
                docx_replace_regex(cell, regex, replace)


regex1 = compile(r"D:\\Artur\\Database\\sample01.docx", filename= sample01.docx)
replace1 = r""
filename = r"D:\\Artur\\Database\\sample01.docx"
doc = Document(filename)
docx_replace_regex(doc, regex1, replace1)
doc.save('sample01.docx')