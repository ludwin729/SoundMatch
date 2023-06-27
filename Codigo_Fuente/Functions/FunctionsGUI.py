import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import Toplevel, Label

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Codigo_Fuente.ReadCsvToNewCsv import *
from Codigo_Fuente.Functions.Function import *
from PIL import Image, ImageTk
from tkinter import messagebox


def showSongs(root, img_boton, printNameSong):
    botons = []
    rowIterador = 2

    for i in range(len(playlist_tracks)):
        songName = playlist_tracks[i].name
        myLabel = Label(root, text=songName)

        myLabel.grid(row=rowIterador, column=0)
        botons.append(Button(root, image=img_boton, padx=0, pady=0, text=songName,
                             command=lambda c=i: printNameSong(botons[c].cget("text"))))
        botons[i].grid(row=rowIterador, column=1)  # this packs the buttons

        rowIterador += 1



def extracSong(song, playlist_tracks):
    for track in playlist_tracks:
        if song == track.name:
            return track


def messageErrorSongNotFound():
    messagebox.showerror("SoundMatch", "La cancion ingresada no es valida")

def messageErrorNothingSong():
    messagebox.showwarning("SoundMatch", "No se ha encontrado ninguna cancion que contenga los caracteres")

def messageNothingChoose():
    messagebox.showerror("SoundMatch", "No has selccionado ninguna cancion")

def pressButonCheck(song):
    if (checkSong(song, playlist_tracks)):
        return True
    else:
        messageErrorSongNotFound()
        return False




def showListOfSongs(root,listOfSongs):
    scrollbar = Scrollbar(root, orient="vertical")

    SelectuserLabel = Label(root, text="Copia el nombre de tu canción").grid(row=0, column=0)
    test = Listbox(root, width=40, height=35, font=("Helvetica", 10))
    for song in listOfSongs:
        test.insert(END,song.name)
    test.grid(row=1, column=0)
    scrollbar.config(command=test.yview)
    scrollbar.grid(row=0, column=2, sticky='ns')



def showListOfSelectedSongs(root, listOfSongs):
    scrollbar = Scrollbar(root, orient="vertical")
    test = Listbox(root, width=20, height=5, font=("Helvetica", 10))

    for x in listOfSongs:
        test.insert(END, x)

    test.grid(row=6, column=0)
    scrollbar.config(command=test.yview)
    scrollbar.grid(row=7, column=1, sticky='ns')


lista_images_artist=[]
def tableArtist(my_tree,song,data_list):

    global lista_images_artist
    lista_images_artist=[]
    i=1
    count=0
    for item in my_tree.get_children():
        my_tree.delete(item)
    for record in data_list:
        if song.artist==record[1]:
            image = Image.open(f'AlbumsCover/album_number_{str(i)}.png')
            resized = image.resize((40, 40))
            new_photo = ImageTk.PhotoImage(resized)
            # photo = ImageTk.PhotoImage(image)
            lista_images_artist.append(new_photo)
            my_tree.insert(parent='', index='end', image=lista_images_artist[count], iid=count, text="",
                           values=(record[0], record[1], record[2], record[3]))
            count += 1
        i += 1

def ButtonArtist(root, songName, my_tree, data_list):
    grafo = nx.Graph()
    song = extracSong(songName, playlist_tracks)
    tableArtist(my_tree, song, data_list)
    generateNodesCaseByArtist(grafo, song, playlist_tracks)
    listaId = []
    diccionario_objetos = {}
    for i in range(len(playlist_tracks)):
        diccionario_objetos[i] = playlist_tracks[i]
        listaId.append(playlist_tracks[i].artist)
    grafo.add_node(song.artist)
    for i in range(len(listaId)):
        valor = diccionario_objetos[i].artist
        if (valor == listaId[i] and valor == song.artist):
            grafo.add_edge(diccionario_objetos[i].name, listaId[i])
    songs_of_group = list(grafo.adj[song.artist])

    # Crear una nueva ventana para mostrar el grafo
    ventana_grafo = Toplevel(root)
    ventana_grafo.title("Grafo de canciones por filtro de artista")

    # Dibujar el grafo en un lienzo de Tkinter
    fig, ax = plt.subplots()
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=True, node_color='lightblue', edge_color='gray')

    # Convertir la figura de Matplotlib en un lienzo de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=ventana_grafo)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Mostrar la ventana con el grafo
    ventana_grafo.mainloop()

