import csv

def write_sorted():
    # Otevření vstupního souboru CSV
    with open('eda\output_for_deleting.csv', 'r') as input_file:
        reader = csv.reader(input_file)
        rows = list(reader)

    # Vytvoření seznamu čísel ve třetím sloupci
    numbers = []
    for row in rows:
        number = row[2]
        numbers.append(number)

    #musí být seřazený za sebou
    # Kontrola, zda se v seznamu čísel vyskytují duplicity
    has_duplicates = False
    line_deleted = False
    updated_rows = []
    for i in range(len(numbers)):
        if line_deleted == False:
            j = i+1
            row_i = rows[i]
            row_j = rows[j]
            if numbers[i] == numbers[j]:
                line_deleted = True
                if row_i[3] == 'True' and row_j[3] == 'True':
                    updated_rows.append(row_i)
                elif row_i[3] == 'True':
                    updated_rows.append(row_i)
                elif row_j[3] == 'True': 
                    updated_rows.append(row_j)
                else:
                    updated_rows.append(row_i)
            else:
                updated_rows.append(row_i)
        else:
            line_deleted = False



    # Otevření výstupního souboru CSV
    with open('eda\output_delete_duplicite.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(updated_rows)

write_sorted()
