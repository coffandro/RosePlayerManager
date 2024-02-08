import customtkinter
import RosePlayerPlaying as Playing
import RosePlayerPorts as Ports

# import RosePlayerSettings as Settings
from PIL import Image


class ScreenManagement(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Primary mode")
        self.add("Secondary mode")

        # create functions
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


class GeneralManagement(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create variables
        self.OptionsList = Ports.GetSerialPorts()
        self.OptionsListShort = Ports.GetShortenedSerialPorts()
        self.CurrentPort = self.OptionsListShort[-1]

        # create functions
        def ModeMenu1(choice):
            self.CurrentPort = self.OptionsListShort[self.OptionsList.index(choice)]
            print("index:", self.CurrentPort)

        def TestConnectionButton():
            Test = Ports.TestSerialPorts(self.CurrentPort)
            if Test == True:
                self.TestLabel.configure(text="This is a Rose Player")
            else:
                self.TestLabel.configure(text="This is not a Rose Player")

        # create tabs
        self.add("General Settings")

        # create widgets
        self.TestLabel = customtkinter.CTkLabel(
            self.tab("General Settings"), text="Not tested"
        )

        self.ExplainLabel = customtkinter.CTkLabel(
            self.tab("General Settings"), text="Select and find a port to connect to"
        )

        self.TestButton = customtkinter.CTkButton(
            self.tab("General Settings"),
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

        # add widgets on tabs
        self.ExplainLabel.grid(row=0, column=0, padx=20)
        self.OptionMenu.grid(row=1, column=0, padx=20)
        self.TestButton.grid(row=2, column=0, padx=20)
        self.TestLabel.grid(row=3, column=0, padx=20)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.iconbitmap("Icons/Rose256.ico")
        self.title("Rose Player Manager")

        self.RosePlayerImage = customtkinter.CTkImage(
            light_image=Image.open("Images/RosePlayerLight.png"),
            dark_image=Image.open("Images/RosePlayerDark.png"),
            size=(640, 360),
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
