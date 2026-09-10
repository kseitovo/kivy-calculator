from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView 
from kivy.graphics import Rectangle 
from kivy.clock import Clock 

MULTIPLIER = 1.8         

class CalculatorApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Налаштування фону
        with main_layout.canvas.before:
            self.bg_rect = Rectangle(source='background.jpg', size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Upper area (Calculations + History)
        top_area = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=0.45)
        
        # Left side (Calculator layout)
        calc_left_side = BoxLayout(orientation='vertical', spacing=8)
        calc_left_side.add_widget(Label(text=f'Формула: (X × {MULTIPLIER}) - Y', font_size=28, size_hint_y=None, height=35, color=(1, 1, 1, 1)))
        
        # Створення полів введення через оптимізовану функцію
        calc_left_side.add_widget(Label(text='Число (X):', font_size=24, size_hint_y=None, height=25, color=(1, 1, 1, 1)))
        self.input_x = self._create_text_input('Введіть X', (0.85, 0.9, 1, 1))
        calc_left_side.add_widget(self.input_x)
        
        calc_left_side.add_widget(Label(text='Число (Y):', font_size=24, size_hint_y=None, height=25, color=(1, 1, 1, 1)))
        self.input_subtract = self._create_text_input('Введіть Y', (1, 1, 1, 1))
        calc_left_side.add_widget(self.input_subtract)
        
        self.current_focus = self.input_x 
        
        # Тексти відображення результатів
        calc_left_side.add_widget(Widget(size_hint_y=None, height=15))
        self.multiply_label = Label(text='* 0', font_size=44, size_hint_y=None, height=50, color=(1, 1, 1, 1))
        self.result_label = Label(text='= 0', font_size=56, size_hint_y=None, height=60, markup=True, color=(1, 1, 1, 1))
        calc_left_side.add_widget(self.multiply_label)
        calc_left_side.add_widget(Widget(size_hint_y=None, height=10))
        calc_left_side.add_widget(self.result_label)
        
        top_area.add_widget(calc_left_side)
        
        # Right side (History)
        history_side = BoxLayout(orientation='vertical', spacing=5)
        history_side.add_widget(Label(text='Історія:', font_size=26, size_hint_y=None, height=30, color=(1, 1, 1, 1)))
        
        scroll_view = ScrollView(size_hint=(1, 1), bar_width=12)
        self.history_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        
        scroll_view.add_widget(self.history_layout)
        history_side.add_widget(scroll_view)
        
        clear_hist_btn = Button(text='Очистити історію', font_size=20, size_hint_y=None, height=45, background_color=(0.7, 0.4, 0.4, 1))
        clear_hist_btn.bind(on_press=self.clear_history)
        history_side.add_widget(clear_hist_btn)
        
        top_area.add_widget(history_side)
        main_layout.add_widget(top_area)
        main_layout.add_widget(Widget(size_hint_y=None, height=15))
        
        # Keyboard Area
        keyboard_area = BoxLayout(orientation='vertical', size_hint_y=0.5, spacing=8)
        grid = GridLayout(cols=3, spacing=8, size_hint_y=0.85)
        
        buttons = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '0', '.', '⌫']
        for btn_text in buttons:
            bg_color = (0.9, 0.3, 0.3, 1) if btn_text == '⌫' else (0.25, 0.25, 0.25, 1)
            btn = Button(text=btn_text, font_size=36, background_color=bg_color)
            btn.bind(on_press=self.on_button_press)
            grid.add_widget(btn)
        keyboard_area.add_widget(grid)
        
        # Bottom row for quick clears
        clear_row = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=0.15)
        for btn_text in ['0*X', '0*Y']:
            btn = Button(text=btn_text, font_size=28, background_color=(0.9, 0.3, 0.3, 1))
            btn.bind(on_press=self.on_button_press)
            clear_row.add_widget(btn)
            
        keyboard_area.add_widget(clear_row)
        main_layout.add_widget(keyboard_area)
        
        self.history_event = None
        self.last_saved_string = ""
        return main_layout

    # ФІКС: Відступи відновлено, помилку усунено
    def _create_text_input(self, hint, bg_color):
        ti = TextInput(
            text='', hint_text=hint, multiline=False, font_size=44, size_hint_y=None, height=80,
            halign='center', padding=[0, 20, 0, 20], background_color=bg_color
        )
        ti.bind(on_touch_down=self.select_field)
        return ti

    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def select_field(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.input_x.background_color = (1, 1, 1, 1)
            self.input_subtract.background_color = (1, 1, 1, 1)
            self.current_focus = instance
            instance.background_color = (0.85, 0.9, 1, 1)
            return True 
        return instance.on_touch_down(touch)

    def on_button_press(self, instance):
        text = instance.text
        if text == '0*X':
            self.input_x.text = ''
        elif text == '0*Y': 
            self.input_subtract.text = ''
        elif text == '⌫':
            self.current_focus.text = self.current_focus.text[:-1]
        elif text == '.':
            if '.' not in self.current_focus.text:
                self.current_focus.text = '0.' if not self.current_focus.text else self.current_focus.text + '.'
        else:
            self.current_focus.text += text
            
        self.calculate()

    def calculate(self):
        txt_x = self.input_x.text
        txt_y = self.input_subtract.text
        
        try:
            val_x = float(txt_x) if txt_x else 0.0
            val_sub = float(txt_y) if txt_y else 0.0
            
            mult_result = val_x * MULTIPLIER
            final_result = mult_result - val_sub
            
            self.multiply_label.text = f'* {round(mult_result, 4)}'
            self.result_label.text = f'= {round(final_result, 4)}'
            
            if self.history_event:
                Clock.unschedule(self.history_event)
            
            if txt_x and txt_y:
                self.history_event = Clock.schedule_once(self.save_to_history, 1.5)
                    
        except ValueError:
            self.multiply_label.text = '* —'
            self.result_label.text = '[color=ff6666]= Помилка![/color]'

    def save_to_history(self, dt):
        current_calc_string = f"X:{self.input_x.text} | Y:{self.input_subtract.text} {self.result_label.text}"
        
        if current_calc_string != self.last_saved_string:
            history_item = Label(
                text=current_calc_string, font_size=40, size_hint_y=None, height=60,
                color=(0.9, 0.9, 0.9, 1), halign='left'
            )
            history_item.bind(size=self._update_label_text_size)
            
            self.history_layout.add_widget(history_item, index=len(self.history_layout.children))
            self.last_saved_string = current_calc_string

    def _update_label_text_size(self, label, size):
        label.text_size = (label.width, None)

    def clear_history(self, instance):
        if self.history_event:
            Clock.unschedule(self.history_event)
        self.history_layout.clear_widgets()
        self.last_saved_string = ""

if __name__ == '__main__':
    CalculatorApp().run()
