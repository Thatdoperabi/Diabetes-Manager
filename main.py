import time
from datetime import datetime

import kivy
import kivymd
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivymd.uix.navigationbar import MDNavigationItem, MDNavigationBar
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.uix.tab import MDTabsItem, MDTabsItemIcon, MDTabsBadge, MDTabsItemText

from helpers import home_page_helper
from kivy.lang import Builder

from kivymd.app import MDApp

Window.size = (300, 500)


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class BaseScreen(MDScreen):
    image_size = StringProperty()


class DiabetesManager(MDApp):
    dropdown_menu = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        Clock.schedule_interval(self.update_time, 3)
        return Builder.load_string(home_page_helper)

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

    def remove_back_button(self):
        self.root.ids.leading_container.clear_widgets()

    def navigate_to_screen(self, instance):
        self.root.ids.screen_manager.current = 'Screen 1'

    def submit_form(self):
        time = self.root.ids.name.time
        email = self.root.ids.email.text
        phone = self.root.ids.phone.text
        print(f"Name: {time}, Email: {email}, Phone: {phone}")

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

    def save_user_data(self, time, sugar_level, meal_time):
        # Connect to database and insert data
        # This is just a placeholder for database operation
        print(f"Saving data: Time - {time}, Sugar Level - {sugar_level}, Meal Time - {meal_time}")


    def on_switch_tabs(
            self,
            bar: MDNavigationBar,
            item: MDNavigationItem,
            item_icon: str,
            item_text: str,
    ):
        self.root.ids.screen_manager.current = item_text


DiabetesManager().run()
