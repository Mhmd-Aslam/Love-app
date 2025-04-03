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
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
import os
import shutil
from kivy.base import EventLoop

class RoundedButton(Button):
    """Button with rounded corners and visible colors"""
    border_radius = ListProperty([70])
    base_font_size = NumericProperty(24)
    
    def __init__(self, **kwargs):
        self.button_color = kwargs.pop('button_color', (0.9, 0.3, 0.5, 1))
        font_size = kwargs.pop('font_size', '24sp')
        if isinstance(font_size, str):
            self.base_font_size = float(font_size[:-2])
        else:
            self.base_font_size = float(font_size)
        
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.font_size = self.base_font_size
        self.draw_button()
        self.bind(pos=self.draw_button, size=self.draw_button, border_radius=self.draw_button)
    
    def draw_button(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.button_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.border_radius)
    
    def on_size(self, instance, size):
        scale_factor = size[1] / (Window.height * 0.3 * 0.3)
        new_size = max(12, self.base_font_size * scale_factor)
        self.font_size = new_size

class LoveApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Love App"
        self.icon = 'logos/heart.png'
        self._keyboard = None
    
    def on_start(self):
        """Bind keyboard events when app starts"""
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.clear_app_data()  # Clear data on initial launch
    
    def _keyboard_closed(self):
        """Handle keyboard being closed"""
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """Handle back button press on Android"""
        if keycode[1] == 'escape':  # Back button
            self.clear_app_data()
            App.get_running_app().stop()
            EventLoop.close()
            return True
        return False

    def clear_app_data(self):
        """Clear all stored data"""
        try:
            # Clear Kivy storage
            store = JsonStore('loveapp.json')
            store.clear()
            
            # Clear cache directory
            cache_dir = self.user_data_dir
            for filename in os.listdir(cache_dir):
                file_path = os.path.join(cache_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        except Exception as e:
            print(f"Error clearing data: {e}")

    message = StringProperty("Will you go on a date with me?")
    original_yes_size = (0.43, 0.6)
    original_yes_pos = {'center_x': 0.27, 'center_y': 0.5}
    no_button_clicks = 0
    
    expand_factors = {
        'left': 0.1,
        'right': 0.2,
        'top': 12.5,
        'bottom': 12
    }
    
    def build(self):
        Window.clearcolor = (0.98, 0.85, 0.9, 1)
        self.setup_ui()
        return self.layout
    
    def setup_ui(self):
        """Initialize all UI elements fresh each time"""
        self.layout = FloatLayout()
        
        # Content
        self.content = FloatLayout(size_hint=(1, 1))
        self.heart = Image(
            source="logos/heart.png",
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.content.add_widget(self.heart)
        
        self.label = Label(
            text=self.message,
            font_size=dp(24),
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
        
        # Buttons
        self.button_box = FloatLayout(size_hint=(1, 0.3), pos_hint={'bottom': 1})
        
        self.yes_button = RoundedButton(
            text="Yes!",
            font_size=dp(24),
            button_color=(0.9, 0.3, 0.5, 1),
            color=(1, 1, 1, 1),
            size_hint=self.original_yes_size,
            pos_hint=self.original_yes_pos,
            bold=True)
        self.yes_button.bind(on_press=self.say_yes)
        
        self.no_button = RoundedButton(
            text="No",
            font_size=dp(24),
            button_color=(0.7, 0.5, 0.7, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.43, 0.6),
            pos_hint={'center_x': 0.73, 'center_y': 0.5},
            bold=True)
        self.no_button.bind(on_press=self.on_no_press)
        
        self.button_box.add_widget(self.yes_button)
        self.button_box.add_widget(self.no_button)
        self.layout.add_widget(self.content)
        self.layout.add_widget(self.button_box)
    
    def show_fullscreen_love(self):
        # Create container for the fullscreen content
        container = FloatLayout()
        
        # Main love button
        self.love_button = RoundedButton(
            text="I LOVE YOU!",
            font_size=dp(48),
            button_color=(1, 0.2, 0.4, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},
            bold=True)
        self.love_button.border_radius = [0]
        container.add_widget(self.love_button)
        
        # Add watermark label
        watermark = Label(
            text="developed by Mhmd-Aslam",
            font_size=dp(12),
            color=(0.5, 0.5, 0.5, 0.7),
            size_hint=(None, None),
            size=(Window.width, dp(20)),
            pos_hint={'center_x': 0.5, 'y': 0.01},
            halign='center')
        container.add_widget(watermark)
        
        self.layout.clear_widgets()
        self.layout.add_widget(container)
        
        anim = (Animation(font_size=dp(52), duration=0.8) + 
               Animation(font_size=dp(48), duration=0.8))
        anim.repeat = True
        anim.start(self.love_button)
    
    def say_yes(self, instance):
        self.show_fullscreen_love()
    
    def on_no_press(self, instance):
        self.no_button_clicks += 1
        current_size = self.yes_button.size_hint
        current_pos = {
            'center_x': self.yes_button.pos_hint['center_x'],
            'center_y': self.yes_button.pos_hint['center_y']
        }
        
        growth_amount = (current_size[0] * 0.2, current_size[1] * 0.2)
        new_width = current_size[0] + growth_amount[0]
        new_height = current_size[1] + growth_amount[1]
        
        width_growth = new_width - current_size[0]
        height_growth = new_height - current_size[1]
        
        new_pos = {
            'center_x': current_pos['center_x'] - (width_growth * (self.expand_factors['left'] - self.expand_factors['right'])/2),
            'center_y': current_pos['center_y'] + (height_growth * (self.expand_factors['top'] - self.expand_factors['bottom'])/2)
        }
        
        anim = Animation(
            size_hint=(new_width, new_height),
            pos_hint=new_pos,
            duration=0.4,
            t='in_out_quad'
        )
        anim.start(self.yes_button)
        
        if self.no_button_clicks >= 7:
            current_no_pos = self.no_button.pos_hint['center_x']
            anim = Animation(
                size_hint_x=max(0.1, self.no_button.size_hint[0] - 0.05),
                pos_hint={'center_x': min(1.5, current_no_pos + 0.065), 'center_y': 0.5},
                duration=0.3
            )
            anim.start(self.no_button)
            
            if current_no_pos >= 1.3:
                Clock.schedule_once(lambda dt: self.button_box.remove_widget(self.no_button), 0.3)
        else:
            anim = Animation(
                size_hint=(max(0.1, self.no_button.size_hint[0] - 0.1), 
                max(0.1, self.no_button.size_hint[1] - 0.1)),
                duration=0.3
            )
            anim.start(self.no_button)
        
        playful_texts = [
            "No", "Try again", "Not today", 
            "Maybe?", "Click Yes!", "Nope!",
            "I'm shy", "Later?", "Can't decide",
            "You wish!", "Not sure", "Think again"
        ]
        self.no_button.text = choice(playful_texts)

if __name__ == '__main__':
    LoveApp().run()