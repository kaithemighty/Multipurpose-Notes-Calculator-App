from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from datetime import date
from kivy.config import Config
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.graphics import Color, Line , Rotate
from kivy.metrics import sp
from kivy.uix.behaviors.button import ButtonBehavior
from kivymd.uix.pickers import MDDatePicker
import pandas as pd
import matplotlib.pyplot as plt
from functools import partial
import os
import csv
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '1067')
Config.write()

global show
global popupWindow

class MainButton(Button):
     pass
class OutlineButton(Button):
     pass

class CreateAccount(FloatLayout):
     def createacct(self):
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, "accountinfo.csv")
        with open(file_path , 'w') as accountinfo:
            accountinfo.write(f"{self.newuser.text}\n{self.newpass.text}")

     def dismiss_popup(self):
        self.parent.parent.parent.dismiss()
        pass
     pass

class INPUT(Screen):
    def show_date_picker(self , *args):
        self.date_picker = MDDatePicker()
        self.date_picker.bind(on_save=self.get_date)
        self.date_picker.open()

    def get_date(self, instance, value, *args):
        self.selected_date = value

    def add_data_field(self):
        self.popup = Popup(
            title='Add a Value',
            size_hint=(.6, .4),
            pos_hint={'top': .85}
        )
        layout = BoxLayout(orientation='vertical')
        self.date_picker = Button(
            text='Date of Transaction',
            on_release=self.show_date_picker
        )
        self.text_input_amount = TextInput(
            multiline=False,
            hint_text='Amount of Transaction'
        )
        layout.add_widget(self.date_picker)
        layout.add_widget(self.text_input_amount)
        add_button = Button(text='DONE', size_hint=(1, .2))
        add_button.bind(on_release = self.add_data_field_values)
        layout.add_widget(add_button)
        self.popup.content = layout
        self.popup.open()
        pass

    def add_data_field_values(self , instance):
        field_name = MDApp.get_running_app().root.ids.input.ids.Chosen_Field.text
        def save_values_to_File(date,amount,file_name):
            current_dir = os.getcwd()
            current_file = ("sources\\" + file_name + ".csv")
            file_path = os.path.join(current_dir , current_file)
            with open(file_path , 'a+') as current_file:
                current_file.write(str(date) + ',' + amount + '\n')
            pass
        def remove_file_entry(selected_date , amount):
            current_dir = os.getcwd()
            file_name = ("sources\\" + field_name + ".csv")
            file_path = os.path.join(current_dir , file_name)
            data = str(selected_date) + ',' + amount
            current_file = open(file_path , 'r')
            lines = current_file.readlines()
            for i in lines:
                lines[lines.index(i)] = i.strip()
                i = i.strip()
            current_file.close()
            open(file_path , 'w').close()
            for i in lines:
                if data == i:
                    lines.remove(i)
            with open(file_path , 'a+') as current_file:
                if lines != None:
                    for i in lines:
                        current_file.write(i + '\n')
            
        amount = self.text_input_amount.text.strip()
        layout = BoxLayout(orientation = 'horizontal' , size_hint_y = (None) , height = 40)

        date_button = OutlineButton(
            text = str(self.selected_date) ,
            size_hint = (.4 , None) ,
            height = 40
            )
        amount_button = OutlineButton(
            text = "$" + amount ,
            size_hint = (.4 , None) , 
            height = 40
            )
        minus_button = OutlineButton(
            text = '-' ,
            size_hint = (.1 , None) ,
            height = 40
            )

        layout.id = (str(self.selected_date) + '_' + amount)
        minus_button.bind(on_release = partial(self.remove_data_field_instance , layout))
        minus_button.bind(on_release=lambda *args: remove_file_entry(str(self.selected_date), str(amount)))

        layout.add_widget(date_button)
        layout.add_widget(amount_button)
        layout.add_widget(minus_button)

        box_layout = self.ids.INPUT_scroll
        box_layout.add_widget(layout)
        save_values_to_File(str(self.selected_date) , amount , field_name)
        self.popup.dismiss()
        pass
    
    def remove_data_field(self, widget):
        self.ids.INPUT_scroll.parent.remove_widget(self.ids.INPUT_scroll)

    def remove_data_field_instance(self , layout , instance):
        self.ids.INPUT_scroll.remove_widget(instance.parent)
    
    def clear_values(self):
        parent_widget = self.ids.INPUT_scroll
        for widget in parent_widget.children[:]:
            parent_widget.remove_widget(widget)
        pass
    pass

show = CreateAccount()
popupWindow = Popup(title = 'Account Creator' , content = CreateAccount())

