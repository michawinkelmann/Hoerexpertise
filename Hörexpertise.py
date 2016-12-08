
# coding: utf-8

# # Sound Zuordnung

# Imports:

# In[1]:

import pyaudio
import wave
import sys
from os import path
import numpy as np
import scipy as sc
import tkinter as tk
import matplotlib.pyplot as plt
from scipy import misc
import matplotlib.gridspec as gridspec
from tkinter import *
from tkinter.filedialog import askopenfilename
import warnings
#handle warnings as errors (for try - except)
warnings.filterwarnings("error")


# Fenster erstellen fuer GUI

# In[2]:

fenster = tk.Tk()
fenster.title("Hörexpertise A")
fenster.geometry("539x438");


# Aufgabenbeschreibung

# In[3]:

#Zeilenumbruch mit \n im Text anpassen an window
ueberschrift = tk.Label(fenster, text='Welches Instrument könnte es sein?',  font = "Verdana 10 bold")
beschreibung = tk.Label(fenster,height=5, text = 'Das hier folgende Experiment soll untersuchen, wie gut Sie einem Klang das passende \n Instrument zuordnen können. Dazu wurden die Klänge einzelner Instrumente bearbeitet, \n sodass die volle Klangfarbe der Instrumente erst nach und nach zu hören ist. \n Je vier hintereinander folgende Klänge gehören zu einem Instrument. \n Wählen Sie das richtige Instrument aus.')


# In[ ]:




# Musikalisch/Unmusikalisch Checkbox

# In[4]:

frage = tk.Label(fenster, text = 'Würden Sie sich selbst als musikalisch bezeichnen?')
var1 = IntVar()
check1 = tk.Checkbutton(fenster, text="Ja", variable=var1, onvalue = 1, offvalue = 0)
#aufrufen mit var1.get()


# Ergebnisfeld definieren als globale Variable, damit bei erneuter Ausführung das alte Ergebnis gelöscht werden kann

# In[5]:

Ergebnis = tk.Label(fenster, text = 'Ergebnis_Platzhalter')


# In[ ]:




# Fotos für Knöpfe

# In[6]:

foto0 = tk.PhotoImage(file=path.relpath("dateien/Bilder/tonabspielen.gif"))
foto00 = tk.PhotoImage(file=path.relpath("dateien/Bilder/tonwiederholen.gif"))
foto1 = tk.PhotoImage(file=path.relpath("dateien/Bilder/Bratsche.gif"))
foto2 = tk.PhotoImage(file=path.relpath("dateien/Bilder/Saxophon.gif"))
foto3 = tk.PhotoImage(file=path.relpath("dateien/Bilder/Klavier.gif"))
foto4 = tk.PhotoImage(file=path.relpath("dateien/Bilder/Harfe.gif"))
foto5 = tk.PhotoImage(file=path.relpath("dateien/Bilder/Gitarre.gif"))
foto6 = tk.PhotoImage(file=path.relpath("dateien/Bilder/Geige.gif"))
foto7 = tk.PhotoImage(file=path.relpath("dateien/Bilder/Orgel.gif"))
foto8 = tk.PhotoImage(file=path.relpath("dateien/Bilder/Horn.gif"))
foto9 = tk.PhotoImage(file=path.relpath("dateien/Bilder/Oboe.gif"))
foto10 = tk.PhotoImage(file=path.relpath("dateien/Bilder/leer.gif"))


# In[7]:

fotoliste = ['Bratsche.png','Saxophon.png','Klavier.png','Harfe.png','Gitarre.png','Geige.png','Orgel.png','Horn.png','Oboe.png','leer.png']


# Toene

# In[8]:

