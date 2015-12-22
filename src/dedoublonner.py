
import argparse
import csv

if __name__ == "__main__":
  uniques = []
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--input")
  parser.add_argument("-o", "--output")
  parser.add_argument("-c", "--colonne", type=int)
  args = parser.parse_args()
  if args.input and args.output and args.colonne:
    with open(args.input, mode='r', newline='') as csvfile, open(args.output, mode='w', newline='') as csvout:
      reader = csv.reader(csvfile, delimiter=';')
      writer = csv.writer(csvout, delimiter=';')
      for row in reader:
        if len(row) > 0:
          val = row[args.colonne]
          val = val.lstrip('.').strip()
          row[args.colonne] = val
          if val not in uniques:
            writer.writerow(row)
            uniques.append(val)
          #end if
        # end if
      # end for
    # end with
  # end if
  else:
    print("Usage: dedoublonner -i 'fichier entrée' -o 'fichier sortie' -c 'colonne sur laquelle dédoublonner'")
  # end else
