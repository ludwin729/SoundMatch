import csv
from Codigo_Fuente.Classes.classes import Song
playlist_tracks=[]

def getSongs():
    with open("../DataSet/Dataset.csv", encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                #print(row[1],row[3],row[15],row[29])
                line_count += 1
            else:
                #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                #name, artist,popularity,tempo,genres
                s=Song(row[0],row[1],row[2],row[3],row[4],list(row[5].split(",")),row[6],row[7])
                playlist_tracks.append(s)
                line_count += 1
        print(f'Processed {line_count} lines.')

    return playlist_tracks
