import csv

if __name__ == "__main__":
  with open('charpente.csv', mode = 'r', newline='') as csvfile, open('charpente2.csv', mode ='w', newline='') as csvout:
    reader = csv.reader(csvfile, delimiter=',')
    writer = csv.writer(csvout, delimiter=';')
    for row in reader:
      writer.writerow(row)
    
