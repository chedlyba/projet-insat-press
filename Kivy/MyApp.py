import os
from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
import os
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView

Builder.load_file('menu_copy.kv')

class MyLayout(Widget) :

    cur_folder = ObjectProperty(None)
    file_chooser = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(str(os.getcwd()))
        self.cur_folder.text = os.getcwd()



    def selected(self, filename) :
        try:
            self.ids.image.source = filename[0]
            print(filename)
        except:
            pass

    def upload_file(self, filename):
        try:
            print(filename[0])
        except:
            pass

    def upload_folder(self,filename):
        try:
            print(filename)

        except:
            pass

class MyApp(App):

    def build(self):
        return MyLayout()

if __name__ == '__main__' :
    MyApp().run() 

