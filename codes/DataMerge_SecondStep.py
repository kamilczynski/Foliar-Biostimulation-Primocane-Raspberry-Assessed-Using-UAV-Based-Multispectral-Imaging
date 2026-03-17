import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox


def choose_input_directory():
    folder_path = filedialog.askdirectory(title="Select the folder with CSV files")
    if folder_path:
        input_field.delete(0, tk.END)
        input_field.insert(0, folder_path)


def choose_output_path():
    file_path = filedialog.asksaveasfilename(
        title="Save the resulting CSV file",
        defaultextension=".csv",
        filetypes=[("CSV", "*.csv")]
    )
    if file_path:
        output_field.delete(0, tk.END)
        output_field.insert(0, file_path)


def load_csv_data(directory, file_list):
    return [
        pd.read_csv(os.path.join(directory, filename))
        for filename in file_list
    ]


def merge_csv_files():
    source_dir = input_field.get()
    target_file = output_field.get()

    if not source_dir:
        messagebox.showerror("Error", "No input folder selected")
        return

    if not target_file:
        messagebox.showerror("Error", "No output file selected")
        return

    csv_list = [
        name for name in os.listdir(source_dir)
        if name.lower().endswith(".csv")
    ]

    if not csv_list:
        messagebox.showerror("Error", "No CSV files in the folder")
        return

    dataframes = load_csv_data(source_dir, csv_list)

    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.to_csv(target_file, index=False)

    messagebox.showinfo(
        "Ready",
        f"Merged {len(csv_list)} files\n"
        f"Number of rows: {len(combined_df)}\n\n"
        f"Save to:\n{target_file}"
    )


# =========================
# GUI
# =========================

root = tk.Tk()
root.title("Merge all CSV files")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Folder wejściowy
tk.Label(frame, text="Folder with CSV files:").grid(row=0, column=0, sticky="w")
input_field = tk.Entry(frame, width=60)
input_field.grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame, text="Select folder", command=choose_input_directory)\
    .grid(row=1, column=1, padx=5)

# Plik wyjściowy
tk.Label(frame, text="CSV output file:").grid(row=2, column=0, sticky="w")
output_field = tk.Entry(frame, width=60)
output_field.grid(row=3, column=0, padx=5, pady=5)
tk.Button(frame, text="Select file", command=choose_output_path)\
    .grid(row=3, column=1, padx=5)

# Start
tk.Button(
    frame,
    text="Merge all into one CSV",
    command=merge_csv_files,
    height=2
).grid(row=4, column=0, columnspan=2, pady=15)

root.mainloop()
