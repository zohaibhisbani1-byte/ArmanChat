from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import pyrebase

# Firebase ki configuration yahan dalein (Apni firebase console se keys le kar)
firebaseConfig = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_PROJECT_ID.firebaseapp.com",
    "databaseURL": "https://YOUR_DATABASE_NAME.firebaseio.com",
    "storageBucket": "YOUR_PROJECT_ID.appspot.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

Window.clearcolor = (0.95, 0.95, 0.95, 1)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        title_label = Label(text='[b]ArmanChat[/b]', markup=True, font_size=32, color=(0.1, 0.4, 0.8, 1), size_hint_y=None, height=60)
        self.username_input = TextInput(hint_text='Apna Naam Likhein', multiline=False, size_hint_y=None, height=50)
        
        login_btn = Button(text='Chat Shuru Karein', size_hint_y=None, height=50, background_color=(0.1, 0.6, 0.9, 1))
        login_btn.bind(on_press=self.go_to_chat)
        
        layout.add_widget(title_label)
        layout.add_widget(self.username_input)
        layout.add_widget(login_btn)
        self.add_widget(layout)
        
    def go_to_chat(self, instance):
        username = self.username_input.text.strip()
        if username:
            chat_screen = self.manager.get_screen('chat')
            chat_screen.set_user(username)
            self.manager.current = 'chat'


class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        self.msg_scroll = ScrollView()
        self.msg_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        self.msg_list.bind(minimum_height=self.msg_list.setter('height'))
        self.msg_scroll.add_widget(self.msg_list)
        
        bottom_layout = BoxLayout(size_hint_y=None, height=60, spacing=5, padding=5)
        self.chat_input = TextInput(hint_text='Message likhein...', multiline=False)
        
        send_btn = Button(text='Bhejein', size_hint_x=None, width=90, background_color=(0.1, 0.6, 0.9, 1))
        send_btn.bind(on_press=self.send_message)
        
        bottom_layout.add_widget(self.chat_input)
        bottom_layout.add_widget(send_btn)
        
        layout.add_widget(self.msg_scroll)
        layout.add_widget(bottom_layout)
        self.add_widget(layout)
        
    def set_user(self, username):
        self.username = username
        
    def send_message(self, instance):
        text = self.chat_input.text.strip()
        if text:
            message_data = {
                "username": self.username,
                "message": text
            }
            db.child("messages").push(message_data)
            
            msg_label = Label(text=f"[b]{self.username}:[/b] {text}", markup=True, size_hint_y=None, height=40, color=(0.2, 0.2, 0.2, 1))
            self.msg_list.add_widget(msg_label)
            self.chat_input.text = ''


class ArmanChatApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ChatScreen(name='chat'))
        return sm

if __name__ == '__main__':
    ArmanChatApp().run()
