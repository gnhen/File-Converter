import os
import sys
import winreg
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from pathlib import Path
import json
from typing import Dict, List
import threading
import ffmpeg
from PIL import Image
import pypdf
import ebooklib
from ebooklib import epub
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


class FileFormatRegistry:
    def __init__(self):
        self.formats = {
            "audio": {
                "extensions": [".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac", ".wma"],
                "converter": self.convert_audio,
            },
            "video": {
                "extensions": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
                "converter": self.convert_video,
            },
            "image": {
                "extensions": [
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".gif",
                    ".bmp",
                    ".tiff",
                    ".webp",
                ],
                "converter": self.convert_image,
            },
            "document": {
                "extensions": [
                    ".pdf",
                    ".epub",
                    ".mobi",
                    ".txt",
                    ".doc",
                    ".docx",
                    ".rtf",
                ],
                "converter": self.convert_document,
            },
        }

    def get_supported_formats(self, file_extension: str) -> List[str]:
        file_extension = file_extension.lower()
        for category in self.formats.values():
            if file_extension in category["extensions"]:
                return [ext for ext in category["extensions"] if ext != file_extension]
        return []

    def convert_audio(self, input_path: str, output_path: str) -> bool:
        try:
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(stream, output_path)
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            return True
        except ffmpeg.Error:
            return False

    def convert_video(self, input_path: str, output_path: str) -> bool:
        try:
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(stream, output_path)
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            return True
        except ffmpeg.Error:
            return False

    def convert_image(self, input_path: str, output_path: str) -> bool:
        try:
            with Image.open(input_path) as img:
                img.save(output_path)
            return True
        except Exception:
            return False

    def convert_document(self, input_path: str, output_path: str) -> bool:
        try:
            input_ext = Path(input_path).suffix.lower()
            output_ext = Path(output_path).suffix.lower()

            if input_ext == ".pdf" and output_ext == ".epub":
                self._pdf_to_epub(input_path, output_path)
            elif input_ext == ".epub" and output_ext == ".pdf":
                self._epub_to_pdf(input_path, output_path)
            return True
        except Exception:
            return False

    def _pdf_to_epub(self, input_path: str, output_path: str):
        book = epub.EpubBook()
        pdf_reader = pypdf.PdfReader(input_path)

        for i, page in enumerate(pdf_reader.pages):
            chapter = epub.EpubHtml(title=f"Page {i+1}", file_name=f"page_{i+1}.xhtml")
            chapter.content = f"<html><body>{page.extract_text()}</body></html>"
            book.add_item(chapter)

        book.spine = ["nav"] + book.items
        epub.write_epub(output_path, book)

    def _epub_to_pdf(self, input_path: str, output_path: str):
        book = epub.read_epub(input_path)
        content = []

        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                content.append(item.get_content().decode("utf-8"))

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))


