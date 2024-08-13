import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from formatters import format_files
from extractors import extract_html_classes_and_ids, extract_css_classes_and_ids, extract_js_classes
from finders import find_missing_css_classes, find_unused_css_classes, find_unused_css_id_selectors, find_class_id_conflicts, find_duplicated_css_classes
from pathlib import Path
import time
from threading import Thread


# Get the path of the current file
script_dir = Path(__file__).resolve()
# Get the parent directory of the current file
script_current_directory_path = script_dir.parent
# Get the parent directory in str
script_current_directory = str(script_current_directory_path)
# Get the current project Directory Path
project_directory = script_current_directory_path.parent


output_dir = Path(script_current_directory + r"\OutputFiles")
output_dir.mkdir(exist_ok=True)

def gui():
    def run_task(task, task_name):
        progress_window = tk.Toplevel(root)
        progress_window.title(f"Progress - {task_name}")
        
        # Center the text
        progress_label = tk.Label(progress_window, text=f"Processing {task_name}...", anchor="center")
        progress_label.pack(pady=20)
        
        def update_label():
            while True:
                for i in range(4):  # Loop to create animation effect
                    time.sleep(0.5)  # Wait for half a second
                    progress_label.config(text=f"Processing {task_name}" + "." * i)
                if not progress_window.winfo_exists():
                    break

        Thread(target=update_label).start()  # Start the animation in a separate thread
        
        # progress_var = tk.DoubleVar()
        
        # # Center the progress bar
        # progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=100)
        # progress_bar.pack(pady=20, padx=20, fill=tk.X)
        
        def task_wrapper():
            task()
            progress_window.destroy()
        
        root.after(100, task_wrapper)
        
        # Center the progress window
        progress_window.update_idletasks()
        width = 300
        height = 150
        x = (progress_window.winfo_screenwidth() // 2) - (width // 2)
        y = (progress_window.winfo_screenheight() // 2) - (height // 2)
        progress_window.geometry(f"{width}x{height}+{x}+{y}")
        
        progress_window.grab_set()
        root.wait_window(progress_window)

    def format_files_gui():
        run_task(format_files, "Format Files")
        messagebox.showinfo("Format Files", "Files formatted successfully!")

    # def extract_html_classes_and_ids_gui():
    #     run_task(extract_html_classes_and_ids, "Extract HTML Classes and IDs")
    #     messagebox.showinfo("Extract HTML Classes and IDs", "HTML classes and IDs extracted successfully!")

    # def extract_css_classes_and_ids_gui():
    #     run_task(extract_css_classes_and_ids, "Extract CSS Classes and IDs")
    #     messagebox.showinfo("Extract CSS Classes and IDs", "CSS classes and IDs extracted successfully!")

    # def extract_js_classes_gui():
    #     run_task(extract_js_classes, "Extract JS Classes")
    #     messagebox.showinfo("Extract JS Classes", "JS classes extracted successfully!")

    def find_missing_css_classes_gui():
        # Function to run the task and update the progress bar
        def task():
            html_classes, html_ids = extract_html_classes_and_ids()
            
            css_classes, css_ids, css_elements, css_pseudos, css_nested = extract_css_classes_and_ids()
            
            missing_classes = find_missing_css_classes(html_classes, css_classes, css_ids, css_elements, css_pseudos)
            with open(str(output_dir) + 'missing_classes.txt', 'w') as f:
                for cls, locations in missing_classes.items():
                    for location in locations:
                        f.write(f'Class: {cls} - File: {location[0]} - Line: {location[1]}\n')

        # Run the task with a progress variable and bar
        run_task(task, "Find Missing CSS Classes")
        messagebox.showinfo("Find Missing CSS Classes", "Missing CSS classes found and written to missing_classes.txt!")

    def find_unused_css_classes_gui():
        run_task(lambda pv, pb: find_unused_css_classes(extract_html_classes_and_ids(pv, pb)[0], extract_css_classes_and_ids(pv, pb)[4], extract_js_classes(pv, pb)), "Find Unused CSS Classes")
        messagebox.showinfo("Find Unused CSS Classes", "Unused CSS classes found and written to unused_classes.txt!")

    def find_unused_css_id_selectors_gui():
        run_task(lambda pv, pb: find_unused_css_id_selectors(extract_css_classes_and_ids(pv, pb)[1], extract_html_classes_and_ids(pv, pb)[1]), "Find Unused CSS ID Selectors")
        messagebox.showinfo("Find Unused CSS ID Selectors", "Unused CSS ID selectors found and written to unused_ids_selectors.txt!")

    def find_class_id_conflicts_gui():
        run_task(lambda pv, pb: find_class_id_conflicts(extract_html_classes_and_ids(pv, pb)[0], extract_html_classes_and_ids(pv, pb)[1], extract_css_classes_and_ids(pv, pb)[4]), "Find Class-ID Conflicts")
        messagebox.showinfo("Find Class-ID Conflicts", "Class-ID conflicts found and written to conflicts.txt!")

    def find_duplicated_css_classes_gui():
        run_task(lambda pv, pb: find_duplicated_css_classes(extract_css_classes_and_ids(pv, pb)[0], extract_css_classes_and_ids(pv, pb)[1], extract_css_classes_and_ids(pv, pb)[2]), "Find Duplicated CSS Classes")
        messagebox.showinfo("Find Duplicated CSS Classes", "Duplicated CSS classes found and written to duplicated_classes.txt!")

    def browse_output_dir():
        output_dir_path = filedialog.askdirectory()
        if output_dir_path:
            global output_dir
            output_dir = Path(output_dir_path)
            messagebox.showinfo("Output Directory", f"Output directory set to: {output_dir}")

    root = tk.Tk()
    root.title("Website Class and ID Extractor")

    # Set dark mode
    root.configure(bg="#222222")
    root.option_add("*Background", "#222222")
    root.option_add("*Foreground", "#FFFFFF")
    root.option_add("*Button.Background", "#333333")
    root.option_add("*Button.Foreground", "#FFFFFF")
    root.option_add("*Button.ActiveBackground", "#444444")
    root.option_add("*Button.ActiveForeground", "#FFFFFF")

    frame = tk.Frame(root, padx=10, pady=10, bg="#222222")
    frame.pack(padx=10, pady=10)

    # Program Title
    label = tk.Label(frame, text="Website Class and ID Extractor", font=("Arial", 16), bg="#222222", fg="#FFFFFF")
    label.pack(pady=20, anchor="center")
    
    # Display the current project directory
    project_directory_label = tk.Label(frame, text=f"Project Directory: {project_directory}\\", font=("Arial", 10), bg="#222222", fg="#FFFFFF")
    project_directory_label.pack(pady=15, anchor="center")
    
    # Display the current output directory
    output_directory_label = tk.Label(frame, text=f"Output Directory: {str(output_dir)}\\", font=("Arial", 10), bg="#222222", fg="#FFFFFF")
    output_directory_label.pack(pady=15, anchor="center")

    format_files_button = tk.Button(frame, text="Format Files", command=format_files_gui, width=27)
    format_files_button.pack(pady=15, anchor="center")

    find_missing_css_classes_button = tk.Button(frame, text="Find Missing CSS Classes", command=find_missing_css_classes_gui, width=27)
    find_missing_css_classes_button.pack(pady=15, anchor="center")

    find_unused_css_classes_button = tk.Button(frame, text="Find Unused CSS Classes", command=find_unused_css_classes_gui, width=27)
    find_unused_css_classes_button.pack(pady=15, anchor="center")

    find_unused_css_id_selectors_button = tk.Button(frame, text="Find Unused CSS ID Selectors", command=find_unused_css_id_selectors_gui, width=27)
    find_unused_css_id_selectors_button.pack(pady=15, anchor="center")

    find_class_id_conflicts_button = tk.Button(frame, text="Find Class-ID Conflicts", command=find_class_id_conflicts_gui, width=27)
    find_class_id_conflicts_button.pack(pady=15, anchor="center")

    find_duplicated_css_classes_button = tk.Button(frame, text="Find Duplicated CSS Classes", command=find_duplicated_css_classes_gui, width=27)
    find_duplicated_css_classes_button.pack(pady=15, anchor="center")

    browse_output_dir_button = tk.Button(frame, text="Browse Output Directory", command=browse_output_dir, width=27)
    browse_output_dir_button.pack(pady=15, anchor="center")

    # Center the main window and increase its size
    root.update_idletasks()
    width = 1050
    height = 625
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.mainloop()
    
if __name__ == "__main__":
    gui()
