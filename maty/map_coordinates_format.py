import csv

def main():
    var = list()
    file_name = r'C:\Users\kiv\Documents\GitHub\astrox2\astrox\Tabulka bez názvu - List 5.csv'
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            tuple = (float(row[0]), float(row[1]))
            print(tuple)
            var.append(tuple)
    return var

if __name__ == "__main__":
    main()