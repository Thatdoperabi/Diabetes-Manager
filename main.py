from kivy.core.window import Window
from kivy.properties import StringProperty
from kivymd.uix.navigationbar import MDNavigationItem, MDNavigationBar
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
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
        name = self.root.ids.name.text
        email = self.root.ids.email.text
        phone = self.root.ids.phone.text
        print(f"Name: {name}, Email: {email}, Phone: {phone}")

    def on_switch_tabs(
            self,
            bar: MDNavigationBar,
            item: MDNavigationItem,
            item_icon: str,
            item_text: str,
    ):
        self.root.ids.screen_manager.current = item_text

    # def open_menu(self):
    #     if not self.dropdown_menu:
    #         menu_items = [
    #             {
    #                 "text": "Blood Sugar",
    #                 "on_release": lambda x="Sugar": self.menu_callback(x),
    #             },
    #             {
    #                 "text": "Food",
    #                 "on_release": lambda x="Food": self.menu_callback(x),
    #             },
    #             {
    #                 "text": "Both",
    #                 "on_release": lambda x="Both": self.menu_callback(x),
    #             }
    #         ]
    #         self.dropdown_menu = MDDropdownMenu(
    #             caller=self.root.ids.button, items=menu_items
    #         )
    #         self.dropdown_menu.open()


DiabetesManager().run()