Tonliste = ['Bratsche_lowpass_400Hz_12db.wav','Bratsche_lowpass_600Hz_12db.wav','Bratsche_lowpass_800Hz_12db.wav','Bratsche_original.wav',
           'Geige_lowpass 400Hz_12db.wav','Geige_lowpass 600Hz_12db.wav','Geige_lowpass 800Hz_12db.wav','Geige_original.wav',
           'Gitarre_lowpass 400Hz_12 db.wav','Gitarre_lowpass 600Hz_12 db.wav','Gitarre_lowpass 800Hz_12 db.wav','Gitarre_original.wav',
           'Horn_lowpass 400Hz_12db.wav','Horn_lowpass 600Hz_12db.wav','Horn_lowpass 800Hz_12db.wav','Horn_original.wav',
           'Oboe_lowpass 400Hz_12db.wav','Oboe_lowpass 600Hz_12db.wav','Oboe_lowpass 800Hz_12db.wav','Oboe_original.wav',
           'Saxophon_lowpass 400Hz_12db.wav','Saxophon_lowpass 600Hz_12db.wav','Saxophon_lowpass 800Hz_12db.wav','Saxophon_original.wav']


# In[9]:

TonZuButton = [['Bratsche_lowpass_400Hz_12db.wav','Bratsche_lowpass_600Hz_12db.wav','Bratsche_lowpass_800Hz_12db.wav','Bratsche_original.wav'], ['Saxophon_lowpass 400Hz_12db.wav','Saxophon_lowpass 600Hz_12db.wav','Saxophon_lowpass 800Hz_12db.wav','Saxophon_original.wav'], [] , [], ['Gitarre_lowpass 400Hz_12 db.wav','Gitarre_lowpass 600Hz_12 db.wav','Gitarre_lowpass 800Hz_12 db.wav','Gitarre_original.wav'], ['Geige_lowpass 400Hz_12db.wav','Geige_lowpass 600Hz_12db.wav','Geige_lowpass 800Hz_12db.wav','Geige_original.wav'], [], ['Horn_lowpass 400Hz_12db.wav','Horn_lowpass 600Hz_12db.wav','Horn_lowpass 800Hz_12db.wav','Horn_original.wav'], ['Oboe_lowpass 400Hz_12db.wav','Oboe_lowpass 600Hz_12db.wav','Oboe_lowpass 800Hz_12db.wav','Oboe_original.wav'] ,[]] 


# Zufällige Reihenfolge der 6 Tonblöcke a' 4 Töne. Gleiche Instrumente bleiben dabei zusammen.

# In[10]:

randList = []
TonlisteRand = []
a = []
def random():
    global Tonliste, randList, TonlisteRand, a
    TonlisteRand = []
    a = [1,6,5,8,9,2]
    np.random.shuffle(a)
    randList =[a[0],a[0],a[0],a[0],a[1],a[1],a[1],a[1],a[2],a[2],a[2],a[2],a[3],a[3],a[3],a[3],a[4],a[4],a[4],a[4],a[5],a[5],a[5],a[5],1]
    for i in range(6):
        for j in range(4):
            TonlisteRand.append(TonZuButton[a[i]-1][j])
            
random()    


# In[ ]:




# # Funktionen

# Counter definieren und Listen einlesen/erstellen

# In[11]:

counter = 0
try:
    ErgebnisListe = np.loadtxt(path.relpath("Ergebnisse/ErgebnisListe.txt"), dtype=int, comments='#', delimiter=',', unpack=False, ndmin=0)
except FileNotFoundError:
    ErgebnisListe = [randList]
except UserWarning:
    ErgebnisListe = [randList]
AktuelleListe = []


# In[ ]:




# Ton abspielen

# In[12]:

def abspielen(wav_filename):
    chunk_size = 1024
    wf = wave.open(path.relpath("dateien/Toene/" + wav_filename), 'rb')
    
    # PyAudio starten
    p = pyaudio.PyAudio()

    # Stream öffnen
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),output=True
    )

    data = wf.readframes(chunk_size)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk_size)
    # Stream stoppen
    stream.stop_stream()
    stream.close()
    # PyAudio schließen
    p.terminate()


# In[13]:

