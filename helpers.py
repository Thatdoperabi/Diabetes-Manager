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
                md_bg_color: self.theme_cls.backgroundColor
                on_enter: app.add_back_button()
                on_leave: app.remove_back_button()
                TabbedPanel:
                    do_default_tab: False
                    TabbedPanelItem:
                        text: 'Sugar'
                        BoxLayout:
                            orientation: 'vertical'
                            padding: dp(20)
                            spacing: dp(30)

                            BoxLayout:
                                orientation: 'horizontal'
                                size_hint_y: None
                                height: dp(48)
                                pos_hint: {'top': 1}

                                MDLabel:
                                    text: "Time:"
                                    size_hint_x: 0.2
                                    halign: 'left'
                                    valign: 'center'

                                MDTextField:
                                    mode: "filled"
                                    hint_text: "Enter your name"
                                    id: sugar_time
                                    halign: 'right'
                                    size_hint_x: 0.4
                                
                            BoxLayout:
                                orientation: 'horizontal'
                                size_hint_y: None
                                height: dp(24)
                                
                                MDSegmentedButton:
                                    id: meal_toggle
                                    size_hint_x: 0.5
                                    MDBoxLayout:
                                        orientation: 'horizontal'
                                        padding: [dp(5), 0]
                                    MDSegmentedButtonItem:
                                        size_hint_x: None
                                        width: dp(130)
                                        MDSegmentButtonLabel:
                                            text: "Post-meal"
                                            font_size: '12sp'
                                    MDSegmentedButtonItem:
                                        size_hint_x: None
                                        width: dp(130)
                                        MDSegmentButtonLabel:
                                            text: "Fasting"
                                            font_size: '12sp'
                                        

                            BoxLayout:
                                orientation: 'vertical'
                                spacing: dp(30)
                                padding: (0, 0, 0, 40)
                                
                                BoxLayout:
                                    orientation: 'horizontal'
                                    size_hint_y: None
                                    height: dp(48)

                                    MDLabel:
                                        text: "Blood Sugar:"
                                        size_hint_x: 0.3
                                        halign: 'left'
                                        valign: 'center'
                                        
                                    MDIcon:
                                        padding: (0, 0, 20, 0)
                                        id: sugar_level_indicator
                                        icon: "circle"
                                        size: dp(24), dp(24)
                                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                        theme_icon_color: "Custom"
                                        color: 0, 1, 0, 1  # Green by default  
                                          
                                    MDTextField:
                                        id: blood_sugar_input
                                        mode: "filled"
                                        hint_text: "Enter blood sugar level"
                                        halign: 'right'
                                        size_hint_x: 0.12
                                        on_text: app.update_sugar_level_indicator(self.text)
                        
                            Widget:
                                size_hint_y: .05
                                
                            MDButton:
                                height: dp(48)
                                pos_hint: {'center_x': .5}
                                style: "elevated"
                                theme_shadow_color: "Custom"
                                shadow_color: "purple"
                            
                                MDButtonText:
                                    text: "Save"
                                    theme_text_color: "Custom"
                                    text_color: "purple"
                                
                    TabbedPanelItem:
                        text: 'Carbs'
                        BoxLayout:
                            orientation: 'vertical'
                            Label:
                                text: 'Content for Carbs'
                    TabbedPanelItem:
                        text: 'Both'
                        BoxLayout:
                            orientation: 'vertical'
                            Label:
                                text: 'Content for Both'
                            


        MDNavigationBar:
            on_switch_tabs: app.on_switch_tabs(*args)
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