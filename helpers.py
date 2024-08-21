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

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: "60dp"
            padding: [dp(5), dp(0), dp(5), dp(5)]  # Remove top padding, add bottom padding
            spacing: "10dp"

            # First item
            NavigationItem:
                orientation: 'vertical'
                size_hint: 1, None
                screen_name: 'home_screen'
                
                Widget:
                    size_hint_y: None
                    height: dp(5)

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)

                    Widget:
                        size_hint_x: 1

                    MDIconButton:
                        icon: "home"
                        size_hint: None, None
                        size: "24dp", "24dp"
                        valign: "center"
                        halign: "center"

                    Widget:
                        size_hint_x: 1

                MDLabel:
                    text: "Home"
                    halign: "center"
                    size_hint_y: None
                    height: "20dp"
                    font_size: "12sp"

            # Second item
            NavigationItem:
                orientation: 'vertical'
                size_hint: 1, None
                screen_name: 'history_screen'
                
                
                Widget:
                    size_hint_y: None
                    height: dp(5)

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)

                    Widget:
                        size_hint_x: 1

                    MDIconButton:
                        icon: "history"
                        size_hint: None, None
                        size: "24dp", "24dp"
                        valign: "center"
                        halign: "center"

                    Widget:
                        size_hint_x: 1

                MDLabel:
                    text: "History"
                    halign: "center"
                    size_hint_y: None
                    height: "20dp"
                    font_size: "12sp"

            # Third item
            NavigationItem:
                orientation: 'vertical'
                size_hint: 1, None
                on_touch_down:
                screen_name: 'ai_screen'
                
                Widget:
                    size_hint_y: None
                    height: dp(5)

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)

                    Widget:
                        size_hint_x: 1

                    MDIconButton:
                        icon: "comment"
                        size_hint: None, None
                        size: "24dp", "24dp"
                        valign: "center"
                        halign: "center"

                    Widget:
                        size_hint_x: 1

                MDLabel:
                    text: "AI Helper"
                    halign: "center"
                    size_hint_y: None
                    height: "20dp"
                    font_size: "12sp"

            # Fourth item
            NavigationItem:
                orientation: 'vertical'
                size_hint: 1, None
                screen_name: 'export_screen'
                
                Widget:
                    size_hint_y: None
                    height: dp(5)

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(30)

                    Widget:
                        size_hint_x: 1

                    MDIconButton:
                        icon: "file-export"
                        size_hint: None, None
                        size: "24dp", "24dp"
                        valign: "center"
                        halign: "center"

                    Widget:
                        size_hint_x: 1

                MDLabel:
                    text: "Export"
                    halign: "center"
                    size_hint_y: None
                    height: "20dp"
                    font_size: "12sp"
"""
