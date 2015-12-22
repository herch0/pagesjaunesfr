# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from bs4 import BeautifulSoup as bs
import csv
import json
import re
import requests
import time

cookies = None
writer = None

#proxies = {
#  "https": "https://212.112.102.43:8080",
#  "http": "http://101.26.38.162:80",
#}

proxies = None

headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.73 Chrome/47.0.2526.73 Safari/537.36',
}

def details(url):
  global cookies, proxies, headers
  print(url)
  try:
    r = requests.get(url, cookies=cookies, proxies=proxies, headers=headers, timeout=30)
  except requests.exceptions.Timeout as e:
    print(e)
    r = requests.get(url, cookies=cookies, proxies=proxies, headers=headers, timeout=30)
  cookies = r.cookies
  soup = bs(r.text, 'html.parser')
  activite = soup.select_one(".coord-rubrique")
  dict_details = {'tel': [], 'fax': [], 'mobile': [], 'activite': activite.string.strip() if activite else ''}
  li_tel = soup.select("#coord-liste-numero_1 li")
  for li in li_tel:
    type_num = li.select_one('.num-tel-label')
    num = li.select_one('.coord-numero')
    if (type_num and num):
      type_num = type_num.string[:3] if type_num else ''
      num = num.string.strip() if num else ''
      if type_num.lower() == 'tél':
        dict_details['tel'].append(num)
      elif type_num.lower() == 'fax':
        dict_details['fax'].append(num)
      elif type_num.lower() == 'mob':
        dict_details['mobile'].append(num)
#  print('fin details')
  return dict_details
# end details()

def first_request(activite, departement):
  global cookies, regex_url_next, writer, proxies, headers
  try:
    r = requests.get("http://www.pagesjaunes.fr/", proxies=proxies, headers=headers, timeout=30)
  except requests.exceptions.Timeout as e:
    print(e)
    r = requests.get("http://www.pagesjaunes.fr/", proxies=proxies, headers=headers, timeout=30)
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
  try:
    r = requests.post('http://www.pagesjaunes.fr/annuaire/chercherlespros', data=post_params, cookies=cookies, proxies=proxies, headers=headers, timeout=30)
  except requests.exceptions.Timeout as e:
    print(e)
    r = requests.post('http://www.pagesjaunes.fr/annuaire/chercherlespros', data=post_params, cookies=cookies, proxies=proxies, headers=headers, timeout=30)
  cookies = r.cookies
  soup = bs(r.text, 'html.parser')
  nb_result = 0
  if soup.select_one('#SEL-nbresultat'):
    nb_result = soup.select_one('#SEL-nbresultat').string.replace(' ', '')
  else:
    print(r.text)
  nb_pages = (int(nb_result) // 20) + 1
  print(nb_result, nb_pages)
  page = 1
  url_next = ''
  match = regex_url_next.search(r.text, re.MULTILINE)
  if (match):
    url_next = match.group(1)
  
  while page <= nb_pages:
    print("page", page)
    url = 'http://www.pagesjaunes.fr' + url_next + '&page=' + str(page)
    data = lire_page(url)
    for infos in data:
      row = {'nom': infos['nom'], 'adresse': infos['adresse'], 'activite1': infos['activite'], 'activite2': activite, 'dept': departement}
      tels = infos['tel']
      row['tel_1'] = tels[0] if len(tels) > 0 else ''
      row['tel_2'] = tels[1] if len(tels) > 1 else ''
      row['fax'] = infos['fax'][0] if len(infos['fax']) > 0 else ''
      row['mobile'] = infos['mobile'][0] if len(infos['mobile']) > 0 else ''
      writer.writerow(row)
    # end for
    page += 1
  # end while
# fin first_request

def lire_page(url):
  global cookies, proxies, headers
#  print('debut lire_page')
  try:
    r = requests.get(url, cookies=cookies, proxies=proxies, headers=headers, timeout=30)
  except requests.exceptions.Timeout as e:
    print(e)
    r = requests.get(url, cookies=cookies, proxies=proxies, headers=headers, timeout=30)
  cookies = r.cookies
  soup = bs(r.text, 'html.parser')
  results = soup.select('.bi-pro.bi-bloc.blocs')
  data = []
  for rs in results:
    json_str = rs["data-pjtoggleclasshisto"]
    dict_json = json.loads(json_str)
    id_bloc = dict_json['idbloc']['id_bloc']
    if (dict_json['idbloc']['no_sequence'].lstrip('0') != ''):
      str_no_sequence = dict_json['idbloc']['no_sequence'].lstrip('0')
      no_sequence = int(str_no_sequence)
    else:
      no_sequence = 0
    nom = rs.select_one('.denomination-links.pj-link')
    adresse = rs.select_one('.adresse.pj-lb.pj-link')
    d = details(r"http://www.pagesjaunes.fr/pros/detail?bloc_id=%s&no_sequence=%d#ancreBlocCoordonnees" % (id_bloc, no_sequence))
    d['nom'] = nom.string.strip() if nom else ''
    d['adresse'] = adresse.string.strip() if adresse else ''
    data.append(d)
  # end for
  return data
# end data()

if __name__ == "__main__":
  regex_url_next = re.compile(r'"technicalUrl":"(.*?)"');
  departements = [
  "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "2A", "2B", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95"]
  with open('construction4.csv', mode='w', newline='') as extract:
    fieldnames = ['nom', 'adresse', 'tel_1', 'tel_2', 'fax', 'mobile', 'activite1', 'activite2', 'dept']
    writer = csv.DictWriter(extract, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    for d in departements:
      print("Département %s" % d)
      try:
        first_request('construction', d)
      except Exception as e:
        print(e)
        try:
          first_request('construction', d)
        except Exception as e:
          print(e)
          continue
  # end for
  
#  'NoneType' object has no attribute 'string'