class FirstScreen(Screen):
    #Login
    #Button.background_color = (.3,.92,1,1)
    Button.background_normal = ""
    Button.color = 0,0,0,1
    user = ObjectProperty()
    password = ObjectProperty()
    popupWindow = ObjectProperty()

    newuser = ObjectProperty()
    newpass = ObjectProperty()
    WindowManager = ObjectProperty()

    def change_INPUT_values(self , field_name):
        button = MDApp.get_running_app().root.ids.input.ids.Chosen_Field
        button.text = field_name
        pass

    def load_values(self, field_name):
        
        current_file = ("sources\\" + field_name + ".csv") 

        try:
            with open(current_file, 'r') as file:
                reader = csv.reader(file)
                grid_layout = MDApp.get_running_app().root.ids.input.ids.INPUT_scroll
                grid_layout.clear_widgets()
                for row in reader:
                    selected_date = row[0]
                    amount = row[1]
                    horizontal_layout = BoxLayout(orientation='horizontal' , size_hint_y = None , height = 40)
                    date_button = OutlineButton(
                        text=str(selected_date),
                        size_hint=(.4, None),
                        height=40
                    )
                    amount_button = OutlineButton(
                        text="$" + amount,
                        size_hint=(.4, None),
                        height=40
                    )
                    minus_button = OutlineButton(
                        text='-',
                        size_hint=(.1, None),
                        height=40,
                    )

                    minus_button.bind(on_release=partial(self.remove_data_field_entry, field_name, selected_date, amount))

                    horizontal_layout.add_widget(date_button)
                    horizontal_layout.add_widget(amount_button)
                    horizontal_layout.add_widget(minus_button)
                    button = self.manager.get_screen('INPUT').ids.INPUT_scroll
                    button.add_widget(horizontal_layout)
                    pass
                pass
        except FileNotFoundError:
            pass
    def remove_data_field_entry(self, field_name, selected_date, amount, instance):
        remove_file_entry(selected_date, amount, field_name)
        scroll_view = MDApp.get_running_app().root.ids.input.ids.INPUT_scroll
        scroll_view.remove_widget(instance.parent)
        self.load_values(field_name)    
        pass

    def load_sources(self , expenses_or_income):
        current_file = expenses_or_income + "_sources.csv"
        def button_press_handler(name):
            def on_button_press(instance):
                setattr(self.manager , 'current' , 'INPUT')
                self.change_INPUT_values(name + ' ' + expenses_or_income)
                self.load_values(name + ' ' + expenses_or_income)
            return on_button_press
        try:
            with open(current_file , 'r') as file:
                reader = list(csv.reader(file))
                layout = MDApp.get_running_app().root.ids.second_screen
                if expenses_or_income.lower() == 'income':
                    child_layout = layout.ids.Income_Box
                elif expenses_or_income.lower() == 'expenses':
                    child_layout = layout.ids.Debt_Box
                child_layout.clear_widgets()
                for row in reader:
                    button_name = str(row[0])
                    parent_layout = BoxLayout(
                        orientation = 'horizontal' ,
                        size_hint_y = None ,
                        height = 100
                        )
                    on_press_callback = button_press_handler(button_name)
                    main_button = OutlineButton(
                        text = button_name ,
                        size_hint = (.9 , None) ,
                        height = 100 ,
                        on_press = on_press_callback
                        )
                    minus_button = OutlineButton(
                        text = '-' ,
                        size_hint = (.1 , None) ,
                        height = 100
                        )
                    parent_layout.id = (button_name.lower() + '_layout')
                    minus_button.bind(
                        on_release = partial(
                            self.unload_data_field_instance ,
                            expenses_or_income ,
                            parent_layout.id
                            )
                        )
                    parent_layout.add_widget(main_button)
                    parent_layout.add_widget(minus_button)

                    child_layout.add_widget(parent_layout)
            
        except FileNotFoundError:
            pass

    def unload_data_field_instance(self , expenses_or_income , button_id , instance):
        layout = MDApp.get_running_app().root.ids.second_screen
        if expenses_or_income.lower() == 'income':
            box_layout = layout.ids.Income_Box
        elif expenses_or_income.lower() == 'expenses':
            box_layout = layout.ids.Debt_Box
        for child in box_layout.children:
            if child.id == button_id:
                box_layout.remove_widget(child)
                break
        #remove the button so it isn't loaded in the future
        current_file = expenses_or_income + "_sources.csv"
        try:
            with open(current_file , 'r') as file:
                reader = csv.reader(file)
                contents = list(reader)
            button_name = button_id.replace("_layout" , "")
            contents[:] = [sublist for sublist in contents if sublist != [button_name.upper()]]
            with open(current_file , 'w') as file:
                writer = csv.writer(file , lineterminator = '\n')
                writer.writerows(contents)

        except FileNotFoundError:
            pass
        except ValueError:
            print('ValueError')
        pass
    
    def validate(self , username , password):
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, "accountinfo.csv")
        with open(file_path , 'r') as accountinfo:
            admin = accountinfo.readlines()
            admin_username = admin[0].rstrip()
            admin_password = admin[1].rstrip()
        if username.rstrip() == admin_username and password.rstrip() == admin_password:
            self.manager.current = 'input'
            
    def show_popup(self):
        popupWindow = Popup(title = 'Account Creator' , content = CreateAccount())
        popupWindow.open()
        
        pass
    
    pass

