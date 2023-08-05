from youtubesearchpython import VideosSearch, Video
from pytube import YouTube
import webbrowser
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior
from kivy.utils import platform
import tkinter as tk
from tkinter import filedialog
from threading import Thread
import ffmpeg


from kivy.core.window import Window
Window.size = (800, 500)

selectedSongsNames = []
selectedSongsLinks = []
ubication = "."
currentsong1 = []
currentsong2 = []
currentsong3 = []
currentsong4 = []
currentsong5 = []


class MainScreen(Screen):
    def refreshList(self, txt):
        txt.text = ""
        for idx, song in enumerate(selectedSongsNames):
            txt.text = txt.text + str(idx) + ". " + song + "\n"
    def explore(self):
        global ubication
        tki = tk.Tk()
        tki.withdraw()
        file_path = filedialog.askdirectory()
        self.ids.ubication.text = file_path
        ubication = str(file_path)
        print(ubication)
    def startDownload(self):
        download = Thread(target=self.download)
        download.start()
    def download(self):
        global selectedSongsLinks
        global selectedSongsNames
        global ubication
        if ubication == "":
            ubication = "."
        self.ids.loading.text = 'Descargando...'
        for idx, link in enumerate(selectedSongsLinks):
            try:
                YouTube(link).streams.filter(only_audio=True, file_extension='webm').order_by('abr').desc().first().download(filename=normalize(selectedSongsNames[idx]), output_path=ubication)
                default_filename = ubication + "/" + normalize(selectedSongsNames[idx]) + ".webm"
                new_filename = ubication + "/" + normalize(selectedSongsNames[idx]) + ".mp3"
                input = ffmpeg.input(default_filename)
                audio = input.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)
                ffmpeg.output(audio, new_filename).run()
                self.ids.loading.text = 'Downloding...(' + str(idx + 1) + '/' + str(len(selectedSongsNames)) + ")"
            except Exception as e:
                print(e)
        selectedSongsNames = []
        selectedSongsLinks = []
        self.ids.loading.text = 'Descarga completa'
        self.refreshList(self.ids.songlist)

def normalize(txt):
    characters = '\/:*?"<>|,.'
    for x in range(len(characters)):
        txt = txt.replace(characters[x],"")
    return txt

class SearchScreen(Screen):
    def startSearch(self):
        search = Thread(target=self.doSearch)
        search.start()
    def doSearch(self, txtInput, txt1, txt2, txt3, txt4, txt5):
        global currentsong1
        global currentsong2
        global currentsong3
        global currentsong4
        global currentsong5
        try:
            videosSearch = VideosSearch(txtInput.text, limit = 5)
            
            txt1.text = videosSearch.result()['result'][0]['title']
            txt2.text = videosSearch.result()['result'][1]['title']
            txt3.text = videosSearch.result()['result'][2]['title']
            txt4.text = videosSearch.result()['result'][3]['title']
            txt5.text = videosSearch.result()['result'][4]['title']

            currentsong1 = [videosSearch.result()['result'][0]['title'], videosSearch.result()['result'][0]['link']]
            currentsong2 = [videosSearch.result()['result'][1]['title'], videosSearch.result()['result'][1]['link']]
            currentsong3 = [videosSearch.result()['result'][2]['title'], videosSearch.result()['result'][2]['link']]
            currentsong4 = [videosSearch.result()['result'][3]['title'], videosSearch.result()['result'][3]['link']]
            currentsong5 = [videosSearch.result()['result'][4]['title'], videosSearch.result()['result'][4]['link']]

            if len(txt1.text) > 80:
                txt1.text = txt1.text[0:80] + "..."
            if len(txt2.text) > 80:
                txt2.text = txt2.text[0:80] + "..."
            if len(txt3.text) > 80:
                txt3.text = txt3.text[0:80] + "..."
            if len(txt4.text) > 80:
                txt4.text = txt4.text[0:80] + "..."
            if len(txt5.text) > 80:
                txt5.text = txt5.text[0:80] + "..."

            self.ids.plus1.source = 'icons/plus-icon.png'
            self.ids.play1.source = 'icons/play-icon.png'
            self.ids.plus1.disabled = False
            self.ids.play1.disabled = False

            self.ids.plus2.source = 'icons/plus-icon.png'
            self.ids.play2.source = 'icons/play-icon.png'
            self.ids.plus2.disabled = False
            self.ids.play2.disabled = False

            self.ids.plus3.source = 'icons/plus-icon.png'
            self.ids.play3.source = 'icons/play-icon.png'
            self.ids.plus3.disabled = False
            self.ids.play3.disabled = False

            self.ids.plus4.source = 'icons/plus-icon.png'
            self.ids.play4.source = 'icons/play-icon.png'
            self.ids.plus4.disabled = False
            self.ids.play4.disabled = False

            self.ids.plus5.source = 'icons/plus-icon.png'
            self.ids.play5.source = 'icons/play-icon.png'
            self.ids.plus5.disabled = False
            self.ids.play5.disabled = False
        except Exception as e:
            print(e)
            txt1.text = "An error has ocurred"
    def selectSearch(self, num):
        if num == 1:
            selectedSongsNames.append(currentsong1[0])
            selectedSongsLinks.append(currentsong1[1])
        elif num == 2:
            selectedSongsNames.append(currentsong2[0])
            selectedSongsLinks.append(currentsong2[1])
        elif num == 3:
            selectedSongsNames.append(currentsong3[0])
            selectedSongsLinks.append(currentsong3[1])
        elif num == 4:
            selectedSongsNames.append(currentsong4[0])
            selectedSongsLinks.append(currentsong4[1])
        elif num == 5:
            selectedSongsNames.append(currentsong5[0])
            selectedSongsLinks.append(currentsong5[1])
    def playSong(self, num):
        if num == 1:
            webbrowser.open(currentsong1[1], new=2, autoraise=True)
        elif num == 2:
            webbrowser.open(currentsong2[1], new=2, autoraise=True)
        elif num == 3:
            webbrowser.open(currentsong3[1], new=2, autoraise=True)
        elif num == 4:
            webbrowser.open(currentsong4[1], new=2, autoraise=True)
        elif num == 5:
            webbrowser.open(currentsong5[1], new=2, autoraise=True)

