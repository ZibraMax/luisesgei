import requests
import os


def download_pdf(url, pdfname, folder):

    r = requests.get(url)
    with open(f'{folder}/{pdfname}.pdf', 'wb') as fd:
        for chunk in r.iter_content(2000):
            fd.write(chunk)
