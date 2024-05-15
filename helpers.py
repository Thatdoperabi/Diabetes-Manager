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
                    
                    
                    MDCard:
                        style: "elevated"
                        pos_hint: {"center_x": .5, "center_y": .85}
                        padding: "8dp"  # Adjust padding if necessary
                        padding: "8dp"
                        size_hint: None, None
                        size: "280dp", "100dp"  # Adjusted the size to provide more space
                        md_bg_color_disabled: "grey"
                        theme_shadow_offset: "Custom"
                        shadow_offset: (1, -2)
                        theme_shadow_softness: "Custom"
                        shadow_softness: 1
                        theme_elevation_level: "Custom"
                        elevation_level: 2
                        
                        BoxLayout:
                            orientation: 'vertical'  # Confirming horizontal orientation
                            size_hint_x: 1  # Use full width of the MDCard
                            
                            BoxLayout:
                                size_hint_y: 0.5
                                MDLabel:
                                    text: "Est. A1C"
                                    halign: 'left'
                                    size_hint_x: None
                                    valign: 'middle'
                                    width: dp(80)
                                    
                                    
                                MDLabel:
                                    id: a1c_value
                                    text: "7.2%"  # Example A1C value
                                    halign: 'left'
                                    theme_text_color: "Custom"
                                    text_color: [0, 1, 0, 1] if 7.2 < 7.0 else [1, 0, 0, 1]
                                    size_hint_x: None
                                    text_size: self.size
                                    valign: 'middle'
                                    width: dp(50)
                                Widget:
                                    size_hint_x: None
                                    width: dp(20)  # This widget acts as a spacer
                                MDLabel:
                                    text: "Last 30 days"
                                    halign: 'right'
                                    size_hint_x: None
                                    text_size: self.size
                                    valign: 'middle'
                                    width: dp(100)
                            MDDivider:
                                size_hint_y: None  # Important to set to None to not stretch
                                height: dp(2)  # Set the height of the divider
                                pos_hint: {'center_x': 0.5}
                            Widget:
                                size_hint_y: 0.5
                    
                    MDCard:
                        style: "elevated"
                        pos_hint: {"center_x": .5, "center_y": .47}
                        padding: "4dp"
                        size_hint: None, None
                        size: "240dp", "180dp"
                        md_bg_color_disabled: "grey"
                        theme_shadow_offset: "Custom"
                        shadow_offset: (1, -2)
                        theme_shadow_softness: "Custom"
                        shadow_softness: 1
                        theme_elevation_level: "Custom"
                        elevation_level: 2

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
                                    text: app.current_time
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
                                        on_release: app.update_fasting_state(self, 'Post-meal')
                                        MDSegmentButtonLabel:
                                            text: "Post-meal"
                                            font_size: '12sp'
                                    MDSegmentedButtonItem:
                                        size_hint_x: None
                                        width: dp(130)
                                        on_release: app.update_fasting_state(self, 'Fasting')
                                        MDSegmentButtonLabel:
                                            text: "Fasting"
                                            font_size: '12sp'
                                        

                            BoxLayout:
                                orientation: 'vertical'
                                spacing: dp(70)
                                padding: (0, 70, 0, 40)
                                
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
                                on_release: app.save_user_data()
                            
                                MDButtonText:
                                    text: "Save"
                                    theme_text_color: "Custom"
                                    text_color: "purple"
                                
                    TabbedPanelItem:
                        text: 'Carbs'
                        BoxLayout:
                            orientation: 'vertical'
                            padding: dp(20)
                            spacing: dp(30)

                            BoxLayout:
                                orientation: 'horizontal'
                                size_hint_y: None
                                height: dp(48)

                                MDLabel:
                                    text: "Time:"
                                    size_hint_x: 0.2
                                    halign: 'left'
                                    valign: 'center'

                                MDTextField:
                                    mode: "filled"
                                    hint_text: "Enter your name"
                                    id: sugar_time
                                    text: app.current_time
                                    halign: 'right'
                                    size_hint_x: 0.4
                            BoxLayout:
                                orientation: 'vertical'
                                spacing: dp(30)
                                padding: (0, 0, 0, 100)
    
                                BoxLayout:
                                    orientation: 'horizontal'
                                    size_hint_y: None
                                    height: dp(48)
    
                                    MDLabel:
                                        text: "Carbs:"
                                        size_hint_x: 0.3
                                        halign: 'left'
                                        valign: 'center'
                                            
                                    MDTextField:
                                        mode: "filled"
                                        id: carbs
                                        halign: 'right'
                                        size_hint_x: 0.12
                                        
                            BoxLayout:
                                orientation: 'vertical'
                                spacing: dp(30)
                                padding: (0, 0, 0, 40)
    
                                BoxLayout:
                                    orientation: 'horizontal'
                                    size_hint_y: None
                                    height: dp(48)
    
                                    MDLabel:
                                        text: "Meal Description:"
                                        size_hint_x: 0.2
                                        halign: 'left'
                                        valign: 'center'
    
                                    MDTextField:
                                        mode: "filled"
                                        id: meal_description
                                        halign: 'right'
                                        size_hint_x: 0.4
                            
                                Widget:
                                    size_hint_y: .05
                                    
                                MDButton:
                                    height: dp(48)
                                    pos_hint: {'center_x': .5}
                                    style: "elevated"
                                    theme_shadow_color: "Custom"
                                    shadow_color: "purple"
                                    on_release: app.save_user_data()
                                
                                    MDButtonText:
                                        text: "Save"
                                        theme_text_color: "Custom"
                                        text_color: "purple"
                    TabbedPanelItem:
                        text: 'Both'
                        ScrollView:
                            do_scroll_x: False
                            do_scroll_y: True
                            BoxLayout:
                                orientation: 'vertical'
                                padding: dp(20)
                                spacing: dp(30)
                                size_hint_y: None
                                height: dp(420)
    
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
                                        text: app.current_time
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
                                            on_release: app.update_fasting_state(self, 'Post-meal')
                                            MDSegmentButtonLabel:
                                                text: "Post-meal"
                                                font_size: '12sp'
                                        MDSegmentedButtonItem:
                                            size_hint_x: None
                                            width: dp(130)
                                            on_release: app.update_fasting_state(self, 'Fasting')
                                            MDSegmentButtonLabel:
                                                text: "Fasting"
                                                font_size: '12sp'
                                            
    
                                BoxLayout:
                                    orientation: 'vertical'
                                    
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
                                            
                                BoxLayout:
                                    orientation: 'vertical'
                                    spacing: dp(30)
                                    padding: (0, 70, 0, 0)
                                    
                                    BoxLayout:
                                        orientation: 'horizontal'
                                        size_hint_y: None
                                        height: dp(48)
                                        
                                        MDLabel:
                                            text: "Carbs:"
                                            size_hint_x: 0.3
                                            halign: 'left'
                                            valign: 'center'   
                                            
                                        MDTextField:
                                            mode: "filled"
                                            id: carbs
                                            halign: 'right'
                                            size_hint_x: 0.12
                                
                                BoxLayout:
                                    orientation: 'vertical'
                                    spacing: dp(30)
                                    padding: (0, 70, 0, 0)
                                    
                                    BoxLayout:
                                        orientation: 'horizontal'
                                        size_hint_y: None
                                        height: dp(48)
                                        
                                        MDLabel:
                                            text: "Meal Description:"
                                            size_hint_x: 0.2
                                            halign: 'left'
                                            valign: 'center'
        
                                        MDTextField:
                                            mode: "filled"
                                            id: meal_description
                                            halign: 'right'
                                            size_hint_x: 0.4
                                                
                            
                                    
                                MDButton:
                                    height: dp(48)
                                    pos_hint: {'center_x': .5}
                                    style: "elevated"
                                    theme_shadow_color: "Custom"
                                    shadow_color: "purple"
                                    on_release: app.save_user_data()
                                
                                    MDButtonText:
                                        text: "Save"
                                        theme_text_color: "Custom"
                                        text_color: "purple"
                            


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