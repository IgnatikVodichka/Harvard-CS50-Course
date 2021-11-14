import csv
import sys


database = []
suspects = []
dna_sample = ""

# stipulating the number of command line arguments
if len(sys.argv) != 3:
    sys.exit("Usage: dna.py [file with persons] [file with DNA sequence]")

# open a file for reading database
with open(sys.argv[1], "r") as file:
    reader = csv.DictReader(file)
    for person in reader:
        for key in person:
            if key != "name":
                person[key] = int(person[key])
        database.append(person)
        # making copy of dictionary to modify it later
        suspects.append(person.copy())

# opening file to read DNA sample from the lab
with open(sys.argv[2], "r") as file:
    dna_sample = file.read()

# changing all values to 0 to count after
for person in suspects:
    for key in person:
        if key != "name":
            person[key] = 0

for suspect in suspects:
    for key in suspect:
        j = len(key)
        if key != "name":
            counter = 0
            # count how many sequences we have
            while key*(counter+1) in dna_sample:
                counter += 1
            suspect[key] = counter
# now we have 2 lists with 2 dictionaries, and if two is completely identical that's out match, else: No match.
for (person, suspect) in zip(database, suspects):
    if person == suspect:
        print(person["name"])
        exit(0)
    else:
        continue
print("No match")