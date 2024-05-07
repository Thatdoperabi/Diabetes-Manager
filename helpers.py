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
            pos_hint: {"center_x": .5, "center_y": .5}
            
            MDTopAppBarLeadingButtonContainer:
                id: leading_container

            MDTopAppBarTitle:
                text: "Diabetes Manager"
                theme_font_size: "Custom"
                font_size: "14dp"


            MDTopAppBarTrailingButtonContainer:
                id: trailing_container
                MDActionTopAppBarButton:
                    icon: "dots-vertical"
                    icon_size: "24dp"


    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: self.theme_cls.backgroundColor
        size_hint_y: 1.5

        MDScreenManager:
            id: screen_manager

            BaseScreen:
                name: "Screen 1"
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
                        on_release: screen_manager.current = "Screen 5"


            BaseScreen:
                name: "Screen 2"

            BaseScreen:
                name: "Screen 3"

            BaseScreen:
                name: "Screen 4"
                
            BaseScreen:
                name: "Screen 5"
                on_enter: app.add_back_button()
                on_leave: app.remove_back_button()
                BoxLayout:
                    orientation: 'vertical'
                    padding: "10dp"
                    spacing: "20dp"
                
                    MDTextField:
                        id: name
                        hint_text: "Enter your name"
                
                    MDTextField:
                        id: email
                        hint_text: "Enter your email"
                
                    MDTextField:
                        id: phone
                        hint_text: "Enter your phone number"
                
                    MDButton:
                        text: "Submit"
                        pos_hint: {'center_x': 0.5}
                        on_release: app.submit_form()


        MDNavigationBar:
            height: "40dp"

            BaseMDNavigationItem:
                icon: "gmail"
                text: "Screen 1"
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