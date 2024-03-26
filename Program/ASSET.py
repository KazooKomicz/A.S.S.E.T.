import tkinter
import tkinter.messagebox
import customtkinter
import os
from PIL import Image
import requests
from bs4 import BeautifulSoup

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #load images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(64, 64))
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.google_logo = customtkinter.CTkImage(Image.open(os.path.join(image_path, "google.png")), size=(64, 64))
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.bing_logo = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bing.png")), size=(64, 64))

        # configure window
        self.title("ASSET prototype")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # create search bar and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="search query")
        self.entry.grid(row=0, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="search button", command=self.press_search)
        self.main_button_1.grid(row=0, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # viewports container
        self.viewports_container = customtkinter.CTkFrame(self)
        self.viewports_container.grid(row=1, column=0, columnspan=4, padx=0, pady=0, sticky="nsew")
        self.viewports_container.rowconfigure(1, weight=1)

        # render each viewport
        query = ""
        self.update_search_results(query)

    def update_search_results(self, query):
        # Clear previous results
        for widget in self.viewports_container.grid_slaves():
            widget.grid_forget()

        # render each viewport
        for i in range(4):
            self.viewports_container.columnconfigure(i, weight=1)
            viewport = customtkinter.CTkScrollableFrame(self.viewports_container, label_text="viewport")
            viewport.grid(row=1, column=i, padx=0, pady=0, sticky="nsew")
            image = customtkinter.CTkLabel(self.viewports_container, text="", image=self.test_image)
            image.grid(row=0, column=i, padx=0, pady=0, sticky="nsew")

            if(i == 0 and query != ""):
                results = self.google_search(query)
                viewport.configure(label_text="Google")
                image.configure(image=self.google_logo)
            elif(i == 1 and query != ""):
                results = self.bing_search(query)
                viewport.configure(label_text="Bing")
                image.configure(image=self.bing_logo)
            else:
                results = ["result", "result", "result"]
            for j, result_text in enumerate(results):
                result = customtkinter.CTkLabel(master=viewport, text=f"{j} - {result_text}\n", anchor= "nw", wraplength=250)
                result.grid(row=j, column=0, padx=0, pady=0, sticky="w")

    def press_search(self):
        print(self.entry.get())
        self.update_search_results(self.entry.get())

    def google_search(self, query):
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('h3')  # Assuming search results are under <h3> tags
        return [result.text for result in results]
    
    def bing_search(self, query):
        url = f"https://www.bing.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('h2')  # Assuming search results are under <h2> tags
        return [result.text for result in results]

if __name__ == "__main__":
    app = App()
    app.mainloop()