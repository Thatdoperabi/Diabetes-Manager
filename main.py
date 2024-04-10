from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationbar import MDNavigationItem, MDNavigationBar
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonText

Window.size = (300, 500)


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class BaseScreen(MDScreen):
    image_size = StringProperty()


KV = '''
<BaseMDNavigationItem>

    MDNavigationItemIcon:
        icon: root.icon

    MDNavigationItemLabel:
        text: root.text


<BaseScreen>

BoxLayout:
    orientation: "vertical"
    
    MDBoxLayout:
        orientation: 'horizontal'
        md_bg_color: self.theme_cls.backgroundColor
        size_hint_y: .18
        
        MDTopAppBar:
            type: "small"
            size_hint_x: 1
            pos_hint: {"center_x": .5, "center_y": .5}
    
            MDTopAppBarTitle:
                text: "Diabetes Manager"
                theme_font_size: "Custom"
                font_size: "16dp"
            MDTopAppBarTrailingButtonContainer:
    
                MDActionTopAppBarButton:
                    icon: "dots-vertical"
    
    
    MDFloatLayout:
        orientation: 'horizontal'
        md_bg_color: self.theme_cls.backgroundColor
        
        MDFabButton:
            id: button
            icon: "plus"
            style: "standard"
            pos_hint: {"center_x": .84, "center_y": .14}
            radius: [self.height / 1, ]
            theme_bg_color: "Custom"
            theme_icon_color: "Custom"
            md_bg_color: "purple"
            icon_color: "black"
            on_release: app.open_menu()

    
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: self.theme_cls.backgroundColor
        size_hint_y: .2
        
        MDScreenManager:
            id: screen_manager

            BaseScreen:
                name: "Screen 1"
                image_size: "1024"

            BaseScreen:
                name: "Screen 2"
                image_size: "800"

            BaseScreen:
                name: "Screen 3"
                image_size: "600"
                
            BaseScreen:
                name: "Screen 4"
                image_size: "600"


    
        MDNavigationBar:
            on_switch_tabs: app.on_switch_tabs(*args)
    
            BaseMDNavigationItem
                icon: "gmail"
                text: "Screen 1"
                active: True
    
            BaseMDNavigationItem
                icon: "twitter"
                text: "Screen 2"
    
            BaseMDNavigationItem
                icon: "linkedin"
                text: "Screen 3"
                
            BaseMDNavigationItem
                icon: "linkedin"
                text: "Screen 4"            
'''


class Example(MDApp):
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
            MDDropdownMenu(
                caller=self.root.ids.button, items=menu_items
            ).open()

    def menu_callback(self, text_item):
        print(text_item)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        return Builder.load_string(KV)


Example().run()

# KV = '''
# <BaseMDNavigationItem>
#
#     MDNavigationItemIcon:
#         icon: root.icon
#
#     MDNavigationItemLabel:
#         text: root.text
#
#
# <BaseScreen>
#
# MDBoxLayout:
#     orientation: "vertical"
#     md_bg_color: self.theme_cls.backgroundColor
#
#     MDTopAppBar:
#         type: "small"
#         size_hint_x: 1
#         pos_hint: {"center_x": .5, "center_y": .95}
#
#         MDTopAppBarTitle:
#             text: "Diabetes Manager"
#         MDTopAppBarTrailingButtonContainer:
#
#             MDActionTopAppBarButton:
#                 icon: "dots-vertical"
#
#     MDNavigationBar:
#         on_switch_tabs: app.on_switch_tabs(*args)
#
#         BaseMDNavigationItem
#             icon: "gmail"
#             text: "Screen 1"
#             active: True
#
#         BaseMDNavigationItem
#             icon: "twitter"
#             text: "Screen 2"
#
#         BaseMDNavigationItem
#             icon: "linkedin"
#             text: "Screen 3"
# '''
#
#
# class Example(MDApp):
#     def on_switch_tabs(
#             self,
#             bar: MDNavigationBar,
#             item: MDNavigationItem,
#             item_icon: str,
#             item_text: str,
#     ):
#         self.root.ids.screen_manager.current = item_text
#
#     def build(self):
#         self.theme_cls.theme_style = "Dark"
#         self.theme_cls.primary_palette = "Purple"
#         return Builder.load_string(KV)
#
#
# Example().run()
# -----------------------------------------------------------------------------------------------------------------------
# from kivy.lang import Builder
# from kivy.metrics import dp
# import kivy
# import kivymd
# from kivymd.app import MDApp
# from kivymd.uix.menu import MDDropdownMenu
# from kivymd.uix.snackbar import Snackbar
# from kivy.core.window import Window
#
# Window.size = (300, 500)
#
# KV = '''
# MDBoxLayout:
#     orientation: "vertical"
#
#     MDTopAppBar:
#         title: "MDTopAppBar"
#         left_action_items: [["menu", lambda x: app.callback(x)]]
#         right_action_items: [["dots-vertical", lambda x: app.callback(x)]]
#
#     MDLabel:
#         text: "Content"
#         halign: "center"
# '''
#
#
# class Test(MDApp):
#     def build(self):
#         print("Kivy version:", kivy.__version__)
#         print("KivyMD version:", kivymd.__version__)
#         self.theme_cls.primary_palette = "Purple"
#         self.theme_cls.theme_style = "Dark"
#
#         menu_items = [
#             {
#                 "text": f"Item {i}",
#                 "on_release": lambda x=f"Item {i}": self.menu_callback(x),
#             } for i in range(5)
#         ]
#         self.menu = MDDropdownMenu(items=menu_items)
#
#         return Builder.load_string(KV)
#
#     def callback(self, button):
#         self.menu.caller = button
#         self.menu.open()
#
#     def menu_callback(self, text_item):
#         self.menu.dismiss()
#         Snackbar(text=text_item).open()
#
#
# Test().run()


