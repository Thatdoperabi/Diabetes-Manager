import os
import threading
import requests
import time
from datetime import datetime
import sqlite3
from kivy.core.window import Window
from kivy.properties import StringProperty, ColorProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationbar import MDNavigationItem
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivymd.app import MDApp
from dotenv import load_dotenv
import socket

from helpers import home_page_helper

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

Window.size = (300, 500)

# Define the system message to set the assistant's persona or rules
system_message = {
    "role": "system",
    "content": "You are a helpful nutritionists named Rabi who provides clear and concise answers. You specialize in "
               "diabetic education. You provide meal recommendations and blood sugar predictions based off of blood "
               "sugar readings and carb intake."
}

class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class BaseScreen(MDScreen):
    image_size = StringProperty()


class HomeScreen(BaseScreen):
    pass


class UserInputScreen(BaseScreen):
    pass


class AiScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conversation_history = []

    def send_message(self):
        user_input = self.ids.user_input.text
        if user_input.strip() == "":
            self.add_message("system", "Please enter a message.")
            return

        prompt = user_input
        self.conversation_history.append({"role": "user", "content": prompt})
        self.add_message("user", prompt)
        self.ids.user_input.text = ""
        threading.Thread(target=self.request_response, args=(prompt,)).start()

    def request_response(self, prompt):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        json_data = {
            "model": "gpt-3.5-turbo",
            "messages": [system_message] + self.conversation_history
        }

        retries = 5
        backoff_factor = 0.3
        for i in range(retries):
            try:
                response = requests.post(url, headers=headers, json=json_data, timeout=10)
                response.raise_for_status()
                data = response.json()
                result = data['choices'][0]['message']['content'].strip()
                self.conversation_history.append({"role": "assistant", "content": result})
                self.add_message("assistant", result)
                return
            except requests.RequestException as e:
                if isinstance(e, requests.exceptions.ConnectionError) and isinstance(e.args[0], socket.gaierror):
                    if i < retries - 1:
                        time.sleep(backoff_factor * (2 ** i))
                        continue
                if i < retries - 1:
                    time.sleep(backoff_factor * (2 ** i))
                else:
                    self.add_message("system", f"Connection Error: {str(e)}")
                    break

    @mainthread
    def add_message(self, role, content):
        message_box = MDBoxLayout(orientation='vertical', size_hint_y=None, padding=[10, 20, 10, 10], spacing=10)

        message_label = MDLabel(
            text=f"{role.capitalize()}: {content}",
            size_hint_y=None,
            text_size=(self.width - 20, None),
            halign='left',
            valign='top'
        )
        message_label.bind(texture_size=lambda instance, value: setattr(message_label, 'height', value[1]))
        message_label.bind(texture_size=lambda instance, value: setattr(message_box, 'height', value[1] + 30))
        message_box.add_widget(message_label)

        self.ids.message_container.add_widget(message_box)
        self.ids.scroll_view.scroll_y = 0

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect('diabetesmanager.db')
        self.cursor = self.conn.cursor()
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS user_info(
            id INTEGER PRIMARY KEY,
            data_time DATETIME,
            blood_sugar INTEGER,
            carbs INTEGER,
            fasting INTEGER,
            meal_description TEXT           
            )
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def add_user_data(self, data_time, blood_sugar, carbs, fasting, meal_description):
        blood_sugar_value = None if blood_sugar is None else blood_sugar
        fasting_value = None if fasting is None else fasting
        carbs_value = None if carbs is None else carbs
        self.cursor.execute('''
            INSERT INTO user_info (data_time, blood_sugar, carbs, fasting, meal_description)
            VALUES (?, ?, ?, ?, ?)
        ''', (data_time, blood_sugar_value, carbs_value, fasting_value, meal_description))
        self.conn.commit()

    def calculate_a1c(self, average_blood_sugar):
        if average_blood_sugar is None:
            return None
        a1c = (average_blood_sugar + 46.7) / 28.7
        return a1c

    def update_a1c(self):
        stats = self.get_blood_sugar_stats()
        if stats and stats[0] is not None:
            avg_blood_sugar = stats[0]
            a1c = self.calculate_a1c(avg_blood_sugar)
            return a1c
        return None

    def get_blood_sugar_stats(self):
        self.cursor.execute('''
            SELECT AVG(blood_sugar), MIN(blood_sugar), MAX(blood_sugar)
            FROM user_info
            WHERE blood_sugar IS NOT NULL
            AND blood_sugar IS NOT ''
        ''')
        result = self.cursor.fetchone()
        return result  # Returns a tuple (avg, min, max)

    def close(self):
        self.conn.close()


