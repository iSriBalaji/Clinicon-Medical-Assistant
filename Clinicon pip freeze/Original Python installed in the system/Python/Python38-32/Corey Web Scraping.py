from bs4 import BeautifulSoup as bs
import requests

#getting the source code of webpage
url = 'https://coreyms.com/'
html_output_name = 'coreyHTML'

req = requests.get(url, 'html.parser')

with open(html_output_name, 'w') as f:
    f.write(req.text)
    f.close()
