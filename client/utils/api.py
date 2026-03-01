import requests
from config import API_URL


def upload_pdfs_api(files):
    files_payload=[ ("files",(f.name,f.read(),"application/pdf")) for f in files]   ## to ensure that uploaded file(s) are in pdf format
    return requests.post(f"{API_URL}/upload_pdfs/",files=files_payload)




def ask_question(question):
    

    return requests.post(f"{API_URL}/ask/",data={"question":question})
    