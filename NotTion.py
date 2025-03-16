import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import webbrowser
import random
import requests
from io import BytesIO
from PIL import Image, ImageTk
import pygame
from ttkthemes import ThemedTk

class GIFLabel(tk.Label):
    def __init__(self, master, gif_path, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frames = []
        try:
            gif = Image.open(gif_path)
            for frame in range(gif.n_frames):
                gif.seek(frame)
                self.frames.append(ImageTk.PhotoImage(gif.copy()))
            self.frame_index = 0
            self.animate()
        except Exception as e:
            print(f"Failed to load GIF: {e}")

    def animate(self):
        if self.frames:
            self.config(image=self.frames[self.frame_index])
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.after(100, self.animate)


class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Hide the main window initially
        self.root.title("NotTion")
        self.root.geometry("1000x600")

        self.file_path = "autosave.txt"
        self.is_saved = False
        self.premium = False  # Track premium status

        # Initialize pygame for sound
        pygame.mixer.init()

        # Show disclaimer before showing the main app
        self.show_disclaimer()

    def show_disclaimer(self):
        """Show a disclaimer before showing the main app."""
        disclaimer_popup = tk.Toplevel(self.root)
        disclaimer_popup.title("Disclaimer")
        disclaimer_popup.attributes("-topmost", True)  # Keep the disclaimer window on top

        disclaimer_text = (
            "By using this application, you agree to view ads.\n\n"
            "There is a random number of 10 to 100 ads.\n"
            "They are here just to annoy you.\n"
            "Click 'Agree' to continue."
        )

        disclaimer_label = ttk.Label(disclaimer_popup, text=disclaimer_text, font=("Arial", 12), padding=20)
        disclaimer_label.pack()

        agree_button = ttk.Button(disclaimer_popup, text="Agree", command=lambda: self.on_agree(disclaimer_popup))
        agree_button.pack(pady=10)

        # Center the disclaimer window
        disclaimer_popup.update_idletasks()
        width = disclaimer_popup.winfo_width()
        height = disclaimer_popup.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        disclaimer_popup.geometry(f"{width}x{height}+{x}+{y}")

    def on_agree(self, disclaimer_popup):
        """Handle the 'Agree' button click."""
        disclaimer_popup.destroy()
        self.initialize_main_app()  # Initialize and show the main app
        self.show_initial_ads()  # Show initial ads after the user agrees
        self.schedule_ads()  # Schedule ads every 20 seconds

    def initialize_main_app(self):
        """Initialize and show the main application UI."""
        self.root.deiconify()  # Show the main window

        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Toolbar
        self.toolbar = ttk.Frame(self.main_frame)
        self.toolbar.pack(fill="x", pady=5)

        # Toolbar buttons
        new_button = ttk.Button(self.toolbar, text="New", command=self.new_note)
        new_button.pack(side="left", padx=5)

        open_button = ttk.Button(self.toolbar, text="Open", command=self.open_note)
        open_button.pack(side="left", padx=5)

        save_button = ttk.Button(self.toolbar, text="Save", command=self.save_note)
        save_button.pack(side="left", padx=5)

        # Text area for notes
        self.text_area = scrolledtext.ScrolledText(self.main_frame, wrap="word", font=("Arial", 12))
        self.text_area.pack(expand=True, fill="both", padx=5, pady=5)

        # Frame for the GIF
        self.gif_frame = ttk.Frame(self.main_frame)
        self.gif_frame.pack(side="right", padx=10)

        # Load and display GIF on the side
        self.load_gif()

        # Menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_note)
        file_menu.add_command(label="Open", command=self.open_note)
        file_menu.add_command(label="Save", command=self.save_note)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.close_app)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Add Gambling Game to the menu
        game_menu = tk.Menu(self.menu_bar, tearoff=0)
        game_menu.add_command(label="Play Gambling Game", command=self.play_gambling_game)
        self.menu_bar.add_cascade(label="Game", menu=game_menu)

        # Start autosave
        self.auto_save()

        # Mismatched keys dictionary
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.mismatched_keys = {
            'a': random.choice(alphabet),
            'b': random.choice(alphabet),
            'c': random.choice(alphabet),
            'd': random.choice(alphabet),
            'e': random.choice(alphabet),
            'f': random.choice(alphabet),
            'g': random.choice(alphabet),
            'h': random.choice(alphabet),
            'i': random.choice(alphabet),
            'j': random.choice(alphabet),
            'k': random.choice(alphabet),
            'l': random.choice(alphabet),
            'm': random.choice(alphabet),
            'n': random.choice(alphabet),
            'o': random.choice(alphabet),
            'p': random.choice(alphabet),
            'q': random.choice(alphabet),
            'r': random.choice(alphabet),
            's': random.choice(alphabet),
            't': random.choice(alphabet),
            'u': random.choice(alphabet),
            'v': random.choice(alphabet),
            'w': random.choice(alphabet),
            'x': random.choice(alphabet),
            'y': random.choice(alphabet),
            'z': random.choice(alphabet)
        }

        # Bind key press event
        self.text_area.bind("<KeyPress>", self.handle_key_press)

        # Override the default close behavior
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def play_gambling_game(self):
        """Play the gambling game."""
        result = random.choices(["rickroll", "premium"], weights=[99, 1])[0]
        if result == "rickroll":
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Rickroll video
            messagebox.showinfo("Result", "You got Rickrolled!")
        else:
            self.premium = True
            messagebox.showinfo("Result", "Congratulations! You won premium status! Ads are now disabled.")
            self.root.after_cancel(self.schedule_ads)  # Cancel scheduled ads

    def show_initial_ads(self):
        if not self.premium:
            num_ads = random.randint(10, 100)  # Random number of ads
            for _ in range(num_ads):
                self.show_ads()

    def schedule_ads(self):
        """Schedule popup ads every 5 seconds."""
        if not self.premium:
            self.show_ads()  # Show an ad
            self.root.after(5000, self.schedule_ads)  # Schedule the next ad

    def handle_key_press(self, event):
        """Handle key press events to output mismatched keys."""
        if event.char in self.mismatched_keys:
            self.text_area.insert(tk.INSERT, self.mismatched_keys[event.char])
            return "break"  # Prevent default behavior

    def load_gif(self):
        try:
            gif_url = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcGVweTBwaGxuODNuNXJkYjBic2lobmdkNzhyeG81dzIyaXcyNDlrbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Fr5LA2RCQbnVp74CxH/giphy.gif"  # Replace with a valid direct GIF URL
            response = requests.get(gif_url)
            response.raise_for_status()

            img_data = BytesIO(response.content)
            gif_label = GIFLabel(self.gif_frame, img_data)
            gif_label.pack()

        except Exception as e:
            print(f"Failed to load GIF: {e}")

    def new_note(self):
        """Clear the text area and reset the file path."""
        self.text_area.delete(1.0, tk.END)
        self.file_path = "autosave.txt"
        self.is_saved = False

    def open_note(self):
        """Open a text file and load its content into the text area."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            self.file_path = file_path
            self.is_saved = True  # Mark as manually saved

    def save_note(self):
        """Save the content of the text area to a file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
            self.file_path = file_path
            self.is_saved = True  # Mark as manually saved
            messagebox.showinfo("Success", "File saved successfully!")

    def auto_save(self):
        """Automatically saves the note every 30 seconds."""
        try:
            with open(self.file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END).strip()
                if content:  # Avoid saving empty files
                    file.write(content)
        except Exception as e:
            print(f"Autosave failed: {e}")

        # Schedule next autosave in 30 seconds
        self.root.after(30000, self.auto_save)

    def show_ads(self):
        """Show a random ad in a popup window."""
        if not self.premium:
            image_urls = [
                "https://www.technologizer.com/wp-content/uploads/2010/05/freeiphone2.jpg",
                "https://pleated-jeans.com/wp-content/uploads/2016/03/Z2opAfu-1.jpg",
                "https://bestlifeonline.com/wp-content/uploads/sites/3/2018/04/8.jpg",
                "https://cdn-images-1.medium.com/fit/t/1600/480/1*p3PWFgyr3YUaRJyAUHym2g.jpeg",
                "https://feldmancreative.com/wp-content/uploads/2013/09/funny-headline12.jpg",
                "https://static.boredpanda.com/blog/wp-content/uploads/2019/10/stupid-funny-newspaper-headlines-19-5db2bdce120d2__700.jpg",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwNZBn1bcyQC9WlUezCYRwDrrk6i034UzoHg&s",
                "https://malwaretips.com/blogs/wp-content/uploads/2014/11/Win-baitstream-biz-virus.jpg",
                "https://byterevel.com/wp-content/uploads/2011/05/congratulations-you-won.png",
                "https://www.technologizer.com/wp-content/uploads/2010/05/freeiphone.jpg",
                "https://i.ytimg.com/vi/6PA4twy0qHw/mqdefault.jpg",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTc8NnOGdQIc6cZ-CWcVNhF_EXbImcE8ZrLzg&s",
                "https://thunderdungeon.com/wp-content/uploads/2025/01/knock-off-brands-4-20250107.jpg",
                "https://dragonspiritnews.org/wp-content/uploads/2023/02/creme-betweens.jpg",
                "https://yourazbraces.com/wp-content/uploads/2024/03/Free-Nintendo-Switch.webp"
            ]

            cat_sounds = [
                "meow1.mp3",
                "meow2.mp3",
                "meow3.mp3"
            ]

            ad_popup = tk.Toplevel(self.root)
            ad_popup.title("Ad")
            ad_popup.attributes("-topmost", True)  # Keep the ad window on top

            random_image_url = random.choice(image_urls)
            try:
                response = requests.get(random_image_url)
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
            except Exception as e:
                print(f"Failed to load image: {e}")
                image = Image.new("RGB", (300, 200), color="gray")

            photo = ImageTk.PhotoImage(image)
            label = tk.Label(ad_popup, image=photo)
            label.photo = photo  # Keep a reference
            label.pack(pady=10)

            close_button = ttk.Button(ad_popup, text="Close", command=lambda win=ad_popup: self.close_ad(win))
            close_button.pack(pady=5)

            img_width, img_height = image.size
            extra_width = 20
            extra_height = 80
            win_width = img_width + extra_width
            win_height = img_height + extra_height

            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            random_x = random.randint(0, max(0, screen_width - win_width))
            random_y = random.randint(0, max(0, screen_height - win_height))

            ad_popup.geometry(f"{win_width}x{win_height}+{random_x}+{random_y}")

            self.play_random_cat_sound(cat_sounds)
            ad_popup.protocol("WM_DELETE_WINDOW", lambda win=ad_popup: self.close_ad(win))

    def close_ad(self, window):
        """Close the ad window and open a random cat video."""
        if not self.premium:
            video_urls = [
                "https://youtu.be/CXJJDxg7Mos?si=GrTT49fqkL45jnIL",
                "https://www.youtube.com/watch?v=ECuuGNt4rqY",
                "https://www.youtube.com/watch?v=LhMwd0JzTXA",
                "https://www.youtube.com/watch?v=6dMjCa0nqK0&pp=ygUTc2tpYmlkaSB0b2lsZXQgc29uZw%3D%3D",
                "https://www.youtube.com/watch?v=gKeBcV513yc"
            ]
            random_videos = random.choice(video_urls)
            webbrowser.open(random_videos)
        window.destroy()

    def play_random_cat_sound(self, cat_sounds):
        """Play a random cat sound from the list."""
        try:
            sound_file = random.choice(cat_sounds)
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Failed to play sound: {e}")

    def close_app(self):
        """Instead of closing, open a cat video in the browser."""
        if not self.premium:
            video_urls = [
                "https://youtu.be/CXJJDxg7Mos?si=GrTT49fqkL45jnIL",
                "https://www.youtube.com/watch?v=ECuuGNt4rqY",
                "https://www.youtube.com/watch?v=LhMwd0JzTXA",
                "https://www.youtube.com/watch?v=6dMjCa0nqK0&pp=ygUTc2tpYmlkaSB0b2lsZXQgc29uZw%3D%3D",
                "https://www.youtube.com/watch?v=gKeBcV513yc"
            ]
            random_videos = random.choice(video_urls)
            webbrowser.open(random_videos)
            messagebox.showinfo("Wait!", "You can't close the app without watching some cat videos!")
        self.root.destroy()


if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Use a modern theme
    app = NoteApp(root)
    root.mainloop()
