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

class GrowingButton(Button):
    """Button that scales its text with its size"""
    def __init__(self, **kwargs):
        # Get font_size from kwargs if specified
        font_size = kwargs.pop('font_size', '24sp')
        if isinstance(font_size, str):
            self.base_font_size = float(font_size[:-2])  # Remove 'sp' suffix
        else:
            self.base_font_size = float(font_size)
        
        super().__init__(**kwargs)
        self.font_size = font_size  # Set the initial font size
        
    def on_size(self, instance, size):
        # Scale font size proportionally to button size
        scale_factor = min(size[0]/self.width, size[1]/self.height)
        new_size = max(self.base_font_size, self.base_font_size * scale_factor * 1.5)
        self.font_size = f"{new_size}sp"

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
        
        # "Yes" Button (using our custom GrowingButton)
        self.yes_button = GrowingButton(
            text="Yes! 💖",
            font_size="24sp",  # Pass as string
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
    
    def show_fullscreen_love(self):
        # Create fullscreen love message
        self.love_button = Button(
            text="I LOVE YOU! ❤️",
            font_size=48,  # Using numeric value here
            background_color=(1, 0.2, 0.4, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},
            background_normal='',
            bold=True)
        
        # Clear current layout and show fullscreen message
        self.layout.clear_widgets()
        self.layout.add_widget(self.love_button)
        
        # Add pulse animation to fullscreen message using numeric values
        anim = (Animation(font_size=52, duration=0.8) + 
               Animation(font_size=48, duration=0.8))
        anim.repeat = True
        anim.start(self.love_button)
    
    def say_yes(self, instance):
        # Immediately show fullscreen love message
        self.show_fullscreen_love()
    
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
        # If Yes button covers most of the screen through No clicks
        if self.yes_scale > 2.5:
            self.show_fullscreen_love()

if __name__ == '__main__':
    LoveApp().run()