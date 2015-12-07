# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from bs4 import BeautifulSoup as bs
import requests

if __name__ == "__main__":
  url = "http://www.pagesjaunes.fr/"
  r = requests.get(url)
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
  
  
  