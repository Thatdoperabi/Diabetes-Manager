import calendar
import logging
import os
import threading

import asynckivy
import requests
import time
from datetime import datetime, timedelta
import sqlite3

import self
from kivy.core.window import Window
from kivy.properties import StringProperty, ColorProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItemTrailingIcon
from kivymd.uix.navigationbar import MDNavigationItem
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivymd.app import MDApp
from dotenv import load_dotenv
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.garden.graph import Graph, MeshLinePlot
import socket
from kivy.uix.togglebutton import ToggleButton
from helpers import home_page_helper
from kivymd.uix.expansionpanel import MDExpansionPanel

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

Window.size = (300, 500)

system_message = {
    "role": "system",
    "content": "You are a helpful nutritionists named Rabi who provides clear and concise answers. You specialize in "
               "diabetic education. You provide meal recommendations and blood sugar predictions based off of blood "
               "sugar readings and carb intake."
}


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

class NavigationItem(BoxLayout):
    screen_name = StringProperty('')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = MDApp.get_running_app()
            app.switch_to_tab(self.screen_name)
            return True  # Consume the touch event so it doesn't propagate further
        return super().on_touch_down(touch)


class BaseScreen(MDScreen):
    image_size = StringProperty()


class HomeScreen(BaseScreen):
    pass


class HistoryScreen(BaseScreen):
    def on_enter(self):
        self.display_history()
        self.update_graph()

    def update_graph(self):
        db_manager = DBManager()
        data = db_manager.get_last_30_days_aggregated_data()
        db_manager.close()

        if not data:
            return

        filtered_data = [(datetime.strptime(row[0], "%Y-%m-%d"), row[1], row[2]) for row in data if row[1] is not None and row[2] is not None]
        if not filtered_data:
            return

        dates, avg_blood_sugar, total_carbs = zip(*filtered_data)

        dates = list(dates)[::-1]
        avg_blood_sugar = list(avg_blood_sugar)[::-1]
        total_carbs = list(total_carbs)[::-1]


        graph = Graph(
            xlabel='Date',
            ylabel='Value',
            x_ticks_minor=1,
            x_ticks_major=1,
            y_ticks_major=10,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            xmin=0,
            xmax=len(dates) - 1 if len(dates) > 1 else 1,
            ymin=80,
            ymax=max(max(avg_blood_sugar), max(total_carbs)) + 10,
            size_hint_y=None,
            height=150
        )

        avg_blood_sugar_plot = MeshLinePlot(color=[1, 0, 0, 1])  # Red color
        avg_blood_sugar_plot.points = [(i, avg_blood_sugar[i]) for i in range(len(avg_blood_sugar))]
        graph.add_plot(avg_blood_sugar_plot)

        # Create total carbs plot
        total_carbs_plot = MeshLinePlot(color=[0, 0, 1, 1])  # Blue color
        total_carbs_plot.points = [(i, total_carbs[i]) for i in range(len(total_carbs))]
        graph.add_plot(total_carbs_plot)

        # Add the graph to the screen
        graph_container = self.ids.graph_container
        graph_container.clear_widgets()
        graph_container.add_widget(graph)

    def display_history(self):
        db_manager = DBManager()
        data = db_manager.get_last_30_days_aggregated_data()
        db_manager.close()

        if not data:
            return

        container = self.ids.history_container
        container.clear_widgets()

        for row in data:
            date, avg_blood_sugar, total_carbs = row

            if avg_blood_sugar is None and total_carbs is None:
                continue

            if avg_blood_sugar is not None:
                avg_blood_sugar = round(avg_blood_sugar)

            avg_blood_sugar_text = f"Average Blood Sugar: {avg_blood_sugar}" if avg_blood_sugar is not None else "No data"
            total_carbs_text = f"Total Carbs: {total_carbs}" if total_carbs is not None else "No data"

            panel = MDBoxLayout(orientation='vertical', size_hint_y=None)

            header = ToggleButton(
                text=date,
                size_hint_y=None,
                height=dp(40),
                group='expansion_panels',
                background_normal='',
                background_color=(0.5, 0.5, 0.5, 1),
                color=(1, 1, 1, 1),
            )
            header.bind(on_release=lambda btn, p=panel: self.toggle_panel(p))

            content_box = MDBoxLayout(orientation='vertical', size_hint_y=None, height=0, opacity=0)
            content_box.add_widget(MDLabel(text=avg_blood_sugar_text, size_hint_y=None, height=dp(20), halign="left"))
            content_box.add_widget(MDLabel(text=total_carbs_text, size_hint_y=None, height=dp(20), halign="left"))

            panel.add_widget(header)
            panel.add_widget(content_box)

            panel.height = dp(40)
            panel.size_hint_y = None

            container.add_widget(panel)

    def toggle_panel(self, panel):
        content_box = panel.children[0]

        if content_box.height == 0:
            content_box.height = dp(40)
            content_box.opacity = 1
            panel.height = dp(40) + content_box.height
        else:
            content_box.height = 0
            content_box.opacity = 0
            panel.height = dp(40)

        panel.size_hint_y = None
        panel.do_layout()

