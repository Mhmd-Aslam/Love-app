from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.graphics import Color, RoundedRectangle
from random import choice

# Set mobile-friendly dimensions
Window.size = (360, 640)  # Standard mobile size

class RoundedButton(Button):
    """Button with rounded corners and visible colors"""
    border_radius = ListProperty([70])  # This makes it a valid Kivy property
    
    def __init__(self, **kwargs):
        # Get button_color from kwargs or use default
        self.button_color = kwargs.pop('button_color', (0.9, 0.3, 0.5, 1))
        
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # Make background transparent
        
        # Initial draw
        self.draw_button()
        
        # Bind properties to update the button
        self.bind(pos=self.draw_button, size=self.draw_button, border_radius=self.draw_button)
        
    def draw_button(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.button_color)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.border_radius
            )

class GrowingButton(RoundedButton):
    """Button that scales its text with size and has rounded corners"""
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
    original_yes_size = (0.43, 0.6)  # Store original size
    original_yes_pos = {'center_x': 0.27, 'center_y': 0.5}  # Store original position
    
    # Custom expansion factors for each edge (left, right, top, bottom)
    # These values determine how much each edge expands relative to others
    expand_factors = {
        'left': 0.2,    # 30% of growth goes to left
        'right': 0.5,   # 70% of growth goes to right
        'top': 5,     # 50% of growth goes to top
        'bottom': 1   # 50% of growth goes to bottom
    }
    
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
            text="Yes!",
            font_size="24sp",
            button_color=(0.9, 0.3, 0.5, 1),  # Pink color
            color=(1, 1, 1, 1),  # White text
            size_hint=self.original_yes_size,
            pos_hint=self.original_yes_pos,
            bold=True)
        self.yes_button.bind(on_press=self.say_yes)
        self.button_box.add_widget(self.yes_button)
        
        # "No" Button
        self.no_button = RoundedButton(
            text="No",
            font_size="24sp",
            button_color=(0.7, 0.5, 0.7, 1),  # Purple color
            color=(1, 1, 1, 1),  # White text
            size_hint=(0.43, 0.6),
            pos_hint={'center_x': 0.73, 'center_y': 0.5},
            bold=True)
        self.no_button.bind(on_press=self.on_no_press)
        self.button_box.add_widget(self.no_button)
        
        # Add all components to main layout
        self.layout.add_widget(self.content)
        self.layout.add_widget(self.button_box)
        
        return self.layout
    
    def show_fullscreen_love(self):
        # Create fullscreen love message
        self.love_button = RoundedButton(
            text="I LOVE YOU! ❤️",
            font_size=48,
            button_color=(1, 0.2, 0.4, 1),  # Romantic red
            color=(1, 1, 1, 1),  # White text
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},
            bold=True)
        self.love_button.border_radius = [0]  # No rounding for fullscreen
        
        # Clear current layout and show fullscreen message
        self.layout.clear_widgets()
        self.layout.add_widget(self.love_button)
        
        # Add pulse animation to fullscreen message
        anim = (Animation(font_size=52, duration=0.8) + 
               Animation(font_size=48, duration=0.8))
        anim.repeat = True
        anim.start(self.love_button)
    
    def say_yes(self, instance):
        # Immediately show fullscreen love message
        self.show_fullscreen_love()
    
    def on_no_press(self, instance):
        # Calculate growth amount (20% of original size)
        growth_amount = (self.original_yes_size[0] * 0.2, self.original_yes_size[1] * 0.2)
        
        # Calculate new size (capped at 100%)
        new_width = min(1.0, self.yes_button.size_hint[0] + growth_amount[0])
        new_height = min(1.0, self.yes_button.size_hint[1] + growth_amount[1])
        
        # Calculate new position based on expansion factors
        width_growth = new_width - self.yes_button.size_hint[0]
        height_growth = new_height - self.yes_button.size_hint[1]
        
        # Calculate new position (expanding according to factors)
        new_pos = {
            'center_x': self.original_yes_pos['center_x'] - (width_growth * (self.expand_factors['left'] - self.expand_factors['right'])/2),
            'center_y': self.original_yes_pos['center_y'] + (height_growth * (self.expand_factors['top'] - self.expand_factors['bottom'])/2)
        }
        
        # Animate the expansion
        anim = Animation(
            size_hint=(new_width, new_height),
            pos_hint=new_pos,
            duration=0.4,
            t='in_out_quad'
        )
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
                "No ", "Try again", "Not today", 
                "Maybe?", "Click Yes!", "Nope!",
                "I'm shy", "Later?", "Can't decide",
                "You wish!", "Not sure", "Think again"
            ]
            self.no_button.text = choice(playful_texts)
        
        # Check if we should show fullscreen
        if new_width >= 1.0 or new_height >= 1.0:
            self.show_fullscreen_love()

if __name__ == '__main__':
    LoveApp().run()