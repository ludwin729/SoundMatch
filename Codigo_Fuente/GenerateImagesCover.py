import requests
import urllib
import csv

def generateAlbumImages():
    i=0
    with open("../DataSet/Dataset.csv", encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                i+=1
                urllib.request.urlretrieve(row[6], f'AlbumsCover/album_number_{str(i)}.png')
                line_count += 1

generateAlbumImages()
