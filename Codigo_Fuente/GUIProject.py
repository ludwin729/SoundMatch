# LIBRARIES
import tkinter
from tkinter import ttk
from tkinter.simpledialog import askstring

import customtkinter
from ReadCsvToNewCsv import *
from PIL import ImageTk
from Functions.FunctionsGUI import *
import webbrowser

# PROGRAM--------------------------------------------------------------------
root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
root.title("SoundMatch")
root.configure(bg='#121212')
playlist_tracks = getSongs()
p1 = PhotoImage(file='images/SoundMatch_logo.png')
root.iconphoto(False, p1)
root.state('zoomed')
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_appearance_mode("dark")

# GLOBAL VARIABLES----------------------------------------------------------
list_all_songs = []
lista_search = []


# IMPORTANT-FUNCTIONS-------------------------------------------------------
def getOnlySong(root, song, data_list):
    i = 1
    # songImage=[]
    for record in data_list:
        if song == record[0]:
            my_pic = Image.open("images/SoundMatch.png")
            resized = my_pic.resize((100, 100))
            new_pic = ImageTk.PhotoImage(resized)
            my_label = tkinter.Label(root, image=new_pic)
            my_label.pack(pady=10)

            image = Image.open(f'AlbumsCover/album_number_{str(i)}.png')
            resized = image.resize((40, 40))
            new_photo = ImageTk.PhotoImage(resized)
            photo_label = Label(root, image=new_photo)
            photo_label.pack(pady=10)

            break

        i += 1


def getAllSongsForTView(my_tree, data_list):
    for item in my_tree.get_children():
        my_tree.delete(item)

    global list_all_songs
    count = 0
    i = 1
    for record in data_list:
        image = Image.open(f'AlbumsCover/album_number_{str(i)}.png')
        resized = image.resize((40, 40))
        new_photo = ImageTk.PhotoImage(resized)
        # photo = ImageTk.PhotoImage(image)
        list_all_songs.append(new_photo)

        my_tree.insert(parent='', index='end', image=list_all_songs[count], iid=count, text="",
                       values=(record[0], record[1], record[2], record[3]))
        count += 1
        i += 1


def search_by_name(my_tree, busqueda):
    if busqueda == "":
        messageErrorSongNotFound()
        return

    hasSong = False

    global lista_search
    lista_search = []
    i = 1
    count = 0

    for item in my_tree.get_children():
        my_tree.delete(item)

    busquedaMiniscula = busqueda.lower()

    for record in data_list:
        if busquedaMiniscula in record[0].lower():
            hasSong = True
            image = Image.open(f'AlbumsCover/album_number_{str(i)}.png')
            resized = image.resize((40, 40))
            new_photo = ImageTk.PhotoImage(resized)
            # photo = ImageTk.PhotoImage(image)
            lista_search.append(new_photo)
            my_tree.insert(parent='', index='end', image=lista_search[count], iid=count, text="",
                           values=(record[0], record[1], record[2], record[3]))
            count += 1
        i += 1

    if not hasSong:
        messageErrorNothingSong()


def showWindown(root):
    root.deiconify()


# Hide the window
def hideWindown(root):
    root.withdraw()


def returnPrincipalWindown(root1, root2):
    root2.destroy()
    root1.deiconify()
    root1.state('zoomed')


# TITLE IMAGE--------------------------------------------------------------
my_pic = Image.open("images/SoundMatch.png")
resized = my_pic.resize((100, 100))
new_pic = ImageTk.PhotoImage(resized)
my_label = Label(root, image=new_pic)
my_label.pack(pady=10)

# FRAME SEARCH------------------------------------------------------------
frame_search = Frame(root, bg="#121212")
entry = customtkinter.CTkEntry(master=frame_search,
                               placeholder_text="¡Busca tu canción!",
                               width=300,
                               height=25,
                               border_width=2,
                               corner_radius=10)