def click_next():
    global counter, ErgebnisListe, AktuelleListe, Ergebnis, var1
    counter = counter + 1 
    if counter == 25:
        AktuelleListe.append(var1.get())
        ErgebnisListe = np.append(ErgebnisListe,[randList],axis=0)
        ErgebnisListe = np.append(ErgebnisListe,[AktuelleListe],axis=0)
        np.savetxt(path.relpath("Ergebnisse/ErgebnisListe.txt"), ErgebnisListe, fmt='%d', delimiter=',', header='Ergebnisse der Testpersonen als Liste. Zwei Zeilen pro Testperson, dabei ein Eintrag pro Ton. Letzter Eintrag = 1: Musikalisch, = 0: unmusikalisch. Kodierung wie folgt: \n 1: Bratscher \n 2: Saxophon \n 3: Klavier \n 4: Harfe \n 5: Gitarre \n 6: Geige \n 7: Orgel \n 8: Horn \n 9: Posaune \n 10: Oboe \n Erste Zeile: Richtige Zuordnung (Muster), Zweite Zeile: Antworten \n Dritte Zeile: Richtige Zuordnung (Muster), Vierte Zeile: Antworten \n Usw.')
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Fertig, Vielen Dank!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
        ergebnisfenster()
    elif counter > 25:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Fertig, Vielen Dank!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    elif counter < 25:
        if len(AktuelleListe)+1 < counter:
            Ergebnis.destroy()
            Ergebnis = tk.Label(fenster, text = 'Noch kein Bild zum aktuellen Ton zugeordnet!',fg = "red", font = "Verdana 10 bold")
            Ergebnis.grid(row=7, columnspan=4)
            counter = counter - 1
        else:
            Ergebnis.destroy()
            Ergebnis = tk.Label(fenster, text = 'Ergebnis_Platzhalter')
            abspielen(TonlisteRand[counter-1])


# In[14]:

def click_repeat():
    global counter, Ergebnis, AktuelleListe, Ergebnis
    if counter == 0:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Es wurde noch kein Ton abgespielt!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    elif len(AktuelleListe) == counter:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Der Ton wurde bereits zugeordnet!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    else:
        if counter > 24:
            Ergebnis.destroy()
            Ergebnis = tk.Label(fenster, text = 'Fertig, Vielen Dank!',fg = "red", font = "Verdana 10 bold")
            Ergebnis.grid(row=7, columnspan=4)
        else:
            Ergebnis.destroy()
            Ergebnis = tk.Label(fenster, text = 'Ergebnis_Platzhalter')
            abspielen(TonlisteRand[counter-1])


# In[15]:

def reset():
    global AktuelleListe, Ergebnis, counter, ErgebnisListe, randList, Tonliste, TonlisteRand
    Ergebnis.destroy()
    Ergebnis = tk.Label(fenster, text = 'Ergebnis_Platzhalter')
    counter = 0
    AktuelleListe = []
    random()
    try:
        ErgebnisListe = np.loadtxt(path.relpath("Ergebnisse/ErgebnisListe.txt"), dtype=int, comments='#', delimiter=',', unpack=False, ndmin=0)
    except FileNotFoundError:
        ErgebnisListe = [randList]
    except UserWarning:
        ErgebnisListe = [randList]


# Buttons drücken

# In[16]:

def click1():
    global counter, AktuelleListe, Ergebnis
    if counter == 0:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Es wurde noch kein Ton abgespielt!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    elif len(AktuelleListe) == counter:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Der Ton wurde bereits zugeordnet!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    else:
        AktuelleListe.append(1)


# In[17]:

def click2():
    global counter, AktuelleListe, Ergebnis
    if counter == 0:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Es wurde noch kein Ton abgespielt!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    elif len(AktuelleListe) == counter:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Der Ton wurde bereits zugeordnet!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    else:
        AktuelleListe.append(2)


# In[18]:

def click3():
    global counter, AktuelleListe, Ergebnis
    if counter == 0:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Es wurde noch kein Ton abgespielt!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    elif len(AktuelleListe) == counter:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Der Ton wurde bereits zugeordnet!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    else:
        AktuelleListe.append(3)


