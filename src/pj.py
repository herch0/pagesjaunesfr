# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from bs4 import BeautifulSoup as bs
import requests
import re
import json

cookies = None

def next_page(url, page):
  global cookies
  url = 'http://www.pagesjaunes.fr' + url + '&page=' + str(page)
  print(url)
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

def data(activite, departement):
  global cookies, regex_url_next
  r = requests.get("http://www.pagesjaunes.fr/")
  cookies = r.cookies
  post_params = {
    'pj4valid':'true',
    'quoiqui': activite,
    'ou':departement,
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
#    'idQuiQuoi':'8185bc09fe552aec77ac544fa7fc61c1',
    'idQuiQuoi':'',
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
      json_str = rs["data-pjtoggleclasshisto"]
      dict_json = json.loads(json_str)
      id_bloc = dict_json['idbloc']['id_bloc']
      if (dict_json['idbloc']['no_sequence']):
        no_sequence = int(dict_json['idbloc']['no_sequence'].lstrip('0'))
      else:
        no_sequence = ''
      print(id_bloc, no_sequence)
      nom = rs.select_one('.denomination-links.pj-link')
      plus_details = rs.select_one('.item.plus-coordonnees')  
      adresse = rs.select_one('.adresse.pj-lb.pj-link')
      phone1 = ''
      phone2 = ''
      mobile = ''
      fax = ''
      if (plus_details):
        details(r"http://www.pagesjaunes.fr/pros/detail?bloc_id=%s&no_sequence=%d#ancreBlocCoordonnees" % (id_bloc, no_sequence));        
      else:
        type_num = rs.select_one('div.item.bi-contact-tel > span > span')
        num = rs.select_one('div.item.bi-contact-tel > span strong')
      print((nom.string.strip() if nom != None and nom.string != None else ''), 
            (adresse.string.strip() if adresse != None and adresse.string != None else ''))
    # end for
    page+=1
    if url_next:
      next_page(url_next, page)
  # end while
# end data()

def details(url):
  global cookies
  r = requests.get(url, cookies=cookies)
  cookies = r.cookies
  soup = bs(r.text, 'html.parser')
  li_tel = soup.select("#coord-liste-numero_1 li")
  for li in li_tel:
    print(li.select_one('.coord-numero').string)
# end details()

if __name__ == "__main__":
  regex_url_next = re.compile(r'"technicalUrl":"(.*?)"');
#  departements = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","2A","2B","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95"]
#  for d in departements:
#    print("Département %s" % d)
  data('medecins generalistes', "01")
  # end for