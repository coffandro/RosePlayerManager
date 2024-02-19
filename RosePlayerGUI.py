import customtkinter
import RosePlayerPlaying as Playing
import RosePlayerFuncs as Global
from PIL import Image
import time

# global variables
Settings = Global.Read_Settings()


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)


class ScreenManagement(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # create tab
        self.add("Primary mode")
        self.add("Secondary mode")

        # create functions
        def CheckScreenAmount():
            if Settings["multScreens"] == 1:
                # couldn't find a "proper" way to check if the tab is present lol
                try:
                    self.tab("Secondary mode")
                except:
                    self.add("Secondary mode")
            else:
                try:
                    self.delete("Secondary mode")
                except:
                    pass
            self.after(100, CheckScreenAmount)

        def ModeMenu1(choice):
            Settings = Global.Read_Settings()
            print("optionmenu dropdown clicked:", choice)
            Settings["optionmenu1"] = choice
            Global.Write_Settings(Settings)

        def ModeMenu2(choice):
            Settings = Global.Read_Settings()
            print("optionmenu dropdown clicked:", choice)
            Settings["optionmenu2"] = choice
            Global.Write_Settings(Settings)

        # add widgets on Primary mode
        self.label1 = customtkinter.CTkLabel(
            master=self.tab("Primary mode"),
            text="What should be displayed in the primary mode?",
        )

        self.optionmenu1 = customtkinter.CTkOptionMenu(
            master=self.tab("Primary mode"),
            values=["Media info", "Hacker mode", "Option 3"],
            command=ModeMenu1,
        )
        self.optionmenu1.set(Settings["optionmenu1"])

        self.optionmenu1.grid(row=1, column=0, columnspan=2, padx=20)
        self.label1.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        # add widgets on Secondary mode
        self.label2 = customtkinter.CTkLabel(
            master=self.tab("Secondary mode"),
            text="What should be displayed in the primary mode?",
        )

        self.optionmenu2 = customtkinter.CTkOptionMenu(
            master=self.tab("Secondary mode"),
            values=["Media info", "Hacker mode", "Option 3"],
            command=ModeMenu2,
        )
        self.optionmenu2.set(Settings["optionmenu2"])

        self.optionmenu2.grid(row=1, column=0, columnspan=2, padx=20)
        self.label2.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        # refresh
        CheckScreenAmount()


class GeneralManagement(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create variables

        # create functions
        def CheckboxEvent():
            Settings = Global.Read_Settings()
            if self.CheckVar.get() == "1":
                Settings["multScreens"] = 1
            else:
                Settings["multScreens"] = 0
            Global.Write_Settings(Settings)

        def MediaDelayButtonAction():
            Settings = Global.Read_Settings()
            DelayNum = self.MediaDelayEntry.get()
            DelayFormat = self.MediaDelayMenu.get()
            try:
                DelayNum = int(DelayNum)
                if DelayFormat == "Sec":
                    Settings["MediaDelay"] = int(DelayNum * 1000)
                elif DelayFormat == "Min":
                    Settings["MediaDelay"] = int(DelayNum * 10000 * 60)
                elif DelayFormat == "Hour":
                    Settings["MediaDelay"] = int(DelayNum * 10000 * 60 * 60)

                print(Settings)
                Settings["MediaDelaySet"] = True
                Settings["MediaDelayFormat"] = DelayFormat

                Global.Write_Settings(Settings)
            except ValueError:
                self.MediaDelayEntry.delete(0, 999)
                self.MediaDelayEntry.insert(0, "NUMBER!")

        # create tab
        self.add("General Settings")

        # create widgets
        self.CheckVar = customtkinter.StringVar(value=str(Settings["multScreens"]))
        self.Checkbox = customtkinter.CTkCheckBox(
            master=self.tab("General Settings"),
            text="Multiple display modes",
            command=CheckboxEvent,
            variable=self.CheckVar,
            onvalue="1",
            offvalue="0",
        )

        self.MediaDelayLabel1 = customtkinter.CTkLabel(
            master=self.tab("General Settings"),
            text="Refresh rate:",
            font=("Roboto", 13, "bold"),
        )
        self.MediaDelayLabel2 = customtkinter.CTkLabel(
            master=self.tab("General Settings"), text="Every:"
        )
        self.MediaDelayEntry = customtkinter.CTkEntry(
            master=self.tab("General Settings"),
            placeholder_text="A number",
            width=85,
        )
        if Settings["MediaDelayFormat"] == "Sec":
            self.MediaDelayEntry.insert(0, int(Settings["MediaDelay"] / 1000))
        elif Settings["MediaDelayFormat"] == "Min":
            self.MediaDelayEntry.insert(0, int(Settings["MediaDelay"] / 10000 / 60))
        elif Settings["MediaDelayFormat"] == "Hour":
            self.MediaDelayEntry.insert(
                0, int(Settings["MediaDelay"] / 10000 / 60 / 60)
            )

        self.MediaDelayMenu_var = customtkinter.StringVar(
            value=Settings["MediaDelayFormat"]
        )
        self.MediaDelayMenu = customtkinter.CTkOptionMenu(
            master=self.tab("General Settings"),
            values=["Sec", "Min", "Hour"],
            variable=self.MediaDelayMenu_var,
            width=65,
        )

        self.MediaDelayButton = customtkinter.CTkButton(
            master=self.tab("General Settings"),
            text="Set Delay",
            command=lambda: MediaDelayButtonAction(),
            width=200,
        )

        # add widgets on tab
        self.Checkbox.grid(row=0, column=0, columnspan=2, padx=10)

        self.MediaDelayLabel1.grid(row=1, column=0, pady=20)
        # self.MediaDelayLabel2.grid(row=1, column=1, pady=10)
        self.MediaDelayEntry.grid(row=1, column=1, pady=20)
        self.MediaDelayMenu.grid(row=1, column=2, pady=20)


class SaveMenu(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create variables
        self.toplevel_window = None

        # create functions
        def SaveSettings():
            Settings = Global.Read_Settings()

            Global.Write_Settings(Settings)

        def ApplySettings():
            Settings = Global.Read_Settings()

            print(Settings["comport"])

            if Settings["comport"] == "":
                if (
                    self.toplevel_window is None
                    or not self.toplevel_window.winfo_exists()
                ):
                    self.toplevel_window = ToplevelWindow(
                        self
                    )  # create window if its None or destroyed
                else:
                    self.toplevel_window.focus()  # if window exists focus it

            Global.Write_Settings(Settings)

        # create tabs
        self.add("Save menu")

        # create widgets
        self.SaveButton = customtkinter.CTkButton(
            master=self.tab("Save menu"),
            text="Save settings",
            command=lambda: SaveSettings(),
        )
        self.ApplyButton = customtkinter.CTkButton(
            master=self.tab("Save menu"),
            text="Apply settings\n(might take a while)",
            command=lambda: ApplySettings(),
        )

        self.SaveButton.grid(row=0, column=0, padx=10)
        self.ApplyButton.grid(row=0, column=1, padx=10)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Rose Player Manager")

        if Global.IsBundled():
            self.iconbitmap("_internal/Icons/Rose256.ico")
            self.RosePlayerImage = customtkinter.CTkImage(
                light_image=Image.open("_internal/Images/RosePlayerLight.png"),
                dark_image=Image.open("_internal/Images/RosePlayerDark.png"),
                size=(720, 360),
            )
        else:
            self.iconbitmap("Icons/Rose256.ico")
            self.RosePlayerImage = customtkinter.CTkImage(
                light_image=Image.open("Images/RosePlayerLight.png"),
                dark_image=Image.open("Images/RosePlayerDark.png"),
                size=(720, 360),
            )

        self.image_label = customtkinter.CTkLabel(
            self, image=self.RosePlayerImage, text=""
        )

        self.image_label.grid(row=0, column=0, padx=10, pady=10)

        self.ScreenTabs = ScreenManagement(master=self)
        self.ScreenTabs.grid(row=0, column=1, padx=10, pady=10)

        self.SettingsTabs = GeneralManagement(master=self)
        self.SettingsTabs.grid(row=1, column=0, padx=10, pady=10)

        self.SaveTabs = SaveMenu(master=self)
        self.SaveTabs.grid(row=1, column=1, padx=10, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
