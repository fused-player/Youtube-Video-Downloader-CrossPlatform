import requests as r
import threading
import pytubefix as pf
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem


KV = """
<ItemConfirm>
    on_release: 
        root.set_icon(check)
        app.on_choose_q(root.text)

    CheckboxLeftWidget:
        id: check
        group: "check"
        on_release : app.on_choose_q(root.text)


MDBoxLayout:
    orientation : "vertical"

    MDTopAppBar:
        title : "Yt Downloader App"
        pos_hint : {"top":1}
        left_action_items : [["menu",lambda x : nav_drawer.set_state('open')]]

    MDNavigationLayout:
        MDScreenManager:
            id : screen_manager

            MDScreen:
                name : "home"

                MDBoxLayout:
                    id : main_box
                    orientation : "vertical"
                    padding : dp(16)
                    spacing : dp(16)
                    MDBoxLayout:
                        spacing : dp(16)
                        adaptive_height : True
                        MDTextField:
                            id : url
                            hint_text : "Paste URL"
                            mode : "round"
                        
                        MDFillRoundFlatIconButton:
                            
                            text : "Fetch"
                            size_hint_x : 0.4
                            icon : "magnify"
                            on_release : app.on_fetch()
                            #pos_hint : {"center_x":.5,"center_y":.5}
                    
                    MDSmartTile:
                        id : thumb
                        source: "test.png"
                        allow_strech : True
                        pos_hint: {"center_x": .5, "center_y": .5}
                        #size_hint_y : 0.8

                                
                        MDLabel:
                            id : thumbnail_title
                            text: "Julia and Julie"
                            bold: True

                    MDBoxLayout:
                        
                        MDBoxLayout:
                            orientation : "vertical"

                            MDLabel:
                                text : "Channel : "

                            MDLabel:
                                text : "Size : "
                            
                            MDLabel:
                                text : "Type : "

                    MDBoxLayout:
                        id: chip_box
                        spacing: "4dp"
                        adaptive_height : True


                        MDBoxLayout:
                            adaptive_height: True
                            MDIconButton:
                                id : v
                                icon : "circle-outline"
                                icon_size : dp(16)
                                on_release : app.choose_cat("v","a","b")

                            MDLabel:
                                text : "V"

                            MDIconButton:
                                id : a
                                icon : "circle-outline"
                                icon_size : dp(16)
                                on_release : app.choose_cat("a","v","b")


                            MDLabel:
                                text : "A"

                            MDIconButton:
                                id : b
                                icon : "circle-outline"
                                icon_size : dp(16)
                                on_release : app.choose_cat("b","v","a")

                            MDLabel:
                                text : "B"
                        

                            MDRoundFlatIconButton:
                                text: "Quality"
                                icon: "multimedia"
                                on_release : app.show_quality_selection()
                                

                        





                    
                    Widget :
                        size_hint_y : 1

            MDScreen:
                name : "about"
            
        MDNavigationDrawer:
            id : nav_drawer

            MDScrollView:
                MDList:
                    OneLineIconListItem:
                        text : "Home"

                        on_press :
                            screen_manager.current = "home"
                            nav_drawer.set_state('close')

                        IconLeftWidget:
                            icon : "home"

                    OneLineIconListItem:
                        text : "About"

                        on_press :
                            screen_manager.current = "about"
                            nav_drawer.set_state('close')

                        IconLeftWidget:
                            icon : "information"
                    



"""

class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for index,check in enumerate(check_list):
            if check != instance_check:
                check.active = False

            

class Ytdownloader(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = ""
        self.image_url = ""
        self.title = ""
        self.avail_resol = []
        self.playlist = False
        self.open_resol_dialog = False
    
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)
    
    def on_fetch(self):
        self.url = self.root.ids.url.text
        print(self.url)
        threading.Thread(target=self.fetch_and_download,daemon=True).start()


    def fetch_and_download(self):
        #getting details of video

        if "https://www.youtube.com/playlist" in self.url.split("?"):
            self.playlist = True

        if not self.playlist:
            self.yt = pf.YouTube(url=self.url,on_complete_callback=self.on_complete)
            self.title = self.yt.title
            self.root.ids.thumbnail_title.text = self.title
            self.image_url = self.yt.thumbnail_url

            for stream in self.yt.streams:
                if stream.resolution:
                    self.avail_resol.append(stream.resolution)

            self.avail_resol = list(set(self.avail_resol))
            print(self.avail_resol)
                
            
            #getting thumnails
            response = r.get(url=self.image_url)

            with open("tmp/current.png","ab") as f:
                for chunk in response.iter_content():
                    if chunk:
                        f.write(chunk)

            self.root.ids.thumb.source = "tmp/current.png"

    def on_complete(self):
        pass


    def choose_cat(self,i,i1,i2):
        if self.root.ids[i].icon == "circle-outline":
            self.root.ids[i].icon = "circle-slice-8"
            self.root.ids[i1].icon = "circle-outline"
            self.root.ids[i2].icon = "circle-outline"
            self.selected_core = i
        elif  self.root.ids[i].icon == "circle-slice-8":
            self.root.ids[i].icon = "circle-outline"
            self.selected_core = "b"

    def vid_downloader(self):
        pass

    def aud_downloader(self):
        pass

    def both_downloader(self):
        pass


    def show_quality_selection(self):
            items = []

            for q in self.avail_resol:
                items.append(ItemConfirm(text=q))

            self.dialog = MDDialog(
                title="Select Quality",
                type="confirmation",
                items=items,
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                ]

            )

            self.dialog.open()

    def on_choose_q(self,selected):
        print(selected)
        

            

                







    

    



if __name__ == "__main__":
    app = Ytdownloader()
    app.run()