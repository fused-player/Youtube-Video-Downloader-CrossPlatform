import asyncio
from kivy.lang import Builder
from kivymd.app import MDApp


KV = """
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


class Ytdownloader(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)
    



if __name__ == "__main__":
    app = Ytdownloader()
    app.run()