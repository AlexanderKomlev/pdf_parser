import fitz
import re
import tqdm


from googletrans import Translator
from db.models import Data


def database_entry(session, id, data_length, length, name, scaling, range, spn):
    """
    Запись данных в базу данных
    """

    translator = Translator()

    # print(id)
    # print(data_length)
    # print(length)
    # print(name)
    # print(translator.translate(name, src='English', dest='Russian').text)
    # print(scaling)
    # print(range)
    # print(spn)
    # print("__________________________")

    session.add(Data(id=id, 
                     data_length=data_length, 
                     length=length, 
                     name=name, 
                     rus_name=translator.translate(name, src='English', dest='Russian').text, 
                     scaling=scaling, 
                     range=range, 
                     spn=spn))
    session.commit()
    

def sort_pdf(pdf_file):
    """
    Извлечение данных из pdf файла
    """

    doc = fitz.open(pdf_file)
    doc1 = ""
    doc2 = ""

    for page in doc:
        if "Parameter Name" in page.get_text():
            doc1 += page.get_text(sort=True)
        if "Parameter Group Name and Acronym" in page.get_text():
            doc2 += page.get_text(sort=True)
    
    doc1 = doc1.split("Data Length: \n")[1:3]
    doc2 = doc2.split("-71 \n5.2")[1:]

    return doc1, doc2


def get_additional_parameters(session, doc2, pgn, paragraph, parameter_name, id, data_length, length):

    pattern = re.compile(r"Slot Scaling:[\s0-9\W\w]*SPN: \n\d*")
    tqdm_doc2 = tqdm.tqdm(doc2, ascii=True, colour='blue')

    for el in tqdm_doc2:
        if paragraph[3:] in el and parameter_name in el and pgn in el:
            group = pattern.findall(el)[0].split("\n")
            scaling = group[0][13:]
            range = group[4]
            spn = group[-1]
            database_entry(session, id, data_length, length, parameter_name, scaling, range, spn)


def parsing_pdf(pdf_file, session):
    """
    Парсинг pdf файла
    """

    doc1, doc2 = sort_pdf(pdf_file)
    tqdm_doc1 = tqdm.tqdm(doc1, ascii=True, colour='white')
    for el in tqdm_doc1:
        data_length = el.split("Data")[0].strip()
        parameter_group = el.split("Parameter Group  \n")[1][0:13].split("\n( ")
        pgn = parameter_group[0].strip()
        id = parameter_group[1].strip("\n )")
        pattern = re.compile(r'\d{1} b[a-zA-Z\s\d\-\.\?()]*\d{1,2}/\d{1,2}/\d{4}')
        pbar = tqdm.tqdm(pattern.findall(el), ascii=True, colour='black')

        for line in pbar:
            parameter_name = line.split("\n")[1].strip(" ")
            paragraph = line.split("\n")[3].strip(" ")
            length = line.split("\n")[0].strip(" ")
            
            get_additional_parameters(session, doc2, pgn, paragraph, parameter_name, id, data_length, length)