class SecondScreen(Screen):
    #Input Income and Debts
    def add_income_button(self , instance):
        button_name = self.text_input.text.upper().strip()
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir , "income_sources.csv")
        with open(file_path , 'a+') as sources:
            sources.write(button_name + "\n")
        layout = BoxLayout(orientation = 'horizontal' , size_hint_y = (None) , height = 100)

        income_button = OutlineButton(
            text = button_name ,
            size_hint = (.9 , None) ,
            height = 100 ,
            on_press = lambda instance: (
                setattr(self.manager, 'current', 'INPUT') ,
                self.change_INPUT_values(button_name + ' Income') ,
                self.load_values(button_name + ' Income')
            )
        )
        minus_button = OutlineButton(
            text = '-' ,
            size_hint = (.1 , None) ,
            height = 100 
            )

        layout.id = button_name.lower() + "_layout"
        minus_button.bind(on_release = partial(self.remove_data_field_income_instance , layout.id))

        layout.add_widget(income_button)
        layout.add_widget(minus_button)

        box_layout = self.ids.Income_Box
        box_layout.add_widget(layout)
        self.popup.dismiss()
        pass
        
    def income_button(self):
        self.popup = Popup(title = 'Income Field' , size_hint = (.6 , .4) , pos_hint = {'top': .85})
        layout = BoxLayout(orientation = 'vertical')
        self.text_input = TextInput(multiline = False , on_text_validate = self.add_income_button)
        layout.add_widget(self.text_input)
        add_button = Button(text = 'DONE' , size_hint = (1 , .2))
        add_button.bind(on_release = self.add_income_button)
        layout.add_widget(add_button)
        self.popup.content = layout
        self.popup.open()
        pass
    
    
    def add_debt_button(self , instance):
        button_name = self.text_input.text.upper().strip()
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir , "expenses_sources.csv")
        with open(file_path , 'a+') as sources:
            sources.write(button_name + "\n")
        layout = BoxLayout(orientation = 'horizontal' , size_hint_y = (None) , height = 100)
        
        debt_button = OutlineButton(
            text = button_name ,
            size_hint = (.9 , None) ,
            height = 100 ,
            on_press = lambda instance: (
                setattr(self.manager, 'current', 'INPUT') ,
                self.change_INPUT_values(button_name + ' Expenses') ,
                self.load_values(button_name + ' Expenses')
            )
        )
        
        minus_button = OutlineButton(
            text = '-' ,
            size_hint = (.1 , None) ,
            height = 100 
            )

        layout.id = button_name.lower() + "_layout"
        minus_button.bind(on_release = partial(self.remove_data_field_debt_instance , layout.id))
        
        layout.add_widget(debt_button)
        layout.add_widget(minus_button)
         
        box_layout = self.ids.Debt_Box
        box_layout.add_widget(layout)
        self.popup.dismiss()
        pass
        
    def debt_button(self):
        self.popup = Popup(title = 'Debt Field' , size_hint = (.6 , .4) , pos_hint = {'top': .85})
        layout = BoxLayout(orientation = 'vertical')
        self.text_input = TextInput(multiline = False , on_text_validate = self.add_debt_button)
        layout.add_widget(self.text_input)
        add_button = Button(text = 'DONE' , size_hint = (1 , .2))
        add_button.bind(on_release = self.add_debt_button)
        layout.add_widget(add_button)
        self.popup.content = layout
        self.popup.open()
        pass
    def income_hint(self):
        self.popup = Popup(title = 'Income Sources' , size_hint = (.6 , .4) , pos_hint = {'top': .85})
        layout = BoxLayout(orientation = 'vertical')
        self.info = Button(text = '           Here you can input your various \n \
income sources for data tracking purposes.  \n \
        Click the "Add Input Field" button to \n \
 add one to the list. Click the minus button \n \
  to remove one if it doesn\'t apply for you. \n \
       Click on any of them to record an \n \
                  entry for the input field' , size_hint = (1 , .9))
        self.exit = Button(text = 'close' , size_hint = (1 , .1))
        self.exit.bind(on_release = self.popup.dismiss)
        layout.add_widget(self.info)
        layout.add_widget(self.exit)                   
        self.popup.content = layout
        self.popup.open()
        pass
    
    def debt_hint(self):
        self.popup = Popup(title = 'Debt Sources' , size_hint = (.6 , .4) , pos_hint = {'top': .85})
        layout = BoxLayout(orientation = 'vertical')
        self.info = Button(text = '           Here you can input your various \n \
    debt sources for data tracking purposes.  \n \
          Click the "Add Debt Field" button to \n \
 add one to the list. Click the minus button \n \
  to remove one if it doesn\'t apply for you. \n \
       Click on any of them to record an \n \
                    entry for the debt field' , size_hint = (1 , .9))
        self.exit = Button(text = 'close' , size_hint = (1 , .1))
        self.exit.bind(on_release = self.popup.dismiss)
        layout.add_widget(self.info)
        layout.add_widget(self.exit)                   
        self.popup.content = layout
        self.popup.open()
        pass
    
    def remove_data_field_debt_instance(self , button_id , instance):
        #When the minus button is pressed, this code removes the button for the data field.
        box_layout = self.ids.Debt_Box
        for child in box_layout.children:
            if child.id == button_id:
                box_layout.remove_widget(child)
                break
        pass
    
    def remove_data_field_income_instance(self , button_id , instance):
        #When the minus button is pressed, this code removes the button for the data field.
        box_layout = self.ids.Income_Box
        for child in box_layout.children:
            if child.id == button_id:
                box_layout.remove_widget(child)
                break
        pass
    
    def remove_data_field_debt(self , instance):
        #When the minus button is pressed, this code removes the button for the data field.
        self.ids.Debt_Box.remove_widget(instance.parent)
        pass
    
    def remove_data_field_income(self , instance):
        #When the minus button is pressed, this code removes the button for the data field.
        self.ids.Income_Box.remove_widget(instance.parent)
        pass

    def change_INPUT_values(self , field_name):
        button = MDApp.get_running_app().root.ids.input.ids.Chosen_Field 
        button.text = field_name
        pass
    
    def load_values(self, field_name):
        
        current_file = ("sources\\" + field_name + ".csv") 

        try:
            with open(current_file, 'r') as file:
                reader = csv.reader(file)
                grid_layout = MDApp.get_running_app().root.ids.input.ids.INPUT_scroll
                grid_layout.clear_widgets()
                for row in reader:
                    selected_date = row[0]
                    amount = row[1]
                    horizontal_layout = BoxLayout(orientation='horizontal' , size_hint_y = None , height = 40)
                    date_button = OutlineButton(
                        text=str(selected_date),
                        size_hint=(.4, None),
                        height=40
                    )
                    amount_button = OutlineButton(
                        text="$" + amount,
                        size_hint=(.4, None),
                        height=40
                    )
                    minus_button = OutlineButton(
                        text='-',
                        size_hint=(.1, None),
                        height=40,
                    )

                    minus_button.bind(on_release=partial(self.remove_data_field_entry, field_name, selected_date, amount))

                    horizontal_layout.add_widget(date_button)
                    horizontal_layout.add_widget(amount_button)
                    horizontal_layout.add_widget(minus_button)
                    button = self.manager.get_screen('INPUT').ids.INPUT_scroll
                    button.add_widget(horizontal_layout)
                    pass
                pass
        except FileNotFoundError:
            pass
    def remove_data_field_entry(self, field_name, selected_date, amount, instance):
        remove_file_entry(selected_date, amount, field_name)
        scroll_view = MDApp.get_running_app().root.ids.input.ids.INPUT_scroll
        scroll_view.remove_widget(instance.parent)
        self.load_values(field_name)    
        pass


                           
    pass
def remove_file_entry(selected_date, amount, field_name):
    current_dir = os.getcwd()
    file_name = os.path.join(current_dir, "sources", field_name + ".csv")
    data = str(selected_date) + ',' + amount
    lines = []
    with open(file_name, 'r') as current_file:
        lines = [line.strip() for line in current_file.readlines()]

    lines = [line for line in lines if line != data]

    with open(file_name, 'w') as current_file:
        for line in lines:
            current_file.write(line + '\n')   
class ThirdScreen(Screen):
    #This Screen Displays Average amount spent per month on each category

    pass




class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("debttoincome.kv")

class AwesomeApp(MDApp):
    def build(self):
        return kv

if __name__ == "__main__":
    AwesomeApp().run()