entry.grid(row=0, column=0, padx=10)

button_search_image = ImageTk.PhotoImage(Image.open("images/lupa.png").resize((10, 10)))
button_search = customtkinter.CTkButton(master=frame_search, command=lambda: search_by_name(my_tree, entry.get()),
                                        image=button_search_image, text="", width=50, height=20, compound="left",
                                        hover_color="#1DDA63")
button_search.grid(row=0, column=1)

frame_search.pack()
# ------------------------------------------------------------------------
data_list = []
for track in playlist_tracks:
    lista = [track.name, track.artist, track.uri_track, track.album]
    data_list.append(lista)

# Create TreeFrame
tree_frame = Frame(root)
tree_frame.pack(pady=5)
# Create Treeview scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
# Create Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=17)
my_tree.pack()
# Configure Scrollbar
tree_scroll.config(command=my_tree.yview)
my_tree["columns"] = ("Nombre", "Artista", "url", "Album")
# Formate our columns
my_tree.column("#0", width=80)
my_tree.column("Nombre", anchor=W, width=500)
my_tree.column("Artista", anchor=CENTER, width=500)
my_tree.column("url", width=0)
my_tree.column("Album", anchor=W, width=500)
# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Nombre", text="Canción", anchor=W)
my_tree.heading("Artista", text="Artista", anchor=CENTER)
my_tree.heading("url", text="", anchor=W)
my_tree.heading("Album", text="Album", anchor=W)
my_tree["displaycolumns"] = ("Nombre", "Artista", "Album")
# Add some style
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=45,
                fieldbackground="#121212")
style.map("Treeview", background=[("selected", "#4C9957")])
getAllSongsForTView(my_tree, data_list)


def openNewWindow(song):
    playlist_quantity = int(askstring('Cantidad', '¿Cuántas canciones necesitas?'))
    hideWindown(root)
    newWindow = Toplevel(root)
    newWindow.title("Resultado!")
    newWindow.geometry("%dx%d" % (width, height))
    newWindow.iconphoto(False, p1)
    newWindow.state('zoomed')
    newWindow.configure(bg='#121212')

    label_title = Label(newWindow, image=new_pic)
    label_title.pack(pady=20)

    frame_buttons = Frame(newWindow)
    frame_buttons.configure(bg='#121212')

    # getOnlySong(newWindow,song,data_list)
    label_name_song = Label(newWindow, text=song, bg='#121212', fg="#f5f7f5")
    label_name_song.pack()

    button_artist = customtkinter.CTkButton(master=frame_buttons,
                                            command=lambda: ButtonArtist(frame_buttons, song, my_tree_result,
                                                                         data_list),
                                            text="Filtrar por artista", width=100, height=40, hover_color="#1DDA63")
    button_artist.grid(row=0, column=0, padx=5)

    button_seems = customtkinter.CTkButton(master=frame_buttons,
                                           command=lambda: ButtonSeems(frame_buttons, song, playlist_quantity,
                                                                       my_tree_result, data_list),
                                           text="Filtrar por similitud", width=100, height=40, hover_color="#1DDA63")
    button_seems.grid(row=0, column=1, padx=5)

    button_popularity = customtkinter.CTkButton(master=frame_buttons,
                                                command=lambda: ButtonPopularity(frame_buttons, song, playlist_quantity,
                                                                                 my_tree_result, data_list),
                                                text="Filtrar por popularidad", width=100, height=40,
                                                hover_color="#1DDA63")
    button_popularity.grid(row=0, column=2)
    frame_buttons.pack()

    # Create TreeFrame
    tree_frame_result = Frame(newWindow)
    tree_frame_result.pack(pady=5)
    # Create Treeview scrollbar
    tree_scroll_result = Scrollbar(tree_frame_result)
    tree_scroll_result.pack(side=RIGHT, fill=Y)
    # Create Treeview
    my_tree_result = ttk.Treeview(tree_frame_result, yscrollcommand=tree_scroll_result.set, height=16)
    my_tree_result.pack()
    # Configure Scrollbar
    tree_scroll_result.config(command=my_tree_result.yview)
    my_tree_result["columns"] = ("Nombre", "Artista", "url", "Album")
    # Formate our columns
    my_tree_result.column("#0", width=80)
    my_tree_result.column("Nombre", anchor=W, width=500)
    my_tree_result.column("Artista", anchor=CENTER, width=500)
    my_tree_result.column("url", width=0)
    my_tree_result.column("Album", anchor=W, width=500)
    # Create Headings
    my_tree_result.heading("#0", text="", anchor=W)
    my_tree_result.heading("Nombre", text="Canción", anchor=W)
    my_tree_result.heading("Artista", text="Artista", anchor=CENTER)
    my_tree_result.heading("url", text="", anchor=W)
    my_tree_result.heading("Album", text="Album", anchor=W)
    my_tree_result["displaycolumns"] = ("Nombre", "Artista", "Album")
    # Add some style
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=45,
                    fieldbackground="#121212")
    style.map("Treeview", background=[("selected", "#4C9957")])

    # getAllSongsForTView(my_tree_result,data_list)
    new_windows_frames = Frame(newWindow)
    new_windows_frames.configure(bg='#121212')
    button_return = customtkinter.CTkButton(master=new_windows_frames,
                                            command=lambda: returnPrincipalWindown(root, newWindow),
                                            image=playlist_image, text="Retornar Playlist", width=100, height=40,
                                            compound="left",
                                            hover_color="#1DDA63")
    button_return.grid(row=0, column=0, padx=5)
    button_spotify = customtkinter.CTkButton(master=new_windows_frames,
                                             command=lambda: open_song_in_spotify(my_tree_result),
                                             image=spotify_image, text="Escuchar en Spotify", width=100, height=40,
                                             compound="left", hover_color="#1DDA63")
    button_spotify.grid(row=0, column=1)
    new_windows_frames.pack()