# In[19]:

def click4():
    global counter, AktuelleListe, Ergebnis
    if counter == 0:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Es wurde noch kein Ton abgespielt!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    elif len(AktuelleListe) == counter:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Der Ton wurde bereits zugeordnet!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    else:
        AktuelleListe.append(4)


# In[20]:

def click5():
    global counter, AktuelleListe, Ergebnis
    if counter == 0:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Es wurde noch kein Ton abgespielt!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    elif len(AktuelleListe) == counter:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Der Ton wurde bereits zugeordnet!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    else:
        AktuelleListe.append(5)


# In[21]:

def click6():
    global counter, AktuelleListe, Ergebnis
    if counter == 0:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Es wurde noch kein Ton abgespielt!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    elif len(AktuelleListe) == counter:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Der Ton wurde bereits zugeordnet!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    else:
        AktuelleListe.append(6)


# In[22]:

def click7():
    global counter, AktuelleListe, Ergebnis
    if counter == 0:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Es wurde noch kein Ton abgespielt!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    elif len(AktuelleListe) == counter:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Der Ton wurde bereits zugeordnet!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    else:
        AktuelleListe.append(7)


# In[23]:

def click8():
    global counter, AktuelleListe, Ergebnis
    if counter == 0:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Es wurde noch kein Ton abgespielt!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    elif len(AktuelleListe) == counter:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Der Ton wurde bereits zugeordnet!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    else:
        AktuelleListe.append(8)


# In[24]:

def click9():
    global counter, AktuelleListe, Ergebnis
    if counter == 0:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Es wurde noch kein Ton abgespielt!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    elif len(AktuelleListe) == counter:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Der Ton wurde bereits zugeordnet!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    else:
        AktuelleListe.append(9)


# In[25]:

def click10():
    global counter, AktuelleListe, Ergebnis
    if counter == 0:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Es wurde noch kein Ton abgespielt!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    elif len(AktuelleListe) == counter:
        Ergebnis.destroy()
        Ergebnis = tk.Label(fenster, text = 'Der Ton wurde bereits zugeordnet!',fg = "red", font = "Verdana 10 bold")
        Ergebnis.grid(row=7, columnspan=4)
    else:
        AktuelleListe.append(0)


# Ergebnisfenster für eine Rückmeldung

# In[77]:

