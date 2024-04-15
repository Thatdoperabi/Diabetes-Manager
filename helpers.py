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

    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: self.theme_cls.backgroundColor
        size_hint_y: 1

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
                        on_release: app.open_menu()

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
"""