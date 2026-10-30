import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image


class ImageCompressorApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Python Batch Image Compressor")
    self.root.geometry("550x450")
    self.root.resizable(False, False)

    # Variables
    self.input_dir = tk.StringVar()
    self.output_dir = tk.StringVar()
    self.quality_var = tk.IntVar(value=70)

    self.create_widgets()

  def create_widgets(self):
    # Title Label
    title_label = tk.Label(
        self.root, text="Image Compression Tool", font=("Arial", 16, "bold")
    )
    title_label.pack(pady=15)

    # Frame for Inputs
    frame = tk.Frame(self.root, padx=20, pady=10)
    frame.pack(fill="x", expand=True)

    # Input Folder Selection
    tk.Label(frame, text="Input Folder:", font=("Arial", 10, "bold")).grid(
        row=0, column=0, sticky="w", pady=5
    )
    tk.Entry(
        frame, textvariable=self.input_dir, width=40, font=("Arial", 10)
    ).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(
        frame, text="Browse", command=self.select_input_folder, width=8
    ).grid(row=0, column=2, pady=5)

    # Output Folder Selection
    tk.Label(frame, text="Output Folder:", font=("Arial", 10, "bold")).grid(
        row=1, column=0, sticky="w", pady=5
    )
    tk.Entry(
        frame, textvariable=self.output_dir, width=40, font=("Arial", 10)
    ).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(
        frame, text="Browse", command=self.select_output_folder, width=8
    ).grid(row=1, column=2, pady=5)

    # Quality Slider
    tk.Label(frame, text="Quality (1-100):", font=("Arial", 10, "bold")).grid(
        row=2, column=0, sticky="w", pady=15
    )
    quality_slider = tk.Scale(
        frame,
        from_=10,
        to=100,
        orient="horizontal",
        variable=self.quality_var,
        length=270,
    )
    quality_slider.grid(row=2, column=1, columnspan=2, sticky="w", pady=15)

    # Start Button
    self.start_btn = tk.Button(
        self.root,
        text="Start Compression",
        command=self.start_thread,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 11, "bold"),
        width=20,
        height=2,
    )
    self.start_btn.pack(pady=10)

    # Status / Log Box
    self.status_box = tk.Text(
        self.root, height=8, width=60, state="disabled", font=("Courier", 9)
    )
    self.status_box.pack(pady=10)

  def select_input_folder(self):
    folder = filedialog.askdirectory()
    if folder:
      self.input_dir.set(folder)

  def select_output_folder(self):
    folder = filedialog.askdirectory()
    if folder:
      self.output_dir.set(folder)

  def log_message(self, message):
    self.status_box.config(state="normal")
    self.status_box.insert(tk.END, message + "\n")
    self.status_box.see(tk.END)
    self.status_box.config(state="disabled")

  def start_thread(self):
    in_dir = self.input_dir.get()
    out_dir = self.output_dir.get()

    if not in_dir or not out_dir:
      messagebox.showerror(
          "Error", "Please select both input and output folders!"
      )
      return

    # Disable button during processing
    self.start_btn.config(state="disabled", text="Processing...")
    self.status_box.config(state="normal")
    self.status_box.delete("1.0", tk.END)
    self.status_box.config(state="disabled")

    # Run in background thread to keep GUI responsive
    threading.Thread(
        target=self.compress_images, args=(in_dir, out_dir), daemon=True
    ).start()

  def compress_images(self, input_folder, output_folder):
    quality = self.quality_var.get()
    tasks = []

    for root, _, files in os.walk(input_folder):
      for file in files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
          input_path = os.path.join(root, file)
          relative_path = os.path.relpath(root, input_folder)
          dest_dir = os.path.join(output_folder, relative_path)
          output_filename = os.path.splitext(file)[0] + ".jpg"
          output_path = os.path.join(dest_dir, output_filename)
          tasks.append((input_path, output_path))

    total_files = len(tasks)
    if total_files == 0:
      self.log_message("No supported images found in the input folder.")
      self.reset_ui()
      return

    self.log_message(
        f"Found {total_files} images. Starting compression at quality"
        f" {quality}..."
    )

    total_orig, total_comp = 0, 0
    success_count = 0

    for input_path, output_path in tasks:
      try:
        with Image.open(input_path) as img:
          # Handle transparency for PNGs
          if img.mode in ("RGBA", "LA") or (
              img.mode == "P" and "transparency" in img.info
          ):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.convert("RGBA").split()[3])
            img = background
          else:
            img = img.convert("RGB")

          os.makedirs(os.path.dirname(output_path), exist_ok=True)
          img.save(output_path, "JPEG", quality=quality, optimize=True)

          orig_size = os.path.getsize(input_path)
          comp_size = os.path.getsize(output_path)
          total_orig += orig_size
          total_comp += comp_size
          success_count += 1
      except Exception as e:
        self.log_message(
            f"Failed: {os.path.basename(input_path)} -> Error: {e}"
        )

    # Summary Report
    self.log_message("\n--- Compression Complete ---")
    self.log_message(f"Successfully processed: {success_count}/{total_files}")
    if total_orig > 0:
      saved = total_orig - total_comp
      self.log_message(
          f"Original Size: {total_orig / (1024*1024):.2f} MB"
      )
      self.log_message(
          f"Compressed Size: {total_comp / (1024*1024):.2f} MB"
      )
      self.log_message(
          f"Total Saved: {saved / (1024*1024):.2f} MB"
          f" ({saved/total_orig*100:.1f}%)"
      )

    self.reset_ui()
    messagebox.showinfo("Success", "All images have been successfully compressed!")

  def reset_ui(self):
    self.start_btn.config(state="normal", text="Start Compression")


if __name__ == "__main__":
  root = tk.Tk()
  app = ImageCompressorApp(root)
  root.mainloop()