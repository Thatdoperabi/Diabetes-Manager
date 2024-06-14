#:include 'home_screen.kv'
#:include 'user_input_screen.kv'

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
        orientation: 'horizontal'
        md_bg_color: self.theme_cls.backgroundColor
        size_hint_y: .18
        height: "40dp"

        MDTopAppBar:
            id: top_app_bar
            type: "small"
            size_hint_x: 1
            size_hint_y: None
            height: "40dp"
            # pos_hint: {"center_x": .5, "center_y": .5}

            MDTopAppBarLeadingButtonContainer:
                id: leading_container

            MDTopAppBarTitle:
                text: "Diabetes Manager"
                theme_font_size: "Custom"
                font_size: "14dp"
                halign: "left"
                
            MDTopAppBarTrailingButtonContainer:
                id: trailing_container
                MDActionTopAppBarButton:
                    icon: "dots-vertical"
                    icon_size: "24dp"
                    pos_hint: {"center_y": .5}


    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: self.theme_cls.backgroundColor
        size_hint_y: 1.5

        MDScreenManager:
            id: screen_manager

            HomeScreen:
                name: "home_screen"

            BaseScreen:
                name: "Screen 2"

            BaseScreen:
                name: "Screen 3"

            BaseScreen:
                name: "Screen 4"

            UserInputScreen:
                name: "user_input_screen"
                md_bg_color: self.theme_cls.backgroundColor
                on_enter: app.add_back_button()
                on_leave: app.remove_back_button()

        MDNavigationBar:
            on_switch_tabs: app.on_switch_tabs(*args)
            height: "40dp"

            BaseMDNavigationItem:
                icon: "gmail"
                text: "Home"
                active: True
                font_size: "12dp"  # Smaller font size for navigation text
                icon_size: "24dp"  # Smaller icon size

            BaseMDNavigationItem:
                icon: "twitter"
                text: "Screen 2"
                font_size: "12dp"
                icon_size: "24dp"

            BaseMDNavigationItem:
                icon: "linkedin"
                text: "Screen 3"
                font_size: "12dp"
                icon_size: "24dp"

            BaseMDNavigationItem:
                icon: "linkedin"
                text: "Screen 4"
                font_size: "12dp"
                icon_size: "24dp"
"""
