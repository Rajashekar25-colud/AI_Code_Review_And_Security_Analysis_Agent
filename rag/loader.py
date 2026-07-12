import os

from pypdf import PdfReader



def load_documents(folder):

    documents = []


    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            path = os.path.join(
                folder,
                file
            )


            reader = PdfReader(path)


            text = ""


            for page in reader.pages:

                text += page.extract_text()



            documents.append(text)


    return documents