def selected_one():
    selected = my_tree.focus()
    temp = my_tree.item(selected, 'values')
    try:
        name_song = temp[0]
        openNewWindow(name_song)
    except:
        messageNothingChoose()


def open_song_in_spotify(my_tree):
    selected = my_tree.focus()
    temp = my_tree.item(selected, 'values')
    try:
        spotify_uri = temp[2][14:]
        webbrowser.open(f'https://open.spotify.com/track/{spotify_uri}')
    except:
        messageNothingChoose()


principalButtonsFrame = Frame(root, bg="#121212")
principalButtonsFrame.pack(pady=5)

choose_image = ImageTk.PhotoImage(Image.open("images/music_choose.png").resize((20, 20)))
button_choose = customtkinter.CTkButton(master=principalButtonsFrame, command=lambda: selected_one(),
                                        image=choose_image, text="¡Elige la canción!", width=100, height=40,
                                        compound="left", hover_color="#1DDA63")
button_choose.grid(row=0, column=0)

spotify_image = ImageTk.PhotoImage(Image.open("images/spotify_logo.png").resize((20, 20)))
button_listen = customtkinter.CTkButton(master=principalButtonsFrame, command=lambda: open_song_in_spotify(my_tree),
                                        image=spotify_image, text="Escuchar en Spotify", width=100, height=40,
                                        compound="left", hover_color="#1DDA63")
button_listen.grid(row=0, column=1, padx=10)

playlist_image = ImageTk.PhotoImage(Image.open("images/playlist.png").resize((20, 20)))
button_restart = customtkinter.CTkButton(master=principalButtonsFrame,
                                         command=lambda: getAllSongsForTView(my_tree, data_list), image=playlist_image,
                                         text="Reiniciar Playlist", width=100, height=40, compound="left",
                                         hover_color="#1DDA63")
button_restart.grid(row=0, column=2)

root.mainloop()