class ExportScreen(BaseScreen):
    def on_enter(self):
        self.populate_calendar()
        self.ids.month_label.text = f"{datetime.now().strftime('%B %Y')}"

    def populate_calendar(self):
        calendar_grid = self.ids.calendar_grid
        calendar_grid.clear_widgets()

        today = datetime.today()
        year = today.year
        month = today.month

        # Update the month label at the top
        self.ids.month_label.text = f"{today.strftime('%B %Y')}"

        # Get the first day of the month and the total number of days
        first_day_of_month, total_days = calendar.monthrange(year, month)

        db_manager = DBManager()

        for day in range(1, total_days + 1):
            # Fetch data for this specific day
            date_str = f"{year}-{month:02d}-{day:02d}"
            avg_blood_sugar = db_manager.get_average_blood_sugar_for_date(date_str)
            total_carbs = db_manager.get_total_carbs_for_date(date_str)

            cell_text = f"[size=12][b]{day}[/b][/size]\n[size=12][color=#FF0000]{avg_blood_sugar or 'N/A'}[/color][/size]\n[size=10][color=#0000FF]{total_carbs or 'N/A'}[/color][/size]"

            # Add empty labels for days before the first of the month
            if day == 1:
                for _ in range(first_day_of_month):
                    calendar_grid.add_widget(MDLabel())

            # Add the day cell
            calendar_grid.add_widget(MDLabel(
                text=cell_text,
                markup=True,
                halign="center",
                valign="middle",
                size_hint=(1, None),  # Ensure the cell uses the available width
                height=dp(80),  # Adjust the height to fit the content
                theme_text_color="Secondary",
            ))

        db_manager.close()


class ExpansionPanelItem(MDExpansionPanel):
    ...


class TrailingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
):
    ...


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
            data_time TEXT,
            blood_sugar INTEGER,
            carbs INTEGER,
            fasting INTEGER,
            meal_description TEXT           
            )
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def add_user_data(self, data_time, blood_sugar, carbs, fasting, meal_description):
        if isinstance(data_time, str):
            try:
                data_time = datetime.strptime(data_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                logging.error("Incorrect data_time format, should be YYYY-MM-DD HH:MM:SS")
                return

        blood_sugar_value = None if blood_sugar is None else blood_sugar
        fasting_value = None if fasting is None else fasting
        carbs_value = None if carbs is None else carbs
        data_time_str = data_time.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO user_info (data_time, blood_sugar, carbs, fasting, meal_description)
            VALUES (?, ?, ?, ?, ?)
        ''', (data_time_str, blood_sugar_value, carbs_value, fasting_value, meal_description))
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
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            SELECT AVG(blood_sugar), MIN(blood_sugar), MAX(blood_sugar)
            FROM user_info
            WHERE blood_sugar IS NOT NULL
            AND blood_sugar IS NOT ''
            AND data_time >= ?
        ''', (thirty_days_ago,))
        result = self.cursor.fetchone()
        return result

    def get_last_30_days_aggregated_data(self):
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            SELECT DATE(data_time), AVG(blood_sugar), SUM(carbs)
            FROM user_info
            WHERE data_time >= ?
            GROUP BY DATE(data_time)
            ORDER BY DATE(data_time)
        ''', (thirty_days_ago,))
        results = self.cursor.fetchall()

        aggregated_data = []
        date_set = set(row[0] for row in results)
        current_date = datetime.now().date()
        for i in range(30):
            check_date = (current_date - timedelta(days=i)).strftime('%Y-%m-%d')
            if check_date in date_set:
                for row in results:
                    if row[0] == check_date:
                        aggregated_data.append(row)
            else:
                aggregated_data.append((check_date, None, None))

        return aggregated_data

    def get_today_average_blood_sugar(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute('''
            SELECT AVG(blood_sugar)
            FROM user_info
            WHERE DATE(data_time) = ?
        ''', (today,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_today_total_carbs(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute('''
            SELECT SUM(carbs)
            FROM user_info
            WHERE DATE(data_time) = ?
        ''', (today,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_average_blood_sugar_for_date(self, date_str):
        self.cursor.execute('''
            SELECT AVG(blood_sugar)
            FROM user_info
            WHERE DATE(data_time) = ?
        ''', (date_str,))
        result = self.cursor.fetchone()
        return round(result[0], 2) if result[0] is not None else None

    def get_total_carbs_for_date(self, date_str):
        self.cursor.execute('''
            SELECT SUM(carbs)
            FROM user_info
            WHERE DATE(data_time) = ?
        ''', (date_str,))
        result = self.cursor.fetchone()
        return result[0] if result[0] is not None else None

    def close(self):
        self.conn.close()


class DiabetesManager(MDApp):
    icon_color = ColorProperty([0.5, 0.5, 0.5, 1])
    current_time = StringProperty()
    fasting_state = None
    dropdown_menu = None

    def on_start(self):
        async def set_panel_list():
            for i in range(12):
                await asynckivy.sleep(0)
                self.root.ids.container.add_widget(ExpansionPanelItem())

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        Clock.schedule_interval(self.update_time, 3)
        Clock.schedule_once(self.update_today_data, 0)
        Clock.schedule_once(self.update_blood_sugar_stats, 0)
        DBManager.__init__(self)
        Builder.load_file('home_screen.kv')
        Builder.load_file('history_screen.kv')
        Builder.load_file('export_screen.kv')
        Builder.load_file('user_input_screen.kv')
        Builder.load_file('ai_screen.kv')
        return Builder.load_string(home_page_helper)

    def tap_expansion_chevron(
            self, panel: MDExpansionPanel, chevron: TrailingPressedIconButton
    ):
        Animation(
            padding=[0, dp(12), 0, dp(12)]
            if not panel.is_open
            else [0, 0, 0, 0],
            d=0.2,
        ).start(panel)
        panel.open() if not panel.is_open else panel.close()
        panel.set_chevron_down(
            chevron
        ) if not panel.is_open else panel.set_chevron_up(chevron)

    def update_fasting_state(self, instance, state):
        self.fasting_state = 1 if state == "Fasting" else 0

    def add_back_button(self):
        back_button = self.root.ids.back_button

        back_button.opacity = 1
        back_button.disabled = False

    def update_today_data(self, *args):
        db_manager = DBManager()
        today_avg_blood_sugar = db_manager.get_today_average_blood_sugar()
        today_total_carbs = db_manager.get_today_total_carbs()
        db_manager.close()

        home_screen = self.root.ids.screen_manager.get_screen('home_screen')
        home_screen.ids.today_blood_sugar.text = str(
            round(today_avg_blood_sugar)) if today_avg_blood_sugar is not None else "N/A"
        home_screen.ids.today_carbs.text = str(today_total_carbs) if today_total_carbs is not None else "N/A"

    def save_user_data(self):
        data_time = self.current_time
        current_screen = self.root.ids.screen_manager.current_screen
        blood_sugar = current_screen.ids.blood_sugar_input.text if current_screen.ids.blood_sugar_input.text.strip() != '' else None
        carbs = current_screen.ids.carbs.text if current_screen.ids.carbs.text.strip() != '' else None
        meal_description = current_screen.ids.meal_description.text if current_screen.ids.meal_description.text.strip() != '' else None
        fasting = self.fasting_state

        if isinstance(data_time, str):
            try:
                data_time = datetime.strptime(data_time, "%I:%M %p %m/%d/%y")
            except ValueError:
                logging.error("Incorrect current_time format, should be I:M P MM/DD/YY")
                return

        db_manager = DBManager()
        db_manager.add_user_data(data_time, blood_sugar, carbs, fasting, meal_description)
        db_manager.close()

        self.update_blood_sugar_stats()

        self.update_today_data()

        self.root.ids.screen_manager.current = 'home_screen'
    def remove_back_button(self):
        back_button = self.root.ids.back_button

        back_button.opacity = 0
        back_button.disabled = True

    def navigate_to_screen(self, instance=None):
        self.root.ids.screen_manager.current = 'home_screen'

    def update_time(self, *args):
        self.current_time = datetime.now().strftime("%I:%M %p %m/%d/%y")
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

    def switch_to_tab(self, screen_name):
        # Set the current screen in the ScreenManager
        self.root.ids.screen_manager.current = screen_name

    def on_switch_tabs(self, bar, item, item_icon, item_text):
        screen_map = {
            "Home": "home_screen",
            "History": "history_screen",
            "AI Helper": "ai_screen",
            "Export": "export_screen"
        }
        new_screen_name = screen_map.get(item_text)
        if new_screen_name:
            self.root.ids.screen_manager.current = new_screen_name


if __name__ == '__main__':
    DiabetesManager().run()
