import os
import time
import ffmpeg
import requests as r
import threading
import pytubefix as pf
from kivy.lang import Builder
from kivy.clock import mainthread,Clock
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem
from plyer import filechooser




class NoneTypeQuality(Exception):
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"{self.message}"

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
        self.path = ""
        self.selected_q = ""
        self.selected_core = ""
        self.ext = ""
        self.avail_resol = []
        self.amount_completed = 0
        self.cache = 0
        self.playlist = False
        self.open_resol_dialog = False
        self.raised = False
        self.raised_d = False
        self.stream = None
        self.proceed_confirm = None

    
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file('ui.kv')
    
    def on_start(self):
        #self.warning_dialog_box("Error test").open()
        pass
    
    def on_fetch(self):
        self.url = self.root.ids.url.text
        print(self.url)
        threading.Thread(target=self.fetch_and_download,daemon=True).start()


    def fetch_and_download(self):
        #getting details of video
        
        try :
            if "playlist" in self.url:
                self.playlist = True

            if not self.playlist:
                self.yt = pf.YouTube(url=self.url,on_complete_callback=self.on_complete)
                self.title = self.yt.title
                self.root.ids.thumbnail_title.text = self.title
                self.root.ids.channel_name.text = f"Channel : {self.yt.author}"
                self.image_url = self.yt.thumbnail_url

                for stream in self.yt.streams:
                    if stream.resolution:
                        self.avail_resol.append(stream.resolution)

                self.avail_resol = list(set(self.avail_resol))
                print(self.avail_resol)
                    
                
                #getting thumnails

                response = r.get(url=self.image_url)
                timestamp = int(time.time())
                img_path = f"tmp/thumb_{timestamp}.png"

                with open(img_path,"ab") as f:
                    for chunk in response.iter_content():
                        if chunk:
                            f.write(chunk)
                @mainthread
                def change_thumb():
                    self.root.ids.thumb.source = ''
                    Clock.schedule_once(lambda dt: setattr(self.root.ids.thumb, "source", img_path), 0.3)

                change_thumb()
                self.cache += 1
        
        except pf.exceptions.RegexMatchError as e:
            @mainthread
            def url_raise():
                return self.warning_dialog_box("Enter a Valid Url").open()
            url_raise()


    def on_complete(self,ar1,ar2):
        self.root.ids.qual.disabled = False


    def choose_cat(self,i,i1,i2):
        if i == "a":
            self.root.ids.qual.disabled = True
        else :
            self.root.ids.qual.disabled = False
        if self.root.ids[i].icon == "circle-outline":
            self.root.ids[i].icon = "circle-slice-8"
            self.root.ids[i1].icon = "circle-outline"
            self.root.ids[i2].icon = "circle-outline"
            self.selected_core = i
        elif  self.root.ids[i].icon == "circle-slice-8":
            self.root.ids[i].icon = "circle-outline"
            self.selected_core = "b"

    def vid_downloader(self):
        self.ext = "mp4"
        self.stream.download(output_path=self.path[0])

    def aud_downloader(self):
        self.ext = "m4a"
        self.stream = self.yt.streams.get_audio_only()
        self.stream.download(output_path=self.path[0])

    def both_downloader(self):
        self.ext = "mp4"
        self.stream.download(output_path=self.path[0])

        self.stream = self.yt.streams.get_audio_only()
        self.stream.download(output_path=self.path[0])

        video_path = os.path.join(self.path[0], f"{self.yt.title}.mp4")
        audio_path = os.path.join(self.path[0], f"{self.yt.title}.m4a")
        output_path = os.path.join(self.path[0], f"{self.yt.title}_merged.mp4")

        video_input = ffmpeg.input(video_path)
        audio_input = ffmpeg.input(audio_path)

        # Output (merge)
        ffmpeg.output(
            video_input,       
            audio_input,
            output_path,
            vcodec='copy',
            acodec='aac',
            progress = "prog.txt",
            loglevel = "info",
            strict='experimental' 
        ).run()

        os.remove(os.path.join(self.path[0],video_path))
        os.remove(os.path.join(self.path[0],audio_path))





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
                        on_release=self.close_d,
                        text_color=self.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_release=self.close_d,
                        text_color=self.theme_cls.primary_color,
                    ),
                ]

            )

            self.dialog.open()

    def on_choose_q(self,selected):
        #self.stream = self.yt.streams.get_highest_resolution()
        self.selected_q = selected
        self.stream = self.yt.streams.filter(resolution=selected).first()
        self.file_size = self.stream.filesize_mb
        self.root.ids.file_size.text = str(self.stream.filesize_mb)
    
    def on_download(self):
        print(self.path)

        def no_dir_error():
            if self.path == "" or self.path == None:
                self.raised_d = True
                return self.warning_dialog_box("Select a Dir").open()
            else : self.raised_d = False
        no_dir_error()



        def no_q_error():
            if not self.raised_d:
                if self.selected_q == "" and self.selected_core == "":
                    self.raised = True
                    self.proceed_confirmations("No Quality or Format selected : Defaulting to Aud + Video(high_res)").open()
                    return True 
                elif self.selected_q == "" or self.selected_core == "":
                    self.raised = True
                    if self.selected_q == "":
                        msg = "No Quality selected : Selecting High Res as default"
                    elif self.selected_core == "":
                        msg = "No Format selected : Selecting Both Aud + Video as default"
                    self.proceed_confirmations(msg).open()
                    return True  
                else:
                    self.raised = False
            return False

        if no_q_error():
            return 


        def dummy_1():

            if not (self.raised and self.raised_d):
                self.control_check()
        threading.Thread(target=dummy_1,daemon=True).start()


    def control_check(self):
        @mainthread
        def dummy():
            if self.proceed_confirm:
                self.proceed_confirm.dismiss()
        dummy()
        if not (self.raised and self.raised_d):
            self.start_download()



    def start_download(self):
        
        Clock.schedule_interval(self.progress_bar,0.5)
        threading.Thread(target=self.progress,daemon=True).start()
        if self.yt == None:
            self.yt = pf.YouTube(url=self.url,on_complete_callback=self.on_complete)

        if self.selected_q == "":
            
            self.stream = self.yt.streams.get_highest_resolution()
            self.file_size = self.stream.filesize_mb

        if self.selected_core == "":
            self.selected_core = "b"

        

        if self.selected_core == "v":   
            self.vid_downloader()
            #self.stream.download(output_path=self.path[0])
        elif self.selected_core == "a":
            self.aud_downloader()
        elif self.selected_core == "b":
            self.both_downloader()
    
    def close_d(self,obj):
        if self.dialog:
            self.dialog.dismiss()

    def open_dir(self):
        self.path = filechooser.choose_dir()
        print(self.path)

    def thread_calls(self,called_by):
        if called_by == "download":
            #threading.Thread(target=self.on_download,daemon=True).start()
            self.on_download()

        elif called_by == "choose_dir":
            threading.Thread(target=self.open_dir,daemon=True).start()
    
    def warning_dialog_box(self,warn_msg):
            self.warn = MDDialog(
                title="Error",
                text=warn_msg,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_release=lambda x : self.warn.dismiss(),
                        text_color=self.theme_cls.primary_color,
                    ),
                ]

            )

            return self.warn
        
    def proceed_confirmations(self,msg):
            self.proceed_confirm = MDDialog(
                title="Warning",
                text=msg,
                buttons=[
                    MDFlatButton(
                        text="cancel",
                        theme_text_color="Custom",
                        on_release=lambda x : self.proceed_confirm.dismiss(),
                        text_color=self.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="proceed",
                        theme_text_color="Custom",
                        on_release=lambda x : threading.Thread(target=self.control_check,daemon=True).start(),
                        text_color=self.theme_cls.primary_color,
                    ),
                ]

            )

            return self.proceed_confirm
    
    def progress(self):
        while not self.amount_completed > 98:
            if os.path.exists(os.path.join(self.path[0],f"{self.yt.title}.{self.ext}")):
                self.amount_completed = ((os.path.getsize(os.path.join(self.path[0],f"{self.yt.title}.{self.ext}"))/1048576)/self.file_size)*100
                print(self.amount_completed)
        self.root.ids.progress.value = 100
            
    def progress_bar(self,dt):
        self.root.ids.progress.value = self.amount_completed

                




if __name__ == "__main__":
    app = Ytdownloader()
    app.run()