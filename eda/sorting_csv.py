import csv



class main():
    def write_missing(input_file, output_file):
        with open(input_file, 'r') as input_file:
            reader = csv.reader(input_file)
            next(reader)  # Přeskočení záhlaví
            rows = list(reader)

            # Vytvoření seznamu čísel ve třetím sloupci
            numbers = []
            for row in rows:
                number = int(row[2])
                numbers.append(number)
            image_name = row[0]
            p=row[-2]
            i=row[-1]
            for y in range(max(numbers)):
                if y not in numbers:
                    rows.append((image_name, '', y, 'False', '', '', '', '', '', '', '', '', p, i))
            print(rows)    


    def write_sorted(input_file, output_file):  
        with open(input_file, 'r') as input_file:
            reader = csv.reader(input_file)
            next(reader)  # Přeskočení záhlaví
            rows = list(reader)

            # Vytvoření seznamu čísel ve třetím sloupci
            numbers = []
            for row in rows:
                number = row[2]
                numbers.append(number)
            end = False
            for i in range(len(numbers)-1):
                numbers = []
                for row in rows:
                    number = row[2]
                    numbers.append(number)
                for j in range(i+1, len(numbers)):
                    if numbers[i] == numbers[j]:
                        row_i = rows[i]
                        row_j = rows[j]
                        line_deleted = True
                        if row_i[3] == 'True' and row_j[3] == 'True':
                            rows.remove(row_j)
                            break
                        elif row_i[3] == 'True':
                            rows.remove(row_j)
                            break
                        elif row_j[3] == 'True': 
                            rows.remove(row_i)
                            break
                        else:
                            rows.remove(row_j)
                            break
            sorted_rows = sorted(rows, key=lambda x: (x[-2], x[-1], x[2]))

            print(sorted_rows)


main.write_missing('eda\input_18_06.csv', 'eda\output_18_06.csv')
main.write_sorted('eda\input_18_06.csv', 'eda\output_18_06.csv')
        

'''
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Přeskočení záhlaví

        rows = []
        cloud_number_list= list()
        

        
        for row in reader:
            image_name, _, cloud_number, valid, x_mrak, y_mrak, x_stin, y_stin, distance_px, distance_m, sun_height, cloud_height, img_count, chop_count = row[:14]  # Změna rozsahu na 14 hodnot
            cloud_number_list.append(cloud_number_list)

           

        # Přidání řádků pro každý chop
        for i in range(int(chop_count)):
            chop_row = [
                image_name,
                '',
                i,
                False,
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                img_count,
                chop_count
            ]
            rows.append(chop_row)

        # Přidání řádku pro daný chop
        chop_row = [
            image_name,
            '',
            chop_number,
            valid,
            x_mrak,
            y_mrak,
            x_stin,
            y_stin,
            distance_px,
            distance_m,
            sun_height,
            cloud_height,
            img_count,
            chop_count
        ]
        rows.append(chop_row)

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'chop',
            'error?',
            'cloud number',
            'valid',
            'x mrak',
            'y mrak',
            'x stin',
            'y stin',
            'vzdalenost v px',
            'vzdalenost v m',
            'vyska slunce',
            'vyska mraku',
            'cislo img',
            'cislo chopu'
        ])
        writer.writerows(rows)
'''
