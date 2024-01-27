import customtkinter
import RosePlayerPlaying as Playing
from PIL import Image


class ScreenManagement(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Primary mode")
        self.add("Secondary mode")

        # create functions
        def ModeMenu1(choice):
            print("optionmenu dropdown clicked:", choice)

        # add widgets on Primary mode
        self.label = customtkinter.CTkLabel(
            master=self.tab("Primary mode"),
            text="What should be displayed in the primary mode?",
        )

        self.optionmenu = customtkinter.CTkOptionMenu(
            master=self.tab("Primary mode"),
            values=["option 1", "option 2"],
            command=ModeMenu1,
        )
        self.optionmenu.set("option 2")

        self.optionmenu.grid(row=1, column=0, columnspan=2, padx=20)
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        # add widgets on Secondary mode


class GeneralManagement(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("General Settings")

        # add widgets on tabs
        self.label = customtkinter.CTkLabel(master=self.tab("General Settings"))
        self.label.grid(row=0, column=0, padx=20, pady=10)


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
