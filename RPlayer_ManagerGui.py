import customtkinter
import find_serial_port as PortsCom
import subprocess
import json
import time
import RPlayer_Settings as Settings

# SETTING UP WINDOW
app = customtkinter.CTk()

# SETTING UP VARIABLE(S)
ComPort = ""

settings = Settings.LoadSettings()


# SETTING UP TABVIEW CLASS
class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        global settings
        super().__init__(master, **kwargs)

        # create tabs
        tab1 = self.add("General settings")
        tab2 = self.add("Primary mode")
        tab3 = self.add("Secondary mode")

        # add 'master=self.tab("Primary mode")' or 'master=self.tab("Secondary mode")' to any master

        # general settings
        def switch_event(self):
            global settings
            settings["multScreens"] = int(self.switch_var.get())
            print("switch toggled, current value:", settings["multScreens"])
            if settings["multScreens"] == 0:
                self.delete("Secondary mode")
            elif settings["multScreens"] == 1:
                self.insert(2, "Secondary mode")

        def optionmenu_callback01(choice):
            global settings
            global ComPort

            print("optionmenu02 dropdown clicked:", choice)
            settings = {
                "comport": OptionsList01Short[OptionsList01.index(choice)],
                "optionmenu1": self.optionmenu02.get(),
                "optionmenu2": self.optionmenu03.get(),
            }
            print(settings)

        self.switch_var = customtkinter.StringVar(value=True)
        self.switch = customtkinter.CTkSwitch(
            master=self.tab("General settings"),
            text="Two modes",
            command=lambda: switch_event(self),
            variable=self.switch_var,
            onvalue=True,
            offvalue=False,
        )
        self.switch.select()

        OptionsList01 = PortsCom.GetSerialPorts()
        OptionsList01Short = PortsCom.GetShortenedSerialPorts()

        # for i in PortsCom.GetSerialPorts():
        #    OptionsList01.append(i)
        # for i in PortsCom.GetShortenedSerialPorts():
        #    OptionsList01Short.append(i)

        self.optionmenu_var01 = customtkinter.StringVar(value=OptionsList01[-1])
        self.optionmenu01 = customtkinter.CTkOptionMenu(
            master=self.tab("General settings"),
            command=optionmenu_callback01,
            values=OptionsList01,
            variable=self.optionmenu_var01,
        )

        self.optionmenu01.grid(row=1, column=1, padx=20, pady=10)
        self.switch.grid(row=0, column=0, padx=20, pady=10)

        # Primary menu
        def optionmenu_callback02(choice):
            global settings
            print("optionmenu02 dropdown clicked:", choice)
            settings = {
                "comport": ComPort,
                "optionmenu1": self.optionmenu02.get(),
                "optionmenu2": self.optionmenu03.get(),
            }
            print(settings)

        self.optionmenu_var02 = customtkinter.StringVar(value=settings["optionmenu1"])
        self.optionmenu02 = customtkinter.CTkOptionMenu(
            master=self.tab("Primary mode"),
            values=["Media info", "Option 2", "Option 3"],
            command=optionmenu_callback01,
            variable=self.optionmenu_var02,
        )

        self.optionmenu02.grid(row=0, column=0, padx=20, pady=10)

        # Second Menu

        def optionmenu_callback03(choice):
            global settings
            print("optionmenu03 dropdown clicked:", choice)
            settings = {
                "comport": ComPort,
                "optionmenu1": self.optionmenu02.get(),
                "optionmenu2": self.optionmenu03.get(),
            }
            print(settings)

        self.optionmenu_var03 = customtkinter.StringVar(value=settings["optionmenu2"])
        self.optionmenu03 = customtkinter.CTkOptionMenu(
            master=self.tab("Secondary mode"),
            values=["Media info", "option 2", "option 3"],
            command=optionmenu_callback03,
            variable=self.optionmenu_var03,
        )

        self.optionmenu03.grid(row=0, column=0, padx=20, pady=10)


# SETTING UP APP
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Rose Player Management app")
        self.iconbitmap("Icons/Rose256.ico")

        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, columnspan=2)

        self.ApplyButton = customtkinter.CTkButton(
            self, text="Apply settings", command=self.apply_button_callbck
        )
        self.ApplyButton.grid(row=1, column=0, padx=20, pady=20)

        self.SaveButton = customtkinter.CTkButton(
            self, text="Save settings", command=self.save_button_callbck
        )
        self.SaveButton.grid(row=1, column=1, padx=20, pady=20)

    def save_button_callbck(self):
        global settings

    def apply_button_callbck(self):
        global settings
        print(settings)
        with open("Settings.json", "w") as f:
            json.dump(settings, f)
        subprocess.run(["python", "RPlayer_ControllerCom.py"])


if __name__ == "__main__":
    app = App()
    app.mainloop()
