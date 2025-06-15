import os
import time
import random
import string
import ssl
import subprocess
import requests as r
import threading
import pytubefix as pf
from jnius import autoclass
from kivy.lang import Builder
from kivy.clock import mainthread,Clock
from kivymd.app import MDApp
from kivy import platform
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.button import MDFlatButton
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.properties import StringProperty,BooleanProperty,ObjectProperty
from kivymd.uix.list import OneLineAvatarIconListItem


if platform == "android":
    from android.storage import primary_external_storage_path,app_storage_path
    from android.permissions import request_permissions, Permission, check_permission  # pylint: disable=import-error # type: ignore
    request_permissions([Permission.READ_EXTERNAL_STORAGE,
                        Permission.WRITE_EXTERNAL_STORAGE])
    
    
    ssl._create_default_https_context = ssl._create_stdlib_context

    main_path = primary_external_storage_path()

    app_dir = app_storage_path()
else :
    import ffmpeg
    from plyer import filechooser


class MDSelectableRecycleBoxLayout(FocusBehavior,
                                   LayoutSelectionBehavior,
                                   RecycleBoxLayout):
    ''' Adds selection and focus behavior to the view. '''
    pass
class PlaylistItem(RecycleDataViewBehavior, MDBoxLayout):
    title = StringProperty()
    thumb = StringProperty()
    url = StringProperty()
    selected = BooleanProperty()
    obj = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos):
            self.parent.select_with_touch(self.index, touch)
            return True
        return False

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected


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
        self.finished_videos = 0
        self.i = 0
        self.cache = 0
        self.playlist = False
        self.open_resol_dialog = False
        self.raised = False
        self.raised_d = False
        self.stream = None
        self.proceed_confirm = None
        self.uni = None
        self.tmp_dir = ""

        self.file_manager_obj = MDFileManager(
            select_path = self.select_path,
            exit_manager = self.exit_manager,
            preview = False
        )
    
    def select_path(self,current_path):
        print(current_path)
        self.path = [current_path]
        self.file_manager_obj.close()
    
    def exit_manager(self):
        self.file_manager_obj.close()

    
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file('ui.kv')
    
    def on_start(self):
        if platform == "android":
            if not self.check_manage_external_storage():
                self.check_manage_external_storage()
                self.warning_dialog_box("Please grant All Files Access permission.").open()
            os.makedirs(os.path.join(app_dir,'tmp/'), exist_ok=True)
            os.makedirs(os.path.join(app_dir,'assets/'), exist_ok=True)
            self.tmp_dir = os.path.join(app_dir,"tmp/")
            self.ffmpeg_android = os.path.join(os.getcwd(),"assets/ffmpeg")

    def sanitize_filename(self, filename):
        # Remove invalid characters for Android
        invalid_chars = ['?', '|', '<', '>', ':', '"', '/', '\\', '*']
        for char in invalid_chars:
            filename = filename.replace(char, '')
        # Remove trailing spaces and dots
        filename = filename.strip('. ')
        return filename


    
    def on_fetch(self):
        self.reset_state()
        self.url = self.root.ids.url.text
        print(self.url)
        threading.Thread(target=self.fetch_and_download,daemon=True).start()


    def fetch_and_download(self):
        #getting details of video
        
        try :
            if "playlist" in self.url:
                self.playlist = True
                @mainthread
                def open_warn():
                    self.warning_dialog_box("Go to Playlist Scetion to Download").open()
                open_warn()
                self.playlist = False

            if not "playlist" in self.url:
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
                if platform == "android":
                    img_path = os.path.join(self.tmp_dir,f"thumb_{timestamp}.png")
                else :
                    img_path = f"thumb_{timestamp}.png"

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
        self.amount_completed = 0
        self.root.ids.progress.value = 0
        @mainthread
        def up():
            self.amount_completed = 0
            self.root.ids.progress.value = 0
        up()


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
        safe_title = self.sanitize_filename(self.yt.title)
        filename = f"{safe_title}.mp4"
        self.stream.download(output_path=self.path[0],filename=filename)

    def aud_downloader(self):
        self.ext = "m4a"
        self.stream = self.yt.streams.get_audio_only()
        safe_title = self.sanitize_filename(self.yt.title)
        filename = f"{safe_title}.m4a"
        self.stream.download(output_path=self.path[0],filename=filename)

    def both_downloader(self):
        if self.stream is None:
            self.stream = self.yt.streams.get_by_resolution(self.selected_q)
    
        safe_title = self.sanitize_filename(self.stream.title)
        filename_video = f"{safe_title}.mp4"
        
        self.stream.download(output_path=self.path[0], filename=filename_video)

        self.stream = self.yt.streams.get_audio_only()

        safe_title = self.sanitize_filename(self.stream.title)
        filename_audio = f"{safe_title}.m4a"

        self.stream.download(output_path=self.path[0], filename=filename_audio)


        output_path = os.path.join(self.path[0], f"{safe_title}_merged.mp4")
        
        

        video_path = os.path.join(self.path[0], filename_video)
        audio_path = os.path.join(self.path[0], filename_audio)

        # Merge
        if platform == "android":
            result = subprocess.run(
                f'/system/bin/linker64 "{self.ffmpeg_android}" -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac -strict experimental -y "{output_path}"',
                shell=True, capture_output=True, text=True
            )
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
        else:
            ffmpeg.output(
                ffmpeg.input(video_path),
                ffmpeg.input(audio_path),
                output_path,
                vcodec='copy', acodec='aac',
                loglevel='info',
                strict='experimental'
            ).run()

        # Clean up
        os.remove(video_path)
        os.remove(audio_path)

        self.root.ids.progress.value = 100
        self.amount_completed = 100







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

        if platform == "android":
            Environment = autoclass('android.os.Environment')
            if Environment.isExternalStorageManager():
                print("All files access granted")
            else:
                print("Not granted")

        @mainthread
        def reset_progress():
            self.amount_completed = 0
            self.root.ids.progress.value = 0

        reset_progress()
        try:
            self.root.ids.main_fetch.disabled = True

            if self.yt is None:
                self.yt = pf.YouTube(url=self.url, on_complete_callback=self.on_complete)

            # Set default core and quality if not selected
            if self.selected_core == "":
                self.selected_core = "b"

            if self.selected_q == "":
                self.stream = self.yt.streams.get_highest_resolution()
            else:
                self.stream = self.yt.streams.filter(resolution=self.selected_q).first()

            # Handle possible None stream
            if self.stream is None:
                self.warning_dialog_box("Failed to get stream for selected resolution").open()
                return

            self.file_size = self.stream.filesize_mb


            Clock.schedule_interval(self.progress_bar, 0.5)
            threading.Thread(target=self.progress, daemon=True).start()


            if self.selected_core == "v":
                self.vid_downloader()
            elif self.selected_core == "a":
                self.aud_downloader()
            elif self.selected_core == "b":
                self.both_downloader()
            
            self.root.ids.main_fetch.disabled = False

        except Exception as e : 
            self.root.ids.main_fetch.disabled = False
            print(f"ERROR in start_download: {e}")

    
    def close_d(self,obj):
        if self.dialog:
            self.dialog.dismiss()

    def open_dir(self):
        if self.uni:
            self.uni.dismiss()

        if platform == "android":
            @mainthread
            def filem():
                self.file_manager_obj.show(main_path)
            filem()
        else :
        
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
    def uni_dialog_box(self,warn_msg,title,func):
            self.uni = MDDialog(
                title=title,
                text=warn_msg,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        theme_text_color="Custom",
                        on_release=lambda x : func(),
                        text_color=self.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="Cancel",
                        theme_text_color="Custom",
                        on_release=lambda x : self.uni.dismiss(),
                        text_color=self.theme_cls.primary_color,
                    ),
                ]

            )

            return self.uni
        
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
        expected_path = os.path.join(self.path[0], self.sanitize_filename(self.stream.default_filename))
        self.amount_completed = 0
        while not self.amount_completed > 98:
            if os.path.exists(expected_path):
                size = os.path.getsize(expected_path)
                self.amount_completed = (size / (self.file_size * 1048576)) * 100
                print(f"Progress: {self.amount_completed:.2f}%")
            time.sleep(0.5)
        @mainthread
        def finish():
            if not self.selected_core == "b":
                self.root.ids.progress.value = 100
                self.amount_completed = 100
            else :
                self.amount_completed = 90
                self.root.ids.progress.value = 90
        finish()
            
    def progress_bar(self,dt):
        self.root.ids.progress.value = self.amount_completed

    def reset_state(self):
        self.yt = None
        self.path = ""
        self.stream = None
        self.selected_q = ""
        self.selected_core = ""
        self.ext = ""
        self.avail_resol = []
        self.file_size = 0
        self.amount_completed = 0
        self.finished_videos = 0
        self.raised = False
        self.raised_d = False
        self.proceed_confirm = None
        self.uni = None
        self.root.ids.progress.value = 0
        self.root.ids.file_size.text = ""
        self.root.ids.thumb.source = ""
        self.root.ids.thumbnail_title.text = ""
        self.root.ids.channel_name.text = ""
        self.yt_play = None
        self.root.ids.play_download.disabled = True

    def on_fetch_playlist(self):
        self.reset_state()
        if "playlist" in self.root.ids.url_play.text:
            self.root.ids.play_fetch.disabled = True
            self.url_play = self.root.ids.url_play.text
            threading.Thread(target=self.on_f_p,daemon=True).start()
        else :
            def open_warn():
                self.warning_dialog_box("Go to Home to Download a Single Video").open()
            open_warn()

    def on_f_p(self):
        self.play_items = []
        data_list = []
        if self.yt_play == None:
            self.yt_play = pf.Playlist(url=self.url_play)

        count = 0
        
        for video in self.yt_play.videos:
            if video == None:
                break
            title = video.title
            r_string = self.random_string()
            thumb_url = video.thumbnail_url
            video = video.streams.get_highest_resolution(progressive=True)


            response = r.get(thumb_url)
            if platform == "android":
                c_path = os.path.join(self.tmp_dir,f'{r_string}.png')
            else : 
                c_path = os.path.join(self.path,f'tmp/{r_string}.png')

            with open(c_path,"wb") as f:
                for chunk in response:

                    if chunk:
                        f.write(chunk)
            timeout = 5  # seconds
            elapsed = 0
            while not os.path.exists(c_path) and elapsed < timeout:
                time.sleep(0.1)
                elapsed += 0.1

            if timeout>5 and not c_path:
                if platform == "android":
                    image = os.path.join(self.path,f'tmp/blank.png')
                else :
                    image = 'test.png'
            else : image = c_path

            data_list.append({
                "title": title,
                "thumb": image,
                "selected": False,
                "index": count,
                "url": video.url,
                "obj": video
            })

            count += 1

            @mainthread
            def update_rv():
                self.root.ids.play_list.data = data_list

            update_rv()
        self.root.ids.play_fetch.disabled = False
        self.root.ids.play_download.disabled = False

    def set_selected(self, index, value):
        self.root.ids.play_list.data[index]["selected"] = value

    def on_playlist_download(self):

        selected_nodes = self.root.ids.play_list.children[0].selected_nodes

        for i in selected_nodes:
            print(self.root.ids.play_list.data[i]["url"])

        if self.path == "":
            self.uni_dialog_box("Choose a Dir","Select Dir",self.open_dir).open()
        if not self.path == "":
            threading.Thread(target=self._download_playlist,args=(selected_nodes,),daemon=True).start()
        

        
    def _download_playlist(self,nodes):

        
        self.root.ids.play_download.disabled = True
        if len(nodes) < 1 : print("Nothing")
        self.selected_videos = nodes
        Clock.schedule_interval(self.update_playlist_ui,0.5)
        for i,node in enumerate(nodes):
            video = self.root.ids.play_list.data[node]["obj"]

            

            video.download(output_path=self.path[0])

            print(f"Download of {video} Completed")
            self.finished_videos = i + 1
        
        def complete():
            print("COmplete")
            self.root.ids.play_list.children[0].selected_nodes = []
            self.root.ids.play_download.disabled = False
        threading.Thread(target=complete,daemon=True).start()

        

    def update_playlist_ui(self,dt):
        self.root.ids.downloaded.text = f"Downloaded : {self.finished_videos}/{len(self.selected_videos)}"

        if len(self.selected_videos) < self.finished_videos:
            self.finished_videos = 0
            Clock.unschedule(self.update_playlist_ui,0.1)
            
    def random_string(self):
        length = 8
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        return random_string
    
    def check_manage_external_storage(self):
        Environment = autoclass('android.os.Environment')
        Settings = autoclass('android.provider.Settings')
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        VERSION = autoclass('android.os.Build$VERSION')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')

        if VERSION.SDK_INT >= 30:
            if not Environment.isExternalStorageManager():
                intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
                uri = Uri.fromParts("package", PythonActivity.mActivity.getPackageName(), None)
                intent.setData(uri)
                PythonActivity.mActivity.startActivity(intent)
                return False
            else:
                return True
        else:
            return True
            





if __name__ == "__main__":
    app = Ytdownloader()
    app.run()