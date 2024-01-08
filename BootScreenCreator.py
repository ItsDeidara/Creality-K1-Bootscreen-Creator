import os
import yt_dlp
from datetime import datetime
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, Label, messagebox, ttk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='#2E2E2E')  # Set background color to dark gray
        self.master = master
        self.master.title("YouTube to GIF Converter")
        self.master.geometry("600x400")  # Set a fixed size for the window
        self.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    
    def create_widgets(self):
        # Metro-style button configuration
        button_style = {
            'bg': '#0078D4',  # Blue color similar to Windows Metro
            'fg': 'white',    # White text color
            'font': ('Segoe UI', 12),
            'borderwidth': 0,
            'highlightthickness': 0,
            'activebackground': '#005A8E',  # Darker blue for active state
        }

        self.notebook = ttk.Notebook(self)

        # Gif2Bootscreen tab
        self.tab1 = tk.Frame(self.notebook, bg='#2E2E2E')
        self.notebook.add(self.tab1, text='Gif2Bootscreen')

        self.label = Label(self.tab1, text="Please select a gif to convert", fg='white', bg='#2E2E2E', font=('Segoe UI', 12))
        self.label.pack(side="top", fill='both', pady=(10, 0))

        self.label_frame = tk.Frame(self.tab1, bg='#2E2E2E')
        self.label_frame.pack(side="top", fill='both', expand=True)

        self.label_frame_label = Label(self.label_frame, bg='#2E2E2E')
        self.label_frame_label.pack(expand=True, fill='both')

        self.convert = tk.Button(self.tab1, text="Start Conversion", command=self.convert_image, **button_style)
        self.convert.pack(side="bottom", pady=(10, 10), padx=20, ipadx=10, ipady=5, anchor='center')

        self.select = tk.Button(self.tab1, text="Select GIF", command=self.select_file, **button_style)
        self.select.pack(side="bottom", pady=(0, 20), padx=20, ipadx=10, ipady=5, anchor='center')

        self.gif_frames = []
        self.current_frame = 0
        self.fps = 30

        # YouTube to Boots GIF tab
        self.tab2 = tk.Frame(self.notebook, bg='#2E2E2E')
        self.notebook.add(self.tab2, text='YouTube to Boots GIF')

        self.url_label = Label(self.tab2, text="Enter YouTube URL:", fg='white', bg='#2E2E2E', font=('Segoe UI', 12))
        self.url_label.pack(side="top", pady=(10, 0))

        self.url_entry = tk.Entry(self.tab2, bg='#2E2E2E', fg='white', font=('Segoe UI', 12))
        self.url_entry.pack(side="top", pady=(0, 20), padx=20, ipadx=10, ipady=5, fill='x')

        self.clear_button = tk.Button(self.tab2, text="Clear", command=self.clear_url_entry, **button_style)
        self.clear_button.pack(side="top", pady=(0, 20), padx=20, ipadx=10, ipady=5, anchor='center')

        self.folder_label = Label(self.tab2, text="Select Save Location:", fg='white', bg='#2E2E2E', font=('Segoe UI', 12))
        self.folder_label.pack(side="top", pady=(10, 0))

        self.folder_entry = tk.Entry(self.tab2, bg='#2E2E2E', fg='white', font=('Segoe UI', 12))
        self.folder_entry.pack(side="top", pady=(0, 20), padx=20, ipadx=10, ipady=5, fill='x')

        self.browse_folder = tk.Button(self.tab2, text="Browse", command=self.browse_folder, **button_style)
        self.browse_folder.pack(side="top", pady=(0, 20), padx=20, ipadx=10, ipady=5, anchor='center')

        self.download_convert_button = tk.Button(self.tab2, text="Download and Convert", command=self.download_and_convert, **button_style)
        self.download_convert_button.pack(side="bottom", pady=(10, 10), padx=20, ipadx=10, ipady=5, anchor='center')

        # YouTube to Boots GIF tab (Third tab)
        self.tab3 = tk.Frame(self.notebook, bg='#2E2E2E')
        self.notebook.add(self.tab3, text='YouTube to Boots GIF')

        self.url_label_tab3 = Label(self.tab3, text="Enter YouTube URL:", fg='white', bg='#2E2E2E', font=('Segoe UI', 12))
        self.url_label_tab3.pack(side="top", pady=(10, 0))

        self.url_entry_tab3 = tk.Entry(self.tab3, bg='#2E2E2E', fg='white', font=('Segoe UI', 12))
        self.url_entry_tab3.pack(side="top", pady=(0, 20), padx=20, ipadx=10, ipady=5, fill='x')

        self.folder_label_tab3 = Label(self.tab3, text="Select Save Location:", fg='white', bg='#2E2E2E', font=('Segoe UI', 12))
        self.folder_label_tab3.pack(side="top", pady=(10, 0))

        self.folder_entry_tab3 = tk.Entry(self.tab3, bg='#2E2E2E', fg='white', font=('Segoe UI', 12))
        self.folder_entry_tab3.pack(side="top", pady=(0, 20), padx=20, ipadx=10, ipady=5, fill='x')

        self.browse_folder_tab3 = tk.Button(self.tab3, text="Browse", command=self.browse_folder_tab3, **button_style)
        self.browse_folder_tab3.pack(side="top", pady=(0, 20), padx=20, ipadx=10, ipady=5, anchor='center')

        self.download_convert_button_tab3 = tk.Button(self.tab3, text="Download and Convert", command=self.download_and_convert_tab3, **button_style)
        self.download_convert_button_tab3.pack(side="bottom", pady=(10, 10), padx=20, ipadx=10, ipady=5, anchor='center')

        self.notebook.pack(fill='both', expand=True)

    def browse_folder_tab3(self):
        folder_selected = filedialog.askdirectory()
        self.folder_entry_tab3.delete(0, tk.END)
        self.folder_entry_tab3.insert(0, folder_selected)

    def download_and_convert_tab3(self):
        url = self.url_entry_tab3.get()
        folder_path = self.folder_entry_tab3.get()

        if not url or not folder_path:
            messagebox.showwarning("Incomplete Information", "Please enter a valid YouTube URL and select a save location.")
            return

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(folder_path, '%(title)s.%(ext)s'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(url, download=True)
                video_title = info_dict.get('title', 'video')
                video_folder = os.path.join(folder_path, video_title)

                if not os.path.exists(video_folder):
                    os.makedirs(video_folder)

                credits_path = os.path.join(video_folder, 'credits.txt')
                with open(credits_path, 'w') as credits_file:
                    credits_file.write(f"YouTube URL: {url}\n")
                    credits_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                # Move downloaded video to the created subfolder
                video_files = [f for f in os.listdir(folder_path) if f.startswith(video_title) and f.endswith(('.mp4', '.mkv', '.webm'))]
                for video_file in video_files:
                    old_path = os.path.join(folder_path, video_file)
                    new_path = os.path.join(video_folder, video_file)
                    os.rename(old_path, new_path)

                # Convert downloaded video to an 800x480 GIF using FFmpeg
                gif_output_path = os.path.join(video_folder, 'output.gif')
                ffmpeg_command = f"ffmpeg -i {os.path.join(video_folder, video_files[0])} -vf 'scale=800:480' {gif_output_path}"
                os.system(ffmpeg_command)

                # Convert the resulting GIF using the same script from the first tab
                ConvertImage(gif_output_path, video_folder)

                # Ask the user if they want to view the converted files
                view_files = messagebox.askyesno("View Files", "Do you want to view the converted files?")

                if view_files:
                    # Open the folder containing the converted files
                    self.open_folder(video_folder)

            except Exception as e:
                messagebox.showerror("Download Error", f"Error during download and conversion: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()
