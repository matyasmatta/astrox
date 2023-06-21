import csv

def fix_nulls(s):
    for line in s:
        yield line.replace('\0', '')

with open(r"c:\Users\kiv\Documents\GitHub\astrox2\astrox\eda\david/in - in.csv", "r+", encoding="utf8") as f:
    n = 0
    csv_reader = csv.reader(fix_nulls(f))
    line_count = 0
    for row in csv_reader:
        n +=1
        try:
            original_list = row[2].split(sep="deg")
            degrees = original_list[0]
            meta_1 = original_list[1]
            meta_2 = meta_1.split(sep="'")
            minutes = meta_2[0]
            meta_3 = meta_2[1].split(sep='"')
            seconds = meta_3[0]
            direction = meta_3[1]
            degrees = float(degrees)
            minutes = float(minutes)
            seconds = float(seconds)
            longitude = degrees+(minutes/60)+(seconds/3600)
            if direction == " W":
                longitude = -longitude

            original_list = row[1].split(sep="deg")
            degrees = original_list[0]
            meta_1 = original_list[1]
            meta_2 = meta_1.split(sep="'")
            minutes = meta_2[0]
            meta_3 = meta_2[1].split(sep='"')
            seconds = meta_3[0]
            direction = meta_3[1]
            degrees = float(degrees)
            minutes = float(minutes)
            seconds = float(seconds)
            latitude = degrees+(minutes/60)+(seconds/3600)
            if direction == " S":
                latitude = -latitude

            coordinates = (latitude, longitude)
            print(coordinates)

            with open(r"c:\Users\kiv\Documents\GitHub\astrox2\astrox\eda\david/out.csv", 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                if n == 1:
                    # write the header
                    header = "number" ,"latitude", "longitude"
                    writer.writerow(header)


                # write the data
                data = n, latitude, longitude
                writer.writerow(data)

        except:
            pass
print("hotovo")