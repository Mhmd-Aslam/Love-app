from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from random import uniform

class LoveApp(App):
    def build(self):
        # Set background color (light pink)
        Window.clearcolor = (1, 0.8, 0.86, 1)  # RGBA

        # Main layout (vertical)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=30)

        # Cute heart image (auto-scaled)
        layout.add_widget(Image(source="heart.png", size_hint=(1, 0.25)))

        # Romantic message
        self.label = Label(text="Will you go on a date with me? ❤️",
                           font_size="22sp",
                           bold=True,
                           color=(1, 0, 0.5, 1))  # Dark pink
        layout.add_widget(self.label)

        # "Yes" Button (small but visible)
        yes_button = Button(text="Yes! 💖",
                            font_size="18sp",
                            background_color=(1, 0.5, 0.7, 1),  # Soft pink
                            color=(1, 1, 1, 1),  # White text
                            size_hint=(0.2, 0.1))  # Scales with screen
        yes_button.bind(on_press=self.say_yes)

        # "No" Button (moves away)
        self.no_button = Button(text="No 😜",
                                font_size="18sp",
                                background_color=(0.9, 0.4, 0.6, 1),
                                color=(1, 1, 1, 1),
                                size_hint=(0.2, 0.1))  # Scales with screen
        self.no_button.bind(on_touch_down=self.move_no_button)

        # Add buttons to layout
        layout.add_widget(yes_button)
        layout.add_widget(self.no_button)

        return layout

    def say_yes(self, instance):
        self.label.text = "Yay! Can't wait for our date! 🥰"
        self.label.color = (1, 0, 0, 1)  # Change text color to red

    def move_no_button(self, instance, touch):
        if self.no_button.collide_point(*touch.pos):
            # Move the "No" button randomly but keep it visible
            self.no_button.pos_hint = {
                "x": uniform(0, 0.7),  # Adjusted for different screens
                "y": uniform(0, 0.7)
            }

LoveApp().run()
