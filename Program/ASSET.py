import tkinter
import tkinter.messagebox
import customtkinter
import os
from PIL import Image

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #load image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(64, 64))

        # configure window
        self.title("ASSET prototype")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="search query")
        self.entry.grid(row=0, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="search button")
        self.main_button_1.grid(row=0, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # viewports container
        self.viewports_container = customtkinter.CTkFrame(self)
        self.viewports_container.grid(row=1, column=0, columnspan=4, padx=0, pady=0, sticky="nsew")
        self.viewports_container.rowconfigure(1, weight=1)

        # render each viewport
        for i in range(6):
            self.viewports_container.columnconfigure(i, weight=1)
            viewport = customtkinter.CTkScrollableFrame(self.viewports_container, label_text="viewport")
            viewport.grid(row=1, column=i, padx=0, pady=0, sticky="nsew")
            image = customtkinter.CTkLabel(self.viewports_container, text="", image=self.test_image)
            image.grid(row=0, column=i, padx=0, pady=0, sticky="nsew")

            for j in range(10):
                result = customtkinter.CTkLabel(master=viewport, text=f"search results {j}")
                result.grid(row=j, column=0, padx=0, pady=0)

if __name__ == "__main__":
    app = App()
    app.mainloop()