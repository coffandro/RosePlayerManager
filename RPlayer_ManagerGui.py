import customtkinter
import RPlayer_GetPlayingInfo as Controller
import subprocess
import json

# SETTING UP WINDOW
app = customtkinter.CTk()

# SETTING UP VARIABLE(S)

try:
    f = open('Settings.json', "rw")

    # returns JSON object as
    # a dictionary
    settings = json.load(f)

    # Closing file
    f.close()
except:
    settings = {"multScreens": 0, "optionmenu1": "Media info","optionmenu2": "Media info"}
# SETTING UP TABVIEW CLASS
class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        global settings
        super().__init__(master, **kwargs)

        # create tabs
        self.add("General settings")
        self.add("Primary mode")
        self.add("Secondary mode")
        
        # add 'master=self.tab("Primary mode")' or 'master=self.tab("Secondary mode")' to any master
        
        # general settings
        def switch_event(self):
            global settings
            settings["multScreens"] = int(self.switch_var.get())
            print("switch toggled, current value:", settings["multScreens"])
            if settings["multScreens"] == 0:
                self.configure(self.tab("Secondary mode"), state="disabled")

        self.switch_var = customtkinter.StringVar(value="on")
        self.switch = customtkinter.CTkSwitch(
            master=self.tab("General settings"),
            text="Two modes",
            command=lambda: switch_event(self),
            variable=self.switch_var,
            onvalue=True,
            offvalue=False)
        
        self.switch.grid(row=0, column=0, padx=20, pady=10)
        
        # Primary menu
        def optionmenu_callback01(choice):
            global settings
            print("optionmenu01 dropdown clicked:", choice)
            settings = {
                "optionmenu1": self.optionmenu01.get(),
                "optionmenu2": self.optionmenu02.get()
            }
            print(settings)
        
        
        self.optionmenu_var01 = customtkinter.StringVar(value=settings["optionmenu1"])
        self.optionmenu01 = customtkinter.CTkOptionMenu(
            master=self.tab("Primary mode"),
            values=[
                "Media info",
                "Option 2",
                "Option 3"
            ],
            command=optionmenu_callback01,
            variable=self.optionmenu_var01)
        
        self.optionmenu01.grid(row=0, column=0, padx=20, pady=10)
        
        # Second Menu
        
        def optionmenu_callback02(choice):
            global settings
            print("optionmenu02 dropdown clicked:", choice)
            settings = {
                "optionmenu1": self.optionmenu01.get(),
                "optionmenu2": self.optionmenu02.get()
            }
            print(settings)

        self.optionmenu_var02 = customtkinter.StringVar(value=settings["optionmenu2"])
        self.optionmenu02 = customtkinter.CTkOptionMenu(
            master=self.tab("Secondary mode"),
            values=[
                "Media info",
                "option 2",
                "option 3"
            ],
            command=optionmenu_callback02,
            variable=self.optionmenu_var02)
        
        self.optionmenu02.grid(row=0, column=0, padx=20, pady=10)

# SETTING UP APP
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Rose Player Management app")
        self.iconbitmap("Icons/Rose256.ico")
    
        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
        
        self.ApplyButton = customtkinter.CTkButton(self, text="Apply settings", command=self.apply_button_callbck)
        self.ApplyButton.grid(row=1, column=0, padx=20, pady=20)
        
        self.SaveButton = customtkinter.CTkButton(self, text="Save settings", command=self.save_button_callbck)
        self.SaveButton.grid(row=1, column=1, padx=20, pady=20)
        
    def save_button_callbck(self):
        global settings
        print(settings)
        with open('Settings.json', 'w') as f:
            json.dump(settings, f)
    
    def apply_button_callbck(self):
        subprocess.run(["python", "RPlayer_ControllerCom.py"])

if __name__ == '__main__':
    app = App()
    app.mainloop()