class ClickableImage(ButtonBehavior, Image):
    pass

class LinkScreen(Screen):
    def __init__(self, **kwargs):
        super(LinkScreen, self).__init__(**kwargs)
    def startGetLink(self):
        getLink = Thread(target=self.getLink)
        getLink.start()
    def getLink(self, link):
        videosSearch2 = Video.getInfo(link.text)
        if videosSearch2 != None:
            selectedSongsNames.append(videosSearch2['title'])
            selectedSongsLinks.append(link.text)
            self.ids.linkerror.text = ''
            self.manager.current = 'main'
        else:
            self.ids.linkerror.text = 'The link could not be found'


class DeleteScreen(Screen):
    def __init__(self, **kwargs):
        super(DeleteScreen, self).__init__(**kwargs)
    def deleteSong(self, id):
        if id.text != "":
            try:
                int(id.text)
                try:
                    selectedSongsNames[int(id.text)]
                    selectedSongsNames.pop(int(id.text))
                    selectedSongsLinks.pop(int(id.text))
                    self.manager.current = 'main'
                except Exception as e:
                    self.ids.deleteerror.text = "That id does not refer to a song"
            except Exception as e:
                self.ids.deleteerror.text = 'You must insert a number id'
        else:
            self.ids.deleteerror.text = 'You must insert an id'
            

class EditScreen(Screen):
    def __init__(self, **kwargs):
        super(EditScreen, self).__init__(**kwargs)
    def editName(self, id, newname):
        if id.text != "":
            if newname.text != "":
                try:
                    int(id.text)
                    try:
                        selectedSongsNames[int(id.text)]
                        selectedSongsNames[int(id.text)] = newname.text
                        self.manager.current = 'main'
                    except Exception as e:
                        self.ids.editerror.text = "That id does not refer to a song"
                except Exception as e:
                    self.ids.editerror.text = 'You must insert a number id'
            else:
                self.ids.editerror.text = 'You must insert a new name'
        else:
            self.ids.editerror.text = 'You must insert an id'

class ScreenManager(ScreenManager):
    pass
'''
def resourcePath():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)
    return os.path.join(os.path.abspath("."))
'''
class MainApp(App):
    title = "Youtube Easy Downloader"
    def build(self):
        self.icon = 'logo.png'
        return Builder.load_file('kivy.kv')
    mainS = MainScreen()

if __name__ == "__main__":
    '''kivy.resources.resource_add_path(resourcePath())'''
    MainApp().run()