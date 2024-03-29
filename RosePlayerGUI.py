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

        # create functions
        def topmost(window):
            window.attributes("-topmost", 1)
            window.attributes("-topmost", 0)

        def Recheck_Function(self):
            Global.Search_Ports()
            Settings = Global.Read_Settings()
            if not Settings["comport"] == "":
                self.label.configure(text="There is a \nRose Player connected")
                self.Button1.configure(text="Apply Settings")
                self.Button1.configure(command=lambda: Global.Apply_Settings())

        def Close(window):
            Settings = Global.Read_Settings()
            window.attributes("-topmost", 0)
            window.attributes("-topmost", 1)
            window.destroy()
            print(Settings["comport"])

        self.parent = self.master.master

        self.geometry(f"407x100")
        self.ws = self.parent.winfo_width()
        self.hs = self.parent.winfo_height()
        self.x = self.ws / 2 + 100
        self.y = self.hs / 2 + 100
        self.geometry("+%d+%d" % (self.x, self.y))

        self.label = customtkinter.CTkLabel(
            self, text="There is no \nRose Player connected"
        )
        self.Button1 = customtkinter.CTkButton(
            self, text="Recheck ports", command=lambda: Recheck_Function(self)
        )
        self.CancelButton = customtkinter.CTkButton(
            self, text="Cancel", command=lambda: Close(self)
        )

        self.label.grid(row=0, column=1)
        self.CancelButton.grid(row=1, column=0)
        self.Button1.grid(row=1, column=2)

        self.grab_set()

        self.after(200, lambda: topmost(self))


class ScreenManagement(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # create tab
        self.add("Primary mode")
        self.add("Secondary mode")

        # create functions
        def CheckScreenAmount():
            Settings = Global.Read_Settings()
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
            values=[
                "Media info",
                "Hacker mode",
            ],
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
            values=["Media info", "Hacker mode"],
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
            print(Settings)
            Global.Write_Settings(Settings)

        def MediaDelayButtonAction():
            Settings = Global.Read_Settings()
            DelayNum = self.MediaDelayEntry.get()
            DelayFormat = self.MediaDelayMenu.get()
            try:
                DelayNum = int(DelayNum)
                if DelayFormat == "Sec":
                    Settings["RefreshDelay"] = int(DelayNum)
                elif DelayFormat == "Min":
                    Settings["RefreshDelay"] = int(DelayNum * 60)
                elif DelayFormat == "Hour":
                    Settings["RefreshDelay"] = int(DelayNum * 60 * 60)

                print(Settings)
                Settings["RefreshDelaySet"] = True
                Settings["RefreshDelayFormat"] = DelayFormat

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

        self.MediaDelayLabel = customtkinter.CTkLabel(
            master=self.tab("General Settings"),
            text="Refresh rate:",
            font=("Roboto", 13, "bold"),
        )
        self.MediaDelayEntry = customtkinter.CTkEntry(
            master=self.tab("General Settings"),
            placeholder_text="A number",
            width=85,
        )
        if Settings["RefreshDelayFormat"] == "Sec":
            self.MediaDelayEntry.insert(0, int(Settings["RefreshDelay"]))
        elif Settings["RefreshDelayFormat"] == "Min":
            self.MediaDelayEntry.insert(0, int(Settings["RefreshDelay"] / 60))
        elif Settings["RefreshDelayFormat"] == "Hour":
            self.MediaDelayEntry.insert(0, int(Settings["RefreshDelay"] / 60 / 60))

        self.MediaDelayMenu_var = customtkinter.StringVar(
            value=Settings["RefreshDelayFormat"]
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
        self.Checkbox.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

        self.MediaDelayLabel.grid(row=1, column=0, pady=0)
        self.MediaDelayEntry.grid(row=1, column=1, pady=0)
        self.MediaDelayMenu.grid(row=1, column=2, pady=0)
        self.MediaDelayButton.grid(row=2, column=0, columnspan=3)


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
            Global.Apply_Settings()

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
            else:
                Global.Apply_Settings()

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
        self.geometry("1100x575")
        self.w = self.winfo_reqwidth()
        self.h = self.winfo_reqheight()
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws / 4) - (self.w / 4)
        self.y = (self.hs / 4) - (self.h / 4)
        self.geometry("+%d+%d" % (self.x, self.y))

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

        self.SettingsTabs = GeneralManagement(master=self, height=160)
        self.SettingsTabs.grid(row=1, column=0, padx=10, pady=10)

        self.SaveTabs = SaveMenu(master=self, height=160)
        self.SaveTabs.grid(row=1, column=1, padx=10, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
