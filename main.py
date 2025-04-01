from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.graphics import Color, RoundedRectangle
from random import choice
from kivy.clock import Clock

# Set mobile-friendly dimensions
Window.size = (360, 640)  # Standard mobile size

class RoundedButton(Button):
    """Button with rounded corners and visible colors"""
    border_radius = ListProperty([70])
    base_font_size = NumericProperty(24)  # Base font size in pixels
    
    def __init__(self, **kwargs):
        # Get button_color from kwargs or use default
        self.button_color = kwargs.pop('button_color', (0.9, 0.3, 0.5, 1))
        
        # Get font_size if specified (either as '24sp' or 24)
        font_size = kwargs.pop('font_size', '24sp')
        if isinstance(font_size, str):
            self.base_font_size = float(font_size[:-2])  # Remove 'sp' suffix
        else:
            self.base_font_size = float(font_size)
        
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # Make background transparent
        self.font_size = self.base_font_size  # Set initial font size
        
        # Initial draw
        self.draw_button()
        
        # Bind properties to update the button
        self.bind(
            pos=self.draw_button, 
            size=self.draw_button, 
            border_radius=self.draw_button
        )
        
    def draw_button(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.button_color)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.border_radius
            )
    
    def on_size(self, instance, size):
        # Calculate proportional font size based on button height
        scale_factor = size[1] / (Window.height * 0.3 * 0.3)  # Original button height
        new_size = max(12, self.base_font_size * scale_factor)  # Minimum 12px
        self.font_size = new_size

class LoveApp(App):
    message = StringProperty("Will you go on a date with me? ❤️")
    original_yes_size = (0.43, 0.6)  # Store original size
    original_yes_pos = {'center_x': 0.27, 'center_y': 0.5}  # Store original position
    no_button_clicks = 0  # Track number of "No" button clicks
    
    # Custom expansion factors for each edge (left, right, top, bottom)
    expand_factors = {
        'left': 0.1,    # 10% of growth goes to left
        'right': 0.2,   # 20% of growth goes to right
        'top': 12.5,    # 62.5% of growth goes to top
        'bottom': 12    # 37.5% of growth goes to bottom
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
        
        # Romantic message - adjusted to fit screen
        self.label = Label(
            text=self.message,
            font_size="24sp",
            bold=True,
            color=(0.8, 0.2, 0.4, 1),
            outline_color=(1, 1, 1, 0.8),
            outline_width=2,
            size_hint=(0.9, None),
            height=Window.height * 0.15,
            pos_hint={'center_x': 0.5, 'top': 0.55},
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.85, None))
        self.content.add_widget(self.label)
        
        # Button container
        self.button_box = FloatLayout(size_hint=(1, 0.3), pos_hint={'bottom': 1})
        
        # "Yes" Button
        self.yes_button = RoundedButton(
            text="Yes!",
            font_size="24sp",
            button_color=(0.9, 0.3, 0.5, 1),
            color=(1, 1, 1, 1),
            size_hint=self.original_yes_size,
            pos_hint=self.original_yes_pos,
            bold=True)
        self.yes_button.bind(on_press=self.say_yes)
        self.button_box.add_widget(self.yes_button)
        
        # "No" Button
        self.no_button = RoundedButton(
            text="No",
            font_size="24sp",
            button_color=(0.7, 0.5, 0.7, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.43, 0.6),
            pos_hint={'center_x': 0.73, 'center_y': 0.5},
            bold=True)
        self.no_button.bind(on_press=self.on_no_press)
        self.button_box.add_widget(self.no_button)
        
        self.layout.add_widget(self.content)
        self.layout.add_widget(self.button_box)
        
        return self.layout
    
    def show_fullscreen_love(self):
        # Create fullscreen love message
        self.love_button = RoundedButton(
            text="I LOVE YOU! ❤️",
            font_size=48,
            button_color=(1, 0.2, 0.4, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},
            bold=True)
        self.love_button.border_radius = [0]
        
        self.layout.clear_widgets()
        self.layout.add_widget(self.love_button)
        
        anim = (Animation(font_size=52, duration=0.8) + 
               Animation(font_size=48, duration=0.8))
        anim.repeat = True
        anim.start(self.love_button)
    
    def say_yes(self, instance):
        self.show_fullscreen_love()
    
    def on_no_press(self, instance):
        self.no_button_clicks += 1
        
        # Use current size and position as the base for expansion
        current_size = self.yes_button.size_hint
        current_pos = {
            'center_x': self.yes_button.pos_hint['center_x'],
            'center_y': self.yes_button.pos_hint['center_y']
        }
        
        # Calculate growth amount (20% of current size)
        growth_amount = (current_size[0] * 0.2, current_size[1] * 0.2)
        
        # Calculate new size (no upper limit)
        new_width = current_size[0] + growth_amount[0]
        new_height = current_size[1] + growth_amount[1]
        
        # Calculate new position based on expansion factors
        width_growth = new_width - current_size[0]
        height_growth = new_height - current_size[1]
        
        # Calculate new position (expanding according to factors)
        new_pos = {
            'center_x': current_pos['center_x'] - (width_growth * (self.expand_factors['left'] - self.expand_factors['right'])/2),
            'center_y': current_pos['center_y'] + (height_growth * (self.expand_factors['top'] - self.expand_factors['bottom'])/2)
        }
        
        # Animate the expansion
        anim = Animation(
            size_hint=(new_width, new_height),
            pos_hint=new_pos,
            duration=0.4,
            t='in_out_quad'
        )
        anim.start(self.yes_button)
        
        # After 7th click, start moving "No" button to the right
        if self.no_button_clicks >= 7:
            # Get current position
            current_no_pos = self.no_button.pos_hint['center_x']
            
            # Create animation to move right and shrink
            anim = Animation(
                size_hint_x=max(0.1, self.no_button.size_hint[0] - 0.05),
                pos_hint={'center_x': min(1.5, current_no_pos + 0.1), 'center_y': 0.5},
                duration=0.3
            )
            anim.start(self.no_button)
            
            # If button goes off screen, remove it
            if current_no_pos >= 1.3:
                Clock.schedule_once(lambda dt: self.button_box.remove_widget(self.no_button), 0.3)
        else:
            # Normal shrinking behavior for first 6 clicks
            anim = Animation(
                size_hint=(max(0.1, self.no_button.size_hint[0] - 0.1), 
                          max(0.1, self.no_button.size_hint[1] - 0.1)),
                duration=0.3
            )
            anim.start(self.no_button)
        
        # Change No button text
        playful_texts = [
            "No ", "Try again", "Not today", 
            "Maybe?", "Click Yes!", "Nope!",
            "I'm shy", "Later?", "Can't decide",
            "You wish!", "Not sure", "Think again"
        ]
        self.no_button.text = choice(playful_texts)

if __name__ == '__main__':
    LoveApp().run()