import tkinter
import tkinter.messagebox
from typing import List
import customtkinter
import os
from PIL import Image
import requests
from bs4 import BeautifulSoup

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

NUM_ENGINES = 4

SEARCH_LIST = ["Google.com", "Bing.com", "Discord.com/servers"]
SEARCH_LIST += [None] * (NUM_ENGINES - len(SEARCH_LIST))

IMAGE_LOAD_LIST = ["google.png", "bing.png"]
IMAGE_LOAD_LIST += ["image_icon_light.png"] * (NUM_ENGINES - len(IMAGE_LOAD_LIST))
IMAGE_LIST = []

NAME_LIST = ["Google", "Bing", "Discord Servers"]
NAME_LIST += ["Default"] * (NUM_ENGINES - len(NAME_LIST))

query = ""
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # load images list
        for i in range(NUM_ENGINES):
            image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
            IMAGE_LIST.append(customtkinter.CTkImage(Image.open(os.path.join(image_path, IMAGE_LOAD_LIST[i]))))

        # configure window
        self.title("ASSET prototype")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # load search bar
        self.entry = customtkinter.CTkEntry(self, placeholder_text="search query")
        self.entry.grid(row=0, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # load button
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="search button", command=self.press_search)
        self.main_button_1.grid(row=0, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # viewports container
        self.viewports_container = customtkinter.CTkFrame(self)
        self.viewports_container.grid(row=1, column=0, columnspan=4, padx=0, pady=0, sticky="nsew")
        self.viewports_container.rowconfigure(1, weight=1)

        # render each viewport

        self.search_results(query)

    def search_results(self,query):
        # Clear previous results
        for widget in self.viewports_container.grid_slaves():
            widget.grid_forget()

        for i in range(NUM_ENGINES):
            self.viewports_container.columnconfigure(i, weight=1)
            viewport = customtkinter.CTkScrollableFrame(self.viewports_container, label_text="viewport")
            viewport.grid(row=1, column=i, padx=0, pady=0, sticky="nsew")
            image = customtkinter.CTkLabel(self.viewports_container, text="", image=IMAGE_LIST[0])
            image.grid(row=0, column=i, padx=0, pady=0, sticky="nsew")

            #
            if(SEARCH_LIST[i] != None):
                results = self.search(f"https://www.{SEARCH_LIST[i]}/search?q=",query)
            viewport.configure(label_text= NAME_LIST[i])
            image.configure(image=IMAGE_LIST[i])

            if (query == ""):
                results = ["result", "result", "result"]

            #Loop to give results
            for j, result_text in enumerate(results):
                result = customtkinter.CTkLabel(master=viewport, text=f"{j} - {result_text}\n", anchor= "nw", wraplength=250)
                result.grid(row=j, column=0, padx=0, pady=0, sticky="w")

        # Search button is clicked, allows for update to any engine list

    # Search Button
    def press_search(self):
        print(self.entry.get())
        self.search_results(self.entry.get())

    # The Search Engines

    def search(self, engine, query):
        url = f"{engine}{query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('h3')  # Assuming search results are under <h3> tags
        return [result.text for result in results]

if __name__ == "__main__":
    app = App()
    app.mainloop()