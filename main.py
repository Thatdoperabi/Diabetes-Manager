from datetime import datetime
import sqlite3
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivymd.uix.navigationbar import MDNavigationItem, MDNavigationBar
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock

from helpers import home_page_helper
from kivy.lang import Builder

from kivymd.app import MDApp

Window.size = (300, 500)


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class BaseScreen(MDScreen):
    image_size = StringProperty()


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

    def close(self):
        self.conn.close()


class DiabetesManager(MDApp):
    current_time = StringProperty()
    fasting_state = None
    dropdown_menu = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        Clock.schedule_interval(self.update_time, 3)
        DBManager.__init__(self)
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
        blood_sugar = self.root.ids.blood_sugar_input.text if self.root.ids.blood_sugar_input.text.strip() != '' else None
        carbs = self.root.ids.carbs.text if self.root.ids.carbs.text.strip() != '' else None
        meal_description = self.root.ids.meal_description.text if self.root.ids.meal_description.text.strip() != '' else None
        fasting = self.fasting_state


        # Save data to database
        db_manager = DBManager()
        db_manager.add_user_data(data_time, blood_sugar, carbs, fasting, meal_description)
        db_manager.close()

    def remove_back_button(self):
        self.root.ids.leading_container.clear_widgets()

    def navigate_to_screen(self, instance):
        self.root.ids.screen_manager.current = 'Screen 1'

    def update_time(self, *args):
        current_time = datetime.now().strftime("%I:%M %p %m/%d/%y")
        if hasattr(self, 'root'):
            self.root.ids.sugar_time.text = f'{current_time}'
            # self.root.ids.carbs_time.text = f'Current Time: {current_time}'
            # self.root.ids.both_time.text = f'Current Time: {current_time}'

    # def on_start(self):
    #     Clock.schedule_interval(self.update_time, 60)

    def update_sugar_level_indicator(self, value):
        if value.isdigit() and int(value) > 180:
            self.root.ids.sugar_level_indicator.color = (1, 0, 0, 1)  # Red
        else:
            self.root.ids.sugar_level_indicator.color = (0, 1, 0, 1)

    def update_time(self, *args):
        self.current_time = datetime.now().strftime("%I:%M %p %m/%d/%y")

    def on_switch_tabs(
            self,
            bar: MDNavigationBar,
            item: MDNavigationItem,
            item_icon: str,
            item_text: str,
    ):
        self.root.ids.screen_manager.current = item_text


DiabetesManager().run()
