import tkinter
import tkinter.messagebox
from typing import List
import customtkinter
import os
import re
from PIL import Image
import requests
from bs4 import BeautifulSoup
import keyboard

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.NUM_ENGINES = 5

        self.SEARCH_LIST = ["Google.com", "Bing.com", "Discord.com/servers"]
        self.SEARCH_LIST += [None] * (self.NUM_ENGINES - len(self.SEARCH_LIST))

        self.IMAGE_LOAD_LIST = ["google.png", "bing.png"]
        self.IMAGE_LOAD_LIST += ["image_icon_light.png"] * (self.NUM_ENGINES - len(self.IMAGE_LOAD_LIST))
        self.IMAGE_LIST = []

        self.NAME_LIST = ["Google", "Bing", "Discord Servers"]
        self.NAME_LIST += ["Default"] * (self.NUM_ENGINES - len(self.NAME_LIST))

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

        def load_image(file_name, size):
            return customtkinter.CTkImage(Image.open(os.path.join(image_path, file_name)), size=(size, size))
        
        # load images list
        for i in range(self.NUM_ENGINES):
            self.IMAGE_LIST.append(load_image(self.IMAGE_LOAD_LIST[i], 48))

        # load plus and minus buttons
            plus_image = load_image("plus.png", 32)
            minus_image = load_image("minus.png", 32)

        # configure window
        self.title("ASSET prototype")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        column_width = 5
        
        # load search bar
        self.entry = customtkinter.CTkEntry(self, placeholder_text="search query")
        self.entry.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # search button
        self.search_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="search button", command=self.press_search)
        self.search_button.grid(row=0, column=4, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # add engine button
        self.add_engine_button = customtkinter.CTkButton(self, fg_color="transparent", text="add", image=plus_image, command = self.add_Engine)
        self.add_engine_button.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")

        # remove engine button
        self.add_engine_button = customtkinter.CTkButton(self, fg_color="transparent", text="remove", image=minus_image, command = self.remove_Engine)
        self.add_engine_button.grid(row=0, column=3, padx=0, pady=0, sticky="nsew")

        # viewports container
        self.viewports_container = customtkinter.CTkFrame(self)
        self.viewports_container.grid(row=1, column=0, columnspan=column_width, padx=0, pady=0, sticky="nsew")
        self.viewports_container.rowconfigure(1, weight=1)
        # for i in range(column_width):
        #     self.viewports_container.columnconfigure(i, weight=1)

        # render each viewport

        self.search_results("")
        keyboard.add_hotkey('enter', lambda: self.press_search())

    def search_results(self,query):
        # Clear previous results
        for widget in self.viewports_container.grid_slaves():
            widget.grid_forget()

        for i in range(self.NUM_ENGINES):
            self.viewports_container.columnconfigure(i, weight=1)
            viewport = customtkinter.CTkScrollableFrame(self.viewports_container, label_text="viewport")
            viewport.grid(row=1, column=i, padx=0, pady=0, sticky="nsew")
            image = customtkinter.CTkLabel(self.viewports_container, text="", image=self.IMAGE_LIST[0])
            image.grid(row=0, column=i, padx=0, pady=0, sticky="nsew")

            if(self.SEARCH_LIST[i] != None):
                results = self.search(f"https://www.{self.SEARCH_LIST[i]}/search?q=",query)
            else:
                results = ["result", "result", "result"]
            viewport.configure(label_text= self.NAME_LIST[i])
            image.configure(image=self.IMAGE_LIST[i])

            #Loop to give results
            for j, result_text in enumerate(results):
                result = customtkinter.CTkLabel(master=viewport, text=f"{j} - {result_text}\n", anchor= "nw", wraplength=round(self.winfo_width()/self.NUM_ENGINES*0.7))
                result.grid(row=j, column=0, padx=0, pady=0, sticky="w")
                #print(round(self.winfo_width()/self.NUM_ENGINES*0.7))

        # Search button is clicked, allows for update to any engine list

    # Search Button
    def press_search(self):
        print(self.entry.get())
        self.search_results(self.entry.get())
    # Changes Mode & Themes

    def button_Mode(self, mode):
        if(mode == 0):
            customtkinter.set_appearance_mode("Light")
        elif(mode == 1):
            customtkinter.set_appearance_mode("Dark")
        elif(mode == 2):
            customtkinter.set_appearance_mode("System")
    def button_Theme(self, theme):
        if (theme == 0):
            customtkinter.set_default_color_theme("blue")
        elif (theme == 1):
            customtkinter.set_default_color_theme("green")
        elif (theme == 2):
            customtkinter.set_default_color_theme("dark-blue")
    #Engine Functions

    def set_Engine(self, name, site, picture):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.SEARCH_LIST.append(site)
        self.IMAGE_LIST.append(customtkinter.CTkImage(Image.open(os.path.join(image_path, picture)), size=(48, 48)))
        self.NAME_LIST.append(name)

    def add_Engine(self):
        self.set_Engine("Default","google.com", "image_icon_light.png")
        self.NUM_ENGINES += 1
        self.search_results(self.entry.get())

    def remove_Engine(self):
        self.NUM_ENGINES -= 1
        self.search_results(self.entry.get())

    # The Search Engines

    def search(self, engine, query):
        url = f"{engine}{query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all(string=re.compile(query))  # Assuming search results are under <h3> tags
        for result in results:
            if result.getText() == "" or result.getText() == None or result.getText() == query:
                results.remove(result)
        return [result.text for result in results]

if __name__ == "__main__":
    app = App()
    app.mainloop()