lista_images_seems = []
def tableSeems(my_tree, data_list,songs_of_seems):
    global lista_images_seems
    lista_images_seems = []

    count = 0

    for item in my_tree.get_children():
        my_tree.delete(item)

    for track in songs_of_seems:
        i = 1

        for record in data_list:
            if track == record[0]:
                image = Image.open(f'AlbumsCover/album_number_{str(i)}.png')
                resized = image.resize((40, 40))
                new_photo = ImageTk.PhotoImage(resized)
                # photo = ImageTk.PhotoImage(image)
                lista_images_seems.append(new_photo)
                my_tree.insert(parent='', index='end', image=lista_images_seems[count], iid=count, text="",
                               values=(record[0], record[1], record[2], record[3]))
                count += 1
                break

            i += 1

def ButtonSeems(root, songName, numberOfPlaylist, my_tree, data_list):
    grafo = nx.Graph()  # Creamos el grafo
    song = extracSong(songName, playlist_tracks)  # Extraemos la canción
    grafo.add_node(song.name)  # Añadimos el nodo de la canción
    generateNodesCaseBySeems(grafo, song, playlist_tracks, numberOfPlaylist)

    # Crear una nueva ventana para mostrar el grafo
    ventana_grafo = Toplevel(root)
    ventana_grafo.title("Grafo de canciones por filtro de similitud")

    # Dibujar el grafo en un lienzo de Tkinter
    fig, ax = plt.subplots()
    elarge = [(u, v) for (u, v, d) in grafo.edges(data=True) if d["weight"] > 5]
    esmall = [(u, v) for (u, v, d) in grafo.edges(data=True) if d["weight"] <= 5]
    pos = nx.spring_layout(grafo, seed=4)
    nx.draw_networkx_nodes(grafo, pos, node_size=700)
    nx.draw_networkx_edges(grafo, pos, edgelist=elarge, width=3)
    nx.draw_networkx_edges(
        grafo, pos, edgelist=esmall, width=3, alpha=0.5, edge_color="b", style="dashed"
    )
    nx.draw_networkx_labels(grafo, pos, font_size=8, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(grafo, "weight")
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels)
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    songs_of_seems = list(grafo.adj[song.name])

    tableSeems(my_tree,data_list,songs_of_seems)

    # Convertir la figura de Matplotlib en un lienzo de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=ventana_grafo)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Mostrar la ventana con el grafo
    ventana_grafo.mainloop()

lista_images_popularity=[]
def tablePopularity(my_tree, data_list,songs_of_popularity):
    global lista_images_popularity
    lista_images_popularity=[]

    count = 0

    for item in my_tree.get_children():
        my_tree.delete(item)

    for track in songs_of_popularity:
        i = 1

        for record in data_list:
            if track == record[0]:
                image = Image.open(f'AlbumsCover/album_number_{str(i)}.png')
                resized = image.resize((40, 40))
                new_photo = ImageTk.PhotoImage(resized)
                # photo = ImageTk.PhotoImage(image)
                lista_images_popularity.append(new_photo)
                my_tree.insert(parent='', index='end', image=lista_images_popularity[count], iid=count, text="",
                               values=(record[0], record[1], record[2], record[3]))
                count += 1
                break

            i += 1

def ButtonPopularity(root, songName, numberOfPlaylist, my_tree, data_list):
    grafo = nx.Graph()  # Creamos el grafo
    song = extracSong(songName, playlist_tracks)  # Extraemos la canción
    generateNodesCaseByPopularity(grafo, song, playlist_tracks, numberOfPlaylist)
    conectionByPopularity(playlist_tracks, grafo, song, numberOfPlaylist)

    songs_of_group = list(grafo.adj[song.name])
    tableSeems(my_tree, data_list, songs_of_group)
    # Crear una nueva ventana para mostrar el grafo
    ventana_grafo = Toplevel(root)
    ventana_grafo.title("Grafo de canciones por filtro de popularidad")

    # Dibujar el grafo en un lienzo de Tkinter
    fig, ax = plt.subplots()
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos=pos, with_labels=True)
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()

    # Convertir la figura de Matplotlib en un lienzo de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=ventana_grafo)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Mostrar la ventana con el grafo
    ventana_grafo.mainloop()