def ergebnisfenster():
    Instrument1 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[a[0]-1]))
    Instrument2 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[a[1]-1]))
    Instrument3 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[a[2]-1]))
    Instrument4 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[a[3]-1]))
    Instrument5 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[a[4]-1]))
    Instrument6 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[a[5]-1]))
    
    
    Instrument11 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[0]-1]))
    Instrument12 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[1]-1]))
    Instrument13 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[2]-1]))
    Instrument14 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[3]-1]))
    
    Instrument21 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[4]-1]))
    Instrument22 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[5]-1]))
    Instrument23 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[6]-1]))
    Instrument24 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[7]-1]))
    
    Instrument31 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[8]-1]))
    Instrument32 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[9]-1]))
    Instrument33 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[10]-1]))
    Instrument34 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[11]-1]))
    
    Instrument41 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[12]-1]))
    Instrument42 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[13]-1]))
    Instrument43 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[14]-1]))
    Instrument44 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[15]-1]))
    
    Instrument51 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[16]-1]))
    Instrument52 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[17]-1]))
    Instrument53 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[18]-1]))
    Instrument54 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[19]-1]))
    
    Instrument61 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[20]-1]))
    Instrument62 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[21]-1]))
    Instrument63 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[22]-1]))
    Instrument64 = misc.imread(path.relpath("dateien/Bilder/" + fotoliste[AktuelleListe[23]-1]))
    
    
    fig = plt.figure(0)
    fig.canvas.set_window_title('Ergebnis')
    
    #Richtige Instrumente
    ax1 = plt.subplot2grid((6,12), (0,0), colspan=2, rowspan=2)
    ax2 = plt.subplot2grid((6,12), (2,0), colspan=2, rowspan=2)
    ax3 = plt.subplot2grid((6,12), (4,0), colspan=2, rowspan=2)
    ax4 = plt.subplot2grid((6,12), (0,7), colspan=2, rowspan=2)
    ax5 = plt.subplot2grid((6,12), (2,7), colspan=2, rowspan=2)
    ax6 = plt.subplot2grid((6,12), (4,7), colspan=2, rowspan=2)
    
    #Gewählte Instrumente
    ax11 = plt.subplot2grid((6,12), (0,3))
    ax12 = plt.subplot2grid((6,12), (0,4))
    ax13 = plt.subplot2grid((6,12), (1,3))
    ax14 = plt.subplot2grid((6,12), (1,4))
    
    ax21 = plt.subplot2grid((6,12), (2,3))
    ax22 = plt.subplot2grid((6,12), (2,4))
    ax23 = plt.subplot2grid((6,12), (3,3))
    ax24 = plt.subplot2grid((6,12), (3,4))
    
    ax31 = plt.subplot2grid((6,12), (4,3))
    ax32 = plt.subplot2grid((6,12), (4,4))
    ax33 = plt.subplot2grid((6,12), (5,3))
    ax34 = plt.subplot2grid((6,12), (5,4))
    
    ax41 = plt.subplot2grid((6,12), (0,10))
    ax42 = plt.subplot2grid((6,12), (0,11))
    ax43 = plt.subplot2grid((6,12), (1,10))
    ax44 = plt.subplot2grid((6,12), (1,11))
    
    ax51 = plt.subplot2grid((6,12), (2,10))
    ax52 = plt.subplot2grid((6,12), (2,11))
    ax53 = plt.subplot2grid((6,12), (3,10))
    ax54 = plt.subplot2grid((6,12), (3,11))
    
    ax61 = plt.subplot2grid((6,12), (4,10))
    ax62 = plt.subplot2grid((6,12), (4,11))
    ax63 = plt.subplot2grid((6,12), (5,10))
    ax64 = plt.subplot2grid((6,12), (5,11))
    
    
    
    
    
    #links
    ax1.imshow(Instrument1)
    ax1.set_title('Instrument:')
    ax2.imshow(Instrument2)
    ax3.imshow(Instrument3)
    
    ax11.imshow(Instrument11)
    ax11.set_title('Auswahl:')
    ax12.imshow(Instrument12)
    ax13.imshow(Instrument13)
    ax14.imshow(Instrument14)
    
    ax21.imshow(Instrument21)
    ax22.imshow(Instrument22)
    ax23.imshow(Instrument23)
    ax24.imshow(Instrument24)
    
    ax31.imshow(Instrument31)
    ax32.imshow(Instrument32)
    ax33.imshow(Instrument33)
    ax34.imshow(Instrument34)
    
    
    #rechts
    ax4.imshow(Instrument4)
    ax4.set_title('Instrument:')
    ax5.imshow(Instrument5)
    ax6.imshow(Instrument6)
    
    ax41.imshow(Instrument41)
    ax41.set_title('Auswahl:')
    ax42.imshow(Instrument42)
    ax43.imshow(Instrument43)
    ax44.imshow(Instrument44)
    
    ax51.imshow(Instrument51)
    ax52.imshow(Instrument52)
    ax53.imshow(Instrument53)
    ax54.imshow(Instrument54)
    
    ax61.imshow(Instrument61)
    ax62.imshow(Instrument62)
    ax63.imshow(Instrument63)
    ax64.imshow(Instrument64)
    
        
    ax1.axis('off')
    ax11.axis('off')
    ax12.axis('off')
    ax13.axis('off')
    ax14.axis('off')
    ax2.axis('off')
    ax21.axis('off')
    ax22.axis('off')
    ax23.axis('off')
    ax24.axis('off')
    ax3.axis('off')
    ax31.axis('off')
    ax32.axis('off')
    ax33.axis('off')
    ax34.axis('off')
    ax4.axis('off')
    ax41.axis('off')
    ax42.axis('off')
    ax43.axis('off')
    ax44.axis('off')
    ax5.axis('off')
    ax51.axis('off')
    ax52.axis('off')
    ax53.axis('off')
    ax54.axis('off')
    ax6.axis('off')
    ax61.axis('off')
    ax62.axis('off')
    ax63.axis('off')
    ax64.axis('off')
    
    
    
    plt.subplots_adjust(wspace=None, hspace=None)
    
    plt.show()


