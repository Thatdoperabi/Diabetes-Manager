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
        id: top_app_bar_layout
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
            opacity: 0
            disabled: True
            size_hint_x: None

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
            padding: [dp(5), dp(0), dp(5), dp(5)]
            spacing: "10dp"

            # Home
            BoxLayout:
                orientation: 'vertical'
                size_hint: None, None
                width: dp(60)
                height: "60dp"

                Widget:
                    size_hint_y: 1

                MDIconButton:
                    icon: "home"
                    size_hint: None, None
                    size: "40dp", "40dp"
                    pos_hint: {"center_x": .5}
                    on_release: app.root.ids.screen_manager.current = 'home_screen'

                MDLabel:
                    text: "Home"
                    halign: "center"
                    size_hint_y: None
                    height: "20dp"
                    font_size: "12sp"
                    pos_hint: {"center_x": .5}

                Widget:
                    size_hint_y: 1

            # History
            BoxLayout:
                orientation: 'vertical'
                size_hint: None, None
                width: dp(60)
                height: "60dp"

                Widget:
                    size_hint_y: 1

                MDIconButton:
                    icon: "history"
                    size_hint: None, None
                    size: "40dp", "40dp"
                    pos_hint: {"center_x": .5}
                    on_release: app.root.ids.screen_manager.current = 'history_screen'

                MDLabel:
                    text: "History"
                    halign: "center"
                    size_hint_y: None
                    height: "20dp"
                    font_size: "12sp"
                    pos_hint: {"center_x": .5}

                Widget:
                    size_hint_y: 1

            # AI Helper
            BoxLayout:
                orientation: 'vertical'
                size_hint: None, None
                width: dp(60)
                height: "60dp"

                Widget:
                    size_hint_y: 1

                MDIconButton:
                    icon: "comment"
                    size_hint: None, None
                    size: "40dp", "40dp"
                    pos_hint: {"center_x": .5}
                    on_release: app.root.ids.screen_manager.current = 'ai_screen'

                MDLabel:
                    text: "AI Helper"
                    halign: "center"
                    size_hint_y: None
                    height: "20dp"
                    font_size: "12sp"
                    pos_hint: {"center_x": .5}

                Widget:
                    size_hint_y: 1

            # Export
            BoxLayout:
                orientation: 'vertical'
                size_hint: None, None
                width: dp(60)
                height: "60dp"

                Widget:
                    size_hint_y: 1

                MDIconButton:
                    icon: "file-export"
                    size_hint: None, None
                    size: "40dp", "40dp"
                    pos_hint: {"center_x": .5}
                    on_release: app.root.ids.screen_manager.current = 'export_screen'

                MDLabel:
                    text: "Export"
                    halign: "center"
                    size_hint_y: None
                    height: "20dp"
                    font_size: "12sp"
                    pos_hint: {"center_x": .5}

                Widget:
                    size_hint_y: 1
"""