class DiabetesManager(MDApp):
    icon_color = ColorProperty([0.5, 0.5, 0.5, 1])  # Default gray color in RGBA
    current_time = StringProperty()
    fasting_state = None
    dropdown_menu = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        Clock.schedule_interval(self.update_time, 3)
        Clock.schedule_once(self.update_blood_sugar_stats, 0)
        DBManager.__init__(self)
        Builder.load_file('home_screen.kv')
        Builder.load_file('user_input_screen.kv')
        Builder.load_file('ai_screen.kv')  # Load the AI screen kv file
        return Builder.load_string(home_page_helper)

    def update_fasting_state(self, instance, state):
        self.fasting_state = 1 if state == "Fasting" else 0

    def add_back_button(self):
        back_button = MDIconButton(
            icon="arrow-left",
            pos_hint={'center_y': 0.5},
            size_hint=(None, None),
            size=("48dp", "48dp")
        )
        back_button.bind(on_release=self.navigate_to_screen)
        self.root.ids.leading_container.clear_widgets()
        self.root.ids.leading_container.add_widget(back_button)
        self.root.ids.leading_container.padding = [0, 0, 10, 0]

    def save_user_data(self):
        # Retrieve data from UI
        data_time = self.current_time
        current_screen = self.root.ids.screen_manager.current_screen
        blood_sugar = current_screen.ids.blood_sugar_input.text if current_screen.ids.blood_sugar_input.text.strip() != '' else None
        carbs = current_screen.ids.carbs.text if current_screen.ids.carbs.text.strip() != '' else None
        meal_description = current_screen.ids.meal_description.text if current_screen.ids.meal_description.text.strip() != '' else None
        fasting = self.fasting_state

        # Save data to database
        db_manager = DBManager()
        db_manager.add_user_data(data_time, blood_sugar, carbs, fasting, meal_description)
        db_manager.close()

        self.update_blood_sugar_stats()

    def remove_back_button(self):
        self.root.ids.leading_container.clear_widgets()

    def navigate_to_screen(self, instance):
        self.root.ids.screen_manager.current = 'home_screen'

    def update_time(self, *args):
        self.current_time = datetime.now().strftime("%I:%M %p %m/%d/%y")
        # Accessing the specific screen by its name in the ScreenManager
        user_input_screen = self.root.ids.screen_manager.get_screen('user_input_screen')
        if hasattr(user_input_screen, 'ids') and 'sugar_time' in user_input_screen.ids:
            user_input_screen.ids.sugar_time.text = self.current_time
        else:
            print("sugar_time widget not found")

    def update_sugar_level_indicator(self, value):
        try:
            sugar_level = int(value)
            if sugar_level < 180:
                self.icon_color = [0, 1, 0, 1]  # Green
            else:
                self.icon_color = [1, 0, 0, 1]  # Red
        except ValueError:
            self.icon_color = [0.5, 0.5, 0.5, 1]

    def update_blood_sugar_stats(self, *args):
        db_manager = DBManager()
        avg, low, high = db_manager.get_blood_sugar_stats()
        a1c = db_manager.update_a1c()
        db_manager.close()

        # Update the UI with the retrieved values
        home_screen = self.root.ids.screen_manager.get_screen('home_screen')
        home_screen.ids.avg_value.text = str(round(avg)) if avg is not None else "N/A"
        home_screen.ids.low_value.text = str(round(low)) if low is not None else "N/A"
        home_screen.ids.high_value.text = str(round(high)) if high is not None else "N/A"

        if a1c is not None:
            home_screen.ids.a1c_value.text = f"{a1c:.2f}%"
            home_screen.ids.a1c_value.text_color = [0, 1, 0, 1] if a1c < 7.0 else [1, 0, 0, 1]
        else:
            home_screen.ids.a1c_value.text = "N/A"
            home_screen.ids.a1c_value.text_color = [1, 0, 0, 1]

    def on_switch_tabs(self, bar, item, item_icon, item_text):
        # Mapping text to screen names
        screen_map = {
            "Home": "home_screen",
            # "Screen 2": "screen_2",
            "AI Helper": "ai_screen",
            # "Screen 4": "screen_4"
        }
        new_screen_name = screen_map.get(item_text)
        if new_screen_name:
            self.root.ids.screen_manager.current = new_screen_name


if __name__ == '__main__':
    DiabetesManager().run()
