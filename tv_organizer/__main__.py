import os
import re
import shutil
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import defaultdict

# --- Core Logic ---

def get_organization_plan(directory):
    """Scans a directory and returns a plan for organizing files."""
    if not os.path.isdir(directory):
        return None, f"Error: Directory not found at '{directory}'"

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        return None, "No files to organize in the selected directory."

    season_pattern = re.compile(r'(\d{2})x\d{2}')
    actions = defaultdict(list)
    
    for filename in files:
        match = season_pattern.search(filename)
        if match:
            season_number = match.group(1)
            folder_name = "Specials" if season_number == "00" else f"Season {season_number}"
            actions[folder_name].append(filename)

    if not actions:
        return None, "No files with the expected season format (e.g., '08x01') were found."
        
    return actions, None

# --- CLI Implementation ---

def run_cli(args):
    """Executes the organization logic based on command-line arguments."""
    if not args.directory:
        print("Error: The 'directory' argument is required for CLI mode.")
        return

    actions, error = get_organization_plan(args.directory)

    if error:
        print(error)
        return

    if args.dry_run:
        print("--- Dry Run Report ---")
        print("The following actions would be taken:\n")
        for folder, file_list in actions.items():
            print(f"Create folder: '{folder}' and move {len(file_list)} file(s):")
            for file in file_list:
                print(f"  - {file}")
            print()
        return

    if args.only_create_folders:
        folders_created_count = 0
        print("--- Creating Folders Only ---")
        for folder_name in actions.keys():
            folder_path = os.path.join(args.directory, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                folders_created_count += 1
                print(f"Created folder: {folder_path}")
        print(f"\n{folders_created_count} new season folder(s) created.")
        return
        
    # Default action: move files
    organized_count = 0
    print("--- Organizing Files ---")
    for folder_name, file_list in actions.items():
        season_folder_path = os.path.join(args.directory, folder_name)
        if not os.path.exists(season_folder_path):
            os.makedirs(season_folder_path)
        
        for filename in file_list:
            source_path = os.path.join(args.directory, filename)
            destination_path = os.path.join(season_folder_path, filename)
            shutil.move(source_path, destination_path)
            organized_count += 1
            print(f"Moved: {filename} -> {folder_name}/")
    
    print(f"\nSuccessfully organized {organized_count} files.")

# --- GUI Implementation ---

def organize_from_gui(directory, dry_run, only_create_folders):
    """Handles the logic when the 'Organize' button is clicked in the GUI."""
    if not directory:
        messagebox.showerror("Error", "Please select a directory.")
        return

    try:
        actions, error = get_organization_plan(directory)
        if error:
            messagebox.showinfo("Information", error)
            return

        if dry_run:
            report = "Dry Run Report:\n\nThe following actions would be taken:\n\n"
            for folder, file_list in actions.items():
                report += f"Create folder: '{folder}' and move {len(file_list)} file(s) into it:\n"
                for file in file_list:
                    report += f"  - {file}\n"
                report += "\n"
            
            report_window = tk.Toplevel()
            report_window.title("Dry Run Report")
            report_text = tk.Text(report_window, wrap="word", height=20, width=80)
            report_text.insert("1.0", report)
            report_text.config(state="disabled")
            report_text.pack(padx=10, pady=10, expand=True, fill="both")
            return

        if only_create_folders:
            folders_created_count = 0
            for folder_name in actions.keys():
                folder_path = os.path.join(directory, folder_name)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    folders_created_count += 1
            messagebox.showinfo("Success", f"{folders_created_count} new season folder(s) created.")
            return
            
        organized_count = 0
        for folder_name, file_list in actions.items():
            season_folder_path = os.path.join(directory, folder_name)
            if not os.path.exists(season_folder_path):
                os.makedirs(season_folder_path)
            
            for filename in file_list:
                source_path = os.path.join(directory, filename)
                destination_path = os.path.join(season_folder_path, filename)
                shutil.move(source_path, destination_path)
                organized_count += 1
        
        messagebox.showinfo("Success", f"Successfully organized {organized_count} files.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def select_directory(entry):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry.delete(0, tk.END)
        entry.insert(0, folder_selected)

def run_gui():
    """Sets up and runs the Tkinter GUI."""
    root = tk.Tk()
    root.title("TV Show Organizer")
    root.geometry("450x200")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(expand=True, fill=tk.BOTH)

    dir_label = tk.Label(frame, text="Select the directory containing your TV show files:")
    dir_label.pack(pady=(0, 5), anchor="w")

    entry_frame = tk.Frame(frame)
    entry_frame.pack(fill=tk.X, expand=True)

    dir_entry = tk.Entry(entry_frame)
    dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2)

    browse_button = tk.Button(entry_frame, text="Browse...", command=lambda: select_directory(dir_entry))
    browse_button.pack(side=tk.RIGHT, padx=(5, 0))

    dry_run_var = tk.BooleanVar()
    only_create_folders_var = tk.BooleanVar()

    checkbox_frame = tk.Frame(frame)
    checkbox_frame.pack(fill=tk.X, pady=5)

    def on_dry_run_toggle():
        if dry_run_var.get():
            only_create_folders_check.config(state="disabled")
        else:
            only_create_folders_check.config(state="normal")

    dry_run_check = tk.Checkbutton(checkbox_frame, text="Dry Run (Show plan, no changes)", variable=dry_run_var, command=on_dry_run_toggle)
    dry_run_check.pack(anchor="w")

    only_create_folders_check = tk.Checkbutton(checkbox_frame, text="Only Create Season Folders", variable=only_create_folders_var)
    only_create_folders_check.pack(anchor="w")
    
    organize_button = tk.Button(
        frame, 
        text="Organize Files", 
        command=lambda: organize_from_gui(dir_entry.get(), dry_run_var.get(), only_create_folders_var.get())
    )
    organize_button.pack(pady=(10, 0), ipady=4, fill=tk.X)

    root.mainloop()

def main():
    parser = argparse.ArgumentParser(description="Organize TV show files into season folders.")
    parser.add_argument(
        "directory", 
        nargs='?', 
        default=None,
        help="The directory to organize. Required for CLI mode."
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the graphical user interface."
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Show what changes would be made without actually moving files."
    )
    parser.add_argument(
        "--only-create-folders", 
        action="store_true", 
        help="Only create the season folders without moving files."
    )
    
    args = parser.parse_args()

    if args.gui:
        run_gui()
    elif args.directory:
        run_cli(args)
    else:
        # If no directory and no --gui flag, show help and suggest --gui
        parser.print_help()
        print("\nFor the graphical interface, run with the --gui flag.")


if __name__ == "__main__":
    main()