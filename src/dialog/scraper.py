from bs4 import BeautifulSoup as BS
import requests as req


BASE_URL = "https://dialog.ru/catalog/lekarstva_i_bady/"

response = req.get(BASE_URL)
soup = BS(response.text, 'lxml')
