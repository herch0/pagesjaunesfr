# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from bs4 import BeautifulSoup as bs
import requests
import re

cookies = None

def next_page(url, page):
  global cookies
  url = 'http://www.pagesjaunes.fr' + url + '&page=' + str(page)
  r = requests.get(url, cookies=cookies)
  cookies = r.cookies
  soup = bs(r.text, 'html.parser')
  results = soup.select('.bi-pro.bi-bloc.blocs')
  for rs in results:
    nom = rs.select_one('.denomination-links.pj-link')
    adresse = rs.select_one('.adresse.pj-lb.pj-link')
    type_num = rs.select_one('div.item.bi-contact-tel > span > span')
    num = rs.select_one('div.item.bi-contact-tel > span strong')
    print((nom.string.strip() if nom != None and nom.string != None else ''), 
          (adresse.string.strip() if adresse != None and adresse.string != None else ''), 
          (type_num.string.strip() if type_num != None and type_num.string != None else ''), 
          (num.string.strip() if num != None and num.string != None else ''))
  # end for
# end next_page

if __name__ == "__main__":
  regex_url_next = re.compile(r'"technicalUrl":"(.*?)"');
  r = requests.get("http://www.pagesjaunes.fr/")
  cookies = r.cookies
  post_params = {
    'pj4valid':'true',
    'quoiqui':'medecin generaliste',
    'ou':'07',
    'idOu':'',
    'quiQuoiSaisi':'',
    'quiQuoiNbCar':'',
    'acOuSollicitee':'1',
    'rangOu':'',
    'sourceOu':'',
    'typeOu':'',
    'nbPropositionOuTop':'5',
    'nbPropositionOuHisto':'0',
    'ouSaisi':'',
    'ouNbCar':'',
    'acQuiQuoiSollicitee':'1',
    'rangQuiQuoi':'1',
    'sourceQuiQuoi':'HISTORIQUE',
    'typeQuiQuoi':'1',
    'idQuiQuoi':'8185bc09fe552aec77ac544fa7fc61c1',
    'nbPropositionQuiQuoiTop':'0',
    'nbPropositionQuiQuoiHisto':'1',
  }
  r = requests.post('http://www.pagesjaunes.fr/annuaire/chercherlespros', data=post_params, cookies=cookies)
  cookies = r.cookies
  soup = bs(r.text, 'html.parser')
  nb_result = soup.select_one('#SEL-nbresultat').string
  nb_pages = (int(nb_result) // 20) + 1
  print(nb_result, nb_pages)
  results = soup.select('.bi-pro.bi-bloc.blocs')
  page = 1
  url_next = ''
  match = regex_url_next.search(r.text, re.MULTILINE)
  if (match):
    url_next = match.group(1)
  while page <= nb_pages:
    print("page", page)
    for rs in results:
      nom = rs.select_one('.denomination-links.pj-link')
      adresse = rs.select_one('.adresse.pj-lb.pj-link')
      type_num = rs.select_one('div.item.bi-contact-tel > span > span')
      num = rs.select_one('div.item.bi-contact-tel > span strong')
      print((nom.string.strip() if nom != None and nom.string != None else ''), 
            (adresse.string.strip() if adresse != None and adresse.string != None else ''), 
            (type_num.string.strip() if type_num != None and type_num.string != None else ''), 
            (num.string.strip() if num != None and num.string != None else ''))
    # end for
    page+=1
    if url_next:
      next_page(url_next, page)
  # end while