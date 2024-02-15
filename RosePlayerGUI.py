import customtkinter
import RosePlayerPlaying as Playing
import RosePlayerFuncs as Global
# import RosePlayerSettings as Settings
from PIL import Image

# global variables
MultipleScreens = 1


class ScreenManagement(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # create tabs
        self.add("Primary mode")
        # if MultipleScreens == 1:
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
            print("optionmenu dropdown clicked:", choice)

        # add widgets on Primary mode
        self.label = customtkinter.CTkLabel(
            master=self.tab("Primary mode"),
            text="What should be displayed in the primary mode?",
        )

        self.optionmenu = customtkinter.CTkOptionMenu(
            master=self.tab("Primary mode"),
            values=["option 1", "option 2"],
            command=ModeMenu2,
        )
        self.optionmenu.set("option 2")

        self.optionmenu.grid(row=1, column=0, columnspan=2, padx=20)
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        # add widgets on Secondary mode

        # refresh
        CheckScreenAmount()


class GeneralManagement(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create variables
        self.OptionsList = Global.GetSerialPorts()
        self.OptionsListShort = Global.GetShortenedSerialPorts()
        self.CurrentPort = self.OptionsListShort[-1]

        # create functions
        def ModeMenu1(choice):
            self.CurrentPort = self.OptionsListShort[self.OptionsList.index(choice)]

        def TestConnectionButton():
            Test = Global.TestSerialPorts(self.CurrentPort)
            if Test == True:
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

        self.OptionmenuVar = customtkinter.StringVar(value=self.OptionsList[-1])
        self.OptionMenu = customtkinter.CTkOptionMenu(
            master=self.tab("General Settings"),
            command=ModeMenu1,
            values=self.OptionsList,
            variable=self.OptionmenuVar,
        )

        self.CheckVar = customtkinter.StringVar(value="on")
        self.Checkbox = customtkinter.CTkCheckBox(
            master=self.tab("General Settings"),
            text="Multiple displays",
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


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        if Global.IsBundled():
            self.iconbitmap("_internal/Icons/Rose256.ico")
        else:    
            self.iconbitmap("Icons/Rose256.ico")
        self.title("Rose Player Manager")

        self.RosePlayerImage = customtkinter.CTkImage(
            light_image=Image.open("Images/RosePlayerLight.png"),
            dark_image=Image.open("Images/RosePlayerDark.png"),
            size=(720, 360),
        )

        self.image_label = customtkinter.CTkLabel(
            self, image=self.RosePlayerImage, text=""
        )  # display the Rose player image

        self.image_label.grid(row=0, column=0, padx=10, pady=10)

        self.ScreenTabs = ScreenManagement(master=self)
        self.ScreenTabs.grid(row=0, column=1, padx=10, pady=10)

        self.SettingsTabs = GeneralManagement(master=self)
        self.SettingsTabs.grid(row=1, columnspan=2, column=0, padx=1, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
