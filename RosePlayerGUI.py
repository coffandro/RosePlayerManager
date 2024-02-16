import customtkinter
import RosePlayerPlaying as Playing
import RosePlayerFuncs as Global
from PIL import Image

# global variables
MultipleScreens = 1
OptionMode1 = "Media info"
OptionMode2 = "Hacker mode"
Settings = {}
Port = ""


class ScreenManagement(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # create tabs
        self.add("Primary mode")
        self.add("Secondary mode")

        # create functions
        def CheckScreenAmount():
            if MultipleScreens == 1:
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

        def ModeMenu2(choice):
            global OptionMode1
            print("optionmenu dropdown clicked:", choice)
            OptionMode1 = choice
        
        def ModeMenu3(choice):
            global OptionMode2
            print("optionmenu dropdown clicked:", choice)
            OptionMode2 = choice

        # add widgets on Primary mode
        self.label1 = customtkinter.CTkLabel(
            master=self.tab("Primary mode"),
            text="What should be displayed in the primary mode?",
        )

        self.optionmenu1 = customtkinter.CTkOptionMenu(
            master=self.tab("Primary mode"),
            values=["Media info", "Hacker mode", "Option 3"],
            command=ModeMenu2,
        )
        self.optionmenu1.set("Media info")

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
            command=ModeMenu3,
        )
        self.optionmenu2.set("Hacker mode")

        self.optionmenu2.grid(row=1, column=0, columnspan=2, padx=20)
        self.label2.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        # refresh
        CheckScreenAmount()


class GeneralManagement(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create variables
        self.OptionsList = Global.GetSerialPorts()
        self.OptionsListShort = Global.GetShortenedSerialPorts()
        try:
            self.CurrentPort = self.OptionsList[-1]
            self.CurrentPortShort = self.OptionsListShort[-1]
        except IndexError:
            self.CurrentPort = "No valid devices connected"
            self.CurrentPortShort = ""

        # create functions
        def ModeMenu1(choice):
            self.CurrentPortShort = self.OptionsListShort[self.OptionsList.index(choice)]
            Port = self.CurrentPortShort

        def TestConnectionButton():
            if self.CurrentPortShort:
                Test = Global.TestSerialPorts(self.CurrentPortShort)
            else:
                self.TestLabel.configure(text="Please connect a device")
            if Test:
                self.TestLabel.configure(text="This is a Rose Player")
            else:
                self.TestLabel.configure(text="This is not a Rose Player")

        def CheckboxEvent():
            global MultipleScreens
            if self.CheckVar.get() == "off":
                MultipleScreens = 0
            else:
                MultipleScreens = 1

        # create tabs
        self.add("General Settings")

        # create widgets
        self.TestLabel = customtkinter.CTkLabel(
            master=self.tab("General Settings"), text="Not tested"
        )

        self.ExplainLabel = customtkinter.CTkLabel(
            master=self.tab("General Settings"),
            text="Select and find a port to connect to",
        )

        self.TestButton = customtkinter.CTkButton(
            master=self.tab("General Settings"),
            text="Test port",
            command=lambda: TestConnectionButton(),
        )

        self.OptionmenuVar = customtkinter.StringVar(value=self.CurrentPort)
        self.OptionMenu = customtkinter.CTkOptionMenu(
            master=self.tab("General Settings"),
            command=ModeMenu1,
            values=self.OptionsList,
            variable=self.OptionmenuVar,
        )

        self.CheckVar = customtkinter.StringVar(value="on")
        self.Checkbox = customtkinter.CTkCheckBox(
            master=self.tab("General Settings"),
            text="Multiple display modes",
            command=CheckboxEvent,
            variable=self.CheckVar,
            onvalue="on",
            offvalue="off",
        )

        # add widgets on tabs
        self.ExplainLabel.grid(row=0, column=0, padx=20)
        self.OptionMenu.grid(row=1, column=0, padx=20)
        self.TestButton.grid(row=2, column=0, padx=20)
        self.TestLabel.grid(row=3, column=0, padx=20)

        self.Checkbox.grid(row=1, column=1, padx=20)

class SaveMenu(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # create functions
        def SaveSettings():
            global Settings
            global Port
            global MultipleScreens
            global OptionMode1
            global OptionMode2

            Settings = {
                "comport": Port,
                "multScreens": MultipleScreens,
                "optionmenu1": OptionMode1,
                "optionmenu2": OptionMode2,
            }

            Global.Write_Settings(Settings)
        
        def ApplySettings():
            Settings = Global.Read_Settings()
            print(Settings)

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
            text="Apply settings",
            command=lambda: ApplySettings(),
        )

        self.SaveButton.grid(row=0, column=0, padx=10)
        self.ApplyButton.grid(row=0, column=1, padx=10)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_default_color_theme("dark-red.json")

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
        self.SettingsTabs.grid(row=1, column=0, pady=10)

        self.SaveTabs = SaveMenu(master=self)
        self.SaveTabs.grid(row=1, column=1, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
