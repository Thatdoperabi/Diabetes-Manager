from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationbar import MDNavigationItem, MDNavigationBar
from kivymd.uix.screen import MDScreen
from helpers import home_page_helper

Window.size = (300, 500)


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class BaseScreen(MDScreen):
    image_size = StringProperty()


class DiabetesManager(MDApp):
    dropdown_menu = None

    def on_switch_tabs(
            self,
            bar: MDNavigationBar,
            item: MDNavigationItem,
            item_icon: str,
            item_text: str,
    ):
        self.root.ids.screen_manager.current = item_text

    def open_menu(self):
        if not self.dropdown_menu:
            menu_items = [
                {
                    "text": "Blood Sugar",
                    "on_release": lambda x="Sugar": self.menu_callback(x),
                },
                {
                    "text": "Food",
                    "on_release": lambda x="Food": self.menu_callback(x),
                },
                {
                    "text": "Both",
                    "on_release": lambda x="Both": self.menu_callback(x),
                }
            ]
            self.dropdown_menu = MDDropdownMenu(
                caller=self.root.ids.button, items=menu_items
            )
            self.dropdown_menu.open()

    def menu_callback(self, text_item):
        self.root.current = text_item
        self.dropdown_menu.dismiss()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        return Builder.load_string(home_page_helper)


DiabetesManager().run()