class ModernConverterGUI:
    def __init__(self, input_path: str):
        try:
            self.input_path = input_path
            self.registry = FileFormatRegistry()

            self.root = tk.Tk()
            self.root.title("Format File Converter")
            self.root.geometry("500x600")
            self.root.resizable(False, False)

            self.colors = {
                "bg": "#2E3440",
                "fg": "#ECEFF4",
                "accent": "#88C0D0",
                "hover": "#5E81AC",
                "success": "#A3BE8C",
                "error": "#BF616A",
                "card": "#3B4252",
            }

            self.root.configure(bg=self.colors["bg"])
            self.setup_styles()
            self.setup_gui()

            self.root.report_callback_exception = self.show_error
        except Exception as e:
            self.show_error(type(e), e, e.__traceback__)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Card.TFrame", background=self.colors["card"])

        style.configure(
            "Modern.TLabel",
            background=self.colors["card"],
            foreground=self.colors["fg"],
            font=("Segoe UI", 10),
        )

        style.configure(
            "Header.TLabel",
            background=self.colors["card"],
            foreground=self.colors["fg"],
            font=("Segoe UI", 12, "bold"),
        )

        style.configure(
            "Modern.TButton",
            background=self.colors["accent"],
            foreground=self.colors["fg"],
            font=("Segoe UI", 10),
            padding=10,
        )

        style.map("Modern.TButton", background=[("active", self.colors["hover"])])

        style.configure(
            "Modern.TCombobox",
            background=self.colors["card"],
            foreground=self.colors["fg"],
            fieldbackground=self.colors["card"],
            arrowcolor=self.colors["fg"],
        )

        style.configure(
            "Modern.Horizontal.TProgressbar",
            background=self.colors["accent"],
            troughcolor=self.colors["card"],
        )

    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="20", style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_label = ttk.Label(
            main_frame,
            text="File Format Converter",
            style="Header.TLabel",
            font=("Segoe UI", 16, "bold"),
        )
        title_label.pack(pady=(0, 20))

        file_info = self.create_file_info_widget(main_frame)
        file_info.pack(fill=tk.X, pady=(0, 20))

        input_ext = Path(self.input_path).suffix
        self.supported_formats = self.registry.get_supported_formats(input_ext)

        format_frame = ttk.Frame(main_frame, style="Card.TFrame", padding="20")
        format_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(
            format_frame, text="Select Output Format", style="Header.TLabel"
        ).pack(anchor="w", pady=(0, 10))

        self.format_var = tk.StringVar()
        format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.format_var,
            style="Modern.TCombobox",
            state="readonly",
            width=40,
        )
        format_combo["values"] = self.supported_formats
        format_combo.pack(fill=tk.X, pady=(0, 10))

        self.convert_button = ttk.Button(
            format_frame,
            text="Convert File",
            style="Modern.TButton",
            command=self.convert_file,
        )
        self.convert_button.pack(fill=tk.X, pady=(10, 0))

        progress_frame = ttk.Frame(main_frame, style="Card.TFrame", padding="20")
        progress_frame.pack(fill=tk.X)

        self.status_label = ttk.Label(
            progress_frame, text="Ready to convert", style="Modern.TLabel"
        )
        self.status_label.pack(anchor="w", pady=(0, 10))

        self.progress = ttk.Progressbar(
            progress_frame, style="Modern.Horizontal.TProgressbar", mode="indeterminate"
        )
        self.progress.pack(fill=tk.X)

    def create_file_info_widget(self, parent):
        info_frame = ttk.Frame(parent, style="Card.TFrame", padding="20")

        file_name = Path(self.input_path).name
        ttk.Label(info_frame, text="Input File", style="Header.TLabel").pack(anchor="w")

        ttk.Label(
            info_frame, text=file_name, style="Modern.TLabel", wraplength=400
        ).pack(anchor="w", pady=(5, 10))

        file_type = Path(self.input_path).suffix.upper()[1:]
        ttk.Label(
            info_frame, text=f"Current Format: {file_type}", style="Modern.TLabel"
        ).pack(anchor="w")

        size_bytes = os.path.getsize(self.input_path)
        size_mb = size_bytes / (1024 * 1024)
        ttk.Label(
            info_frame, text=f"Size: {size_mb:.2f} MB", style="Modern.TLabel"
        ).pack(anchor="w", pady=(0, 10))

        return info_frame

    def show_error(self, exc_type, exc_value, exc_traceback):
        error_msg = "".join(
            traceback.format_exception(exc_type, exc_value, exc_traceback)
        )

        error_window = tk.Toplevel(self.root)
        error_window.title("Error Occurred")
        error_window.geometry("600x400")

        text_widget = tk.Text(error_window, wrap=tk.WORD, bg="white", fg="black")
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert("1.0", error_msg)

        button = ttk.Button(error_window, text="Close", command=error_window.destroy)
        button.pack(pady=10)

    def convert_file(self):
        if not self.format_var.get():
            messagebox.showerror("Error", "Please select an output format")
            return

        output_path = Path(self.input_path).with_suffix(self.format_var.get())

        self.convert_button.state(["disabled"])
        self.status_label.configure(text="Converting...")
        self.progress.start()

        thread = threading.Thread(target=self._convert_thread, args=(output_path,))
        thread.start()

    def _convert_thread(self, output_path: Path):
        input_ext = Path(self.input_path).suffix.lower()
        success = False

        for category in self.registry.formats.values():
            if input_ext in category["extensions"]:
                success = category["converter"](self.input_path, str(output_path))
                break

        self.root.after(0, self._conversion_complete, success, output_path)

    def _conversion_complete(self, success: bool, output_path: Path):
        self.progress.stop()
        self.convert_button.state(["!disabled"])

        if success:
            self.status_label.configure(text="Conversion completed successfully!")
            messagebox.showinfo(
                "Success", f"File converted successfully!\nSaved to: {output_path}"
            )
            self.root.after(1000, self.root.destroy)
        else:
            self.status_label.configure(text="Conversion failed")
            messagebox.showerror("Error", "Conversion failed. Please try again.")


def add_context_menu():
    try:
        python_path = sys.executable
        script_path = os.path.abspath(__file__)

        key_path = r"*\\shell\\FormatFile"

        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "Format File")

        command_key_path = f"{key_path}\\command"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_key_path) as key:
            command = f'"{python_path}" "{script_path}" "%1"'
            winreg.SetValue(key, "", winreg.REG_SZ, command)

        return True
    except Exception as e:
        print(f"Error adding context menu: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        if add_context_menu():
            print("Context menu added successfully!")
        else:
            print("Failed to add context menu")
        return

    input_path = sys.argv[1]

    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return

    gui = ModernConverterGUI(input_path)
    gui.root.mainloop()


if __name__ == "__main__":
    main()
