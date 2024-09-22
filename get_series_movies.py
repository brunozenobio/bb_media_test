from bs4 import BeautifulSoup
import requests
from scrapping_py import *
from playwright.sync_api import sync_playwright
import re


datos = get_data(run())

print(datos)