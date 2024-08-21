#:include 'home_screen.kv'
#:include 'user_input_screen.kv'
#:include 'ai_screen.kv'
#:include 'history_screen.kv'

home_page_helper = """
<BaseMDNavigationItem>
    MDNavigationItemIcon:
        icon: root.icon

    MDNavigationItemLabel:
        text: root.text


<BaseScreen>

BoxLayout:
    orientation: "vertical"

    MDBoxLayout:
        id: top_app_bar_layout  # Ensure this ID matches the one in your Python code
        orientation: 'horizontal'
        size_hint_y: .18
        height: "40dp"
        padding: [dp(15), 0, dp(15), 0]

        MDIconButton:
            id: back_button
            icon: "arrow-left"
            size_hint: None, None
            size: "48dp", "48dp"
            pos_hint: {'center_y': 0.5}
            on_release: app.navigate_to_screen()
            opacity: 0  # Initially hidden
            disabled: True  # Initially disabled
            size_hint_x: None  # Prevents taking up space when hidden

        Label:
            text: "Diabetes Manager"
            font_size: "14dp"
            halign: "left"
            valign: "center"
            size_hint_x: None
            width: self.texture_size[0]

        Widget:
            size_hint_x: 1  # Filler to push icons to the right

        MDIconButton:
            icon: "dots-vertical"
            size_hint_x: None
            size_hint_y: None
            width: "40dp"
            height: "40dp"
            pos_hint: {"center_y": .5}



    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: self.theme_cls.backgroundColor
        size_hint_y: 1.5

        MDScreenManager:
            id: screen_manager

            HomeScreen:
                name: "home_screen"

            HistoryScreen:
                name: "history_screen"

            AiScreen:
                name: "ai_screen"

            ExportScreen:
                name: "export_screen"

            UserInputScreen:
                name: "user_input_screen"
                md_bg_color: self.theme_cls.backgroundColor
                on_enter: app.add_back_button()
                on_leave: app.remove_back_button()

        MDNavigationBar:
            on_switch_tabs: app.on_switch_tabs(*args)
            height: "40dp"

            BaseMDNavigationItem:
                icon: "home"
                text: "Home"
                active: True
                font_size: "12dp"  # Smaller font size for navigation text
                icon_size: "24dp"  # Smaller icon size

            BaseMDNavigationItem:
                icon: "history"
                text: "History"
                font_size: "12dp"
                icon_size: "24dp"

            BaseMDNavigationItem:
                icon: "comment"
                text: "AI Helper"
                font_size: "12dp"
                icon_size: "24dp"

            BaseMDNavigationItem:
                icon: "file-export"
                text: "Export"
                font_size: "12dp"
                icon_size: "24dp"
"""