# In[ ]:




# In[ ]:




# In[27]:

button0 = tk.Button(fenster, width=40, height=40, image=foto0, bg='white', command=click_next)
button00 = tk.Button(fenster, width=40, height=37, image=foto00, bg='white', command=click_repeat)


# In[28]:

button1 = tk.Button(fenster,text = 'Bratsche', font = "Verdana 15 bold",fg="red", width=100, height=100, image=foto1, bg='white', command=click1, compound="center")
button2 = tk.Button(fenster,text = 'Saxophon',font = "Verdana 15 bold",fg="red", width=100, height=100, image=foto2, bg='white', command=click2, compound="center")
button3 = tk.Button(fenster,text = 'Klavier',font = "Verdana 15 bold",fg="red", width=100, height=100, image=foto3, bg='white', command=click3, compound="center")
button4 = tk.Button(fenster,text = 'Harfe',font = "Verdana 15 bold",fg="red", width=100, height=100, image=foto4, bg='white', command=click4, compound="center")
button5 = tk.Button(fenster,text = 'Gitarre',font = "Verdana 15 bold",fg="red", width=100, height=100, image=foto5, bg='white', command=click5, compound="center")
button6 = tk.Button(fenster,text = 'Geige',font = "Verdana 15 bold",fg="red", width=100, height=100, image=foto6, bg='white', command=click6, compound="center")
button7 = tk.Button(fenster,text = 'Orgel',font = "Verdana 15 bold",fg="red", width=100, height=100, image=foto7, bg='white', command=click7, compound="center")
button8 = tk.Button(fenster,text = 'Horn',font = "Verdana 15 bold",fg="red", width=100, height=100, image=foto8, bg='white', command=click8, compound="center")
button9 = tk.Button(fenster,text = 'Oboe',font = "Verdana 15 bold",fg="red", width=100, height=100, image=foto9, bg='white', command=click9, compound="center")
button10 = tk.Button(fenster,text = 'Weiß ich \n nicht' ,font = "Verdana 15 bold",fg="black", width=100, height=100, image=foto10, bg='white', command=click10, compound="center")


# In[29]:

button11 = tk.Button(fenster, text="RESET", command=reset)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[30]:

ueberschrift.grid(row=0,columnspan=5)
beschreibung.grid(row=1,column=0, columnspan=5)
frage.grid(row=2, columnspan=5)
check1.grid(row=3, columnspan=5)


# In[31]:

next_ton = tk.Label(fenster,height=2, text = 'Nächsten Ton \n abspielen:')
repeat_ton = tk.Label(fenster,height=2, text = 'Ton wiederholen:')

next_ton.grid(row=4,column=3)
repeat_ton.grid(row=4,column=0)
button0.grid(row=4,column=4)
button00.grid(row=4,column=1)


# In[32]:

button1.grid(row=5,column=0)
button2.grid(row=5,column=1)
button3.grid(row=5,column=2)
button4.grid(row=5,column=3)
button5.grid(row=5,column=4)
button6.grid(row=6,column=0)
button7.grid(row=6,column=1)
button8.grid(row=6,column=2)
button9.grid(row=6,column=3)
button10.grid(row=6,column=4)


# In[33]:

button11.grid(row=7,column=4)


# In[ ]:




# In[ ]:




# In[ ]:




# In[34]:

tk.mainloop()


# In[ ]:




# In[35]:




# In[36]:




# In[ ]:




# In[ ]:



