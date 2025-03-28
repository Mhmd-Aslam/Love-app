from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty
from random import choice

# Set mobile-friendly dimensions
Window.size = (360, 640)  # Standard mobile size

class LoveApp(App):
    message = StringProperty("Will you go on a date with me? ❤️")
    yes_scale = NumericProperty(1.0)  # Scale factor for Yes button
    
    def build(self):
        # Romantic background
        Window.clearcolor = (0.98, 0.85, 0.9, 1)
        
        # Main layout using FloatLayout for absolute positioning
        self.layout = FloatLayout()
        
        # Content container
        self.content = FloatLayout(size_hint=(1, 1))
        
        # Heart image
        self.heart = Image(
            source="logos/heart.png",
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.content.add_widget(self.heart)
        
        # Romantic message
        self.label = Label(
            text=self.message,
            font_size="28sp",
            bold=True,
            color=(0.8, 0.2, 0.4, 1),
            outline_color=(1, 1, 1, 0.8),
            outline_width=2,
            size_hint=(0.9, None),
            pos_hint={'center_x': 0.5, 'top': 0.5},
            halign='center')
        self.content.add_widget(self.label)
        
        # Button container
        self.button_box = FloatLayout(size_hint=(1, 0.3), pos_hint={'bottom': 1})
        
        # "Yes" Button
        self.yes_button = Button(
            text="Yes! 💖",
            font_size="24sp",
            background_color=(0.9, 0.3, 0.5, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.45, 0.8),
            pos_hint={'center_x': 0.3, 'center_y': 0.5},
            background_normal='',
            bold=True,
            border=(10, 10, 10, 10))
        self.yes_button.bind(on_press=self.say_yes)
        self.button_box.add_widget(self.yes_button)
        
        # "No" Button
        self.no_button = Button(
            text="No 😜",
            font_size="24sp",
            background_color=(0.7, 0.5, 0.7, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.45, 0.8),
            pos_hint={'center_x': 0.7, 'center_y': 0.5},
            background_normal='',
            bold=True,
            border=(10, 10, 10, 10))
        self.no_button.bind(on_press=self.on_no_press)
        self.button_box.add_widget(self.no_button)
        
        # Add all components to main layout
        self.layout.add_widget(self.content)
        self.layout.add_widget(self.button_box)
        
        return self.layout
    
    def say_yes(self, instance):
        # Celebration message
        self.message = "Yay! I'm so happy! 🥰💕"
        
        # Change button colors
        self.yes_button.background_color = (0.2, 0.8, 0.3, 1)  # Green
        self.no_button.background_color = (0.9, 0.2, 0.2, 1)   # Red
        
        # Heart animation
        anim = Animation(size_hint=(0.45, 0.45), duration=0.2) + \
               Animation(size_hint=(0.4, 0.4), duration=0.2)
        anim.start(self.heart)
    
    def on_no_press(self, instance):
        # Grow Yes button exponentially
        self.yes_scale *= 1.2  # 20% growth per click
        
        # Animate the expansion
        anim = Animation(
            size_hint=(self.yes_scale, self.yes_scale),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            duration=0.3,
            t='in_out_quad'
        )
        anim.bind(on_complete=self.check_fullscreen)
        anim.start(self.yes_button)
        
        # Shrink No button
        anim = Animation(
            size_hint=(max(0, self.no_button.size_hint[0] - 0.1), 
                      max(0, self.no_button.size_hint[1] - 0.1)),
            duration=0.3
        )
        anim.start(self.no_button)
        
        # Change No button text if visible
        if self.no_button.size_hint[0] > 0.1:
            playful_texts = [
                "No 😜", "Try again", "Not today", 
                "Maybe?", "Click Yes!", "Nope!",
                "I'm shy", "Later?", "Can't decide",
                "You wish!", "Not sure", "Think again"
            ]
            self.no_button.text = choice(playful_texts)
    
    def check_fullscreen(self, *args):
        # If Yes button covers most of the screen
        if self.yes_scale > 2.5:
            # Move to top layer and cover everything
            self.button_box.remove_widget(self.yes_button)
            self.layout.remove_widget(self.content)
            self.layout.remove_widget(self.button_box)
            self.layout.add_widget(self.yes_button)
            
            # Final fullscreen appearance
            self.yes_button.size_hint = (1, 1)
            self.yes_button.pos_hint = {'x': 0, 'y': 0}
            self.yes_button.text = "I LOVE YOU! ❤️"
            self.yes_button.font_size = "32sp"
            self.yes_button.background_color = (1, 0.2, 0.4, 1)  # Romantic red

if __name__ == '__main__':
    LoveApp().run()