# Example of a table
#     def build(self):
#         screen = Screen()
#         table = MDDataTable(pos_hint={'center_x': 0.5, 'center_y': 0.5},
#                             size_hint=(0.9, 0.6),
#                             check=True,
#                             row_num=10,
#                             column_data=[
#                                 ("No.", dp(18)),
#                                 ("Food", dp(20)),
#                                 ("Calories", dp(20))
#                             ],
#                             row_data=[
#                                 ("1", "Burger", "300"),
#                                 ("2", "Fries", "200"),
#                                 ("3", "Burger", "300"),
#                                 ("4", "Fries", "200"),
#                                 ("5", "Burger", "300"),
#                                 ("6", "Fries", "200"),
#                                 ("7", "Burger", "300"),
#                                 ("8", "Fries", "200"),
#                                 ("9", "Burger", "300"),
#                             ]
#                             )
#         table.bind(on_check_press=self.check_press)
#         table.bind(on_row_press=self.row_press)
#         screen.add_widget(table)
#         return screen
#
#     def check_press(self, instance_table, current_row):
#         print(instance_table, current_row)
#
#     def row_press(self, instance_table, instance_row):
#         print(instance_table, instance_row)
#
#
# DiabetesManager().run()


# Example of using a builder to create lists
# list_helper = """
# ScrollView:
#     id: container
#     MDList:
#         id: list_container
# """
#
# class DiabetesManager(MDApp):
#     def build(self):
#         screen = Builder.load_string(helpers.list_helper)
#         return screen
#
#     def on_start(self):
#         container = self.root.ids.list_container
#         for i in range(20):
#             items = OneLineListItem(text='Item ' + str(i))
#             container.add_widget(items)
#
#
# DiabetesManager().run()

# Example of lists, icons and imgs
# Flow to create a list : OneLineListItem-> MDList -> ScrollView -> Screen
# def build(self):
#     screen = Screen()
#
#     scroll = ScrollView()
#     list_view = MDList()
#     scroll.add_widget(list_view)
#
#     for i in range(20):
#         image = ImageLeftWidget(source='images.png')
#         items = ThreeLineIconListItem(text='Item ' + str(i), secondary_text='Hello World',
#                                       tertiary_text='Try me')
#         items.add_widget(image)
#         list_view.add_widget(items)
#
#     screen.add_widget(scroll)
#     return screen

# Example of mat dialog
# def show_data(self, obj):
#     if self.username.text is "":
#         check_string = 'Please enter a username'
#     else:
#         check_string = self.username.text + ' does not exist'
#     close_button = MDFlatButton(text='Close', on_release=self.close_dialog)
#     more_button = MDFlatButton(text='More')
#     self.dialog = MDDialog(title='Username Check', text=check_string,
#                            size_hint=(0.5, 1),
#                            buttons=[close_button, more_button])
#     self.dialog.open()
#
#
# def close_dialog(self, obj):
#     self.dialog.dismiss()


# Example of using Builder to create text fields
# username_helper = """
# MDTextField:
#     hint_text: "Enter username"
#     helper_text: "or click on forgot username"
#     helper_text_mode: "on_focus"
#     icon_right: "android"
#     icon_right_color: app.theme_cls.primary_color
#     pos_hint: {'center_x': 0.5, 'center_y': 0.5}
#     size_hint_x: None
#     width: 300
# """
#
#
# class DiabetesManager(MDApp):
#     def build(self):
#         screen = Screen()
#         self.theme_cls.primary_palette = "Purple"
#         # username = MDTextField(text='Enter username',
#         #                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
#         #                        size_hint_x=None, width=300)
#         username = Builder.load_string(username_helper)
#         screen.add_widget(username)
#         return screen


# Example of theme
# def build(self):
#     self.theme_cls.primary_palette = "Purple"
#     self.theme_cls.theme_style = "Dark"
#     screen = Screen()
#     btn_flat = MDRectangleFlatButton(text='Hello World',
#                                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
#     screen.add_widget(btn_flat)
#     return screen


# Example of buttons and screen
# screen = Screen()
# btn_flat = MDRectangleFlatButton(text='Hello World',
#                                  pos_hint={'center_x': 0.5, 'center_y': 0.5})
# icon_btn = MDIconButton(icon='android',
#                         pos_hint={'center_x': 0.5, 'center_y': 0.5})
# screen.add_widget(btn_flat)
# return screen


# Examples of text labels and icons
# label = MDLabel(text='Hello World', halign='center', theme_text_color='Custom',
#                 text_color=(236 / 255.0, 98 / 255.0, 81 / 255.0, 1),
#                 font_style='H1')
# icon_label = MDIcon(icon='language-python', halign='center')
# return icon_label
