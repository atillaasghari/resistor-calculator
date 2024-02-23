import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class ResistorCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Resistor Calculator")

        self.image_label = ttk.Label(root)
        self.image_label.grid(row=1, column=4, rowspan=6, padx=5, pady=5)

        self.num_bands_label = ttk.Label(root, text="Number of Bands:")
        self.num_bands_label.grid(row=0, column=1, padx=5, pady=5)

        self.num_bands_var = tk.IntVar(value=4)  # Default value
        self.num_bands_combo = ttk.Combobox(root, textvariable=self.num_bands_var, values=[3, 4, 5, 6], state="readonly")
        self.num_bands_combo.grid(row=0, column=2, padx=5, pady=5)
        self.num_bands_combo.bind("<<ComboboxSelected>>", self.update_band_colors)

        self.color_labels = []
        self.color_vars = []
        self.color_combos = []

        self.update_band_colors()

        self.calculate_button = ttk.Button(root, text="Calculate", command=self.calculate_resistance)
        self.calculate_button.grid(row=7, column=1, columnspan=2, padx=5, pady=5)

        self.result_label = ttk.Label(root, text="")
        self.result_label.grid(row=8, column=1, columnspan=2, padx=5, pady=5)

    def update_band_colors(self, event=None):
        num_bands = self.num_bands_var.get()

        # Clear previous band color selectors
        for label in self.color_labels:
            label.grid_forget()
        for combo in self.color_combos:
            combo.grid_forget()
        self.color_labels.clear()
        self.color_vars.clear()
        self.color_combos.clear()

        # Create new band color selectors
        for i in range(num_bands):
            label_text = f"Band {i+1} Color:"
            if i == 3:
                label_text = "Multiplier Color:"
            elif i == 4:
                label_text = "Tolerance Color:"
            elif num_bands == 6 and i == 5:
                label_text = "Temperature Coefficient Color:"
            label = ttk.Label(self.root, text=label_text)
            label.grid(row=i+1, column=1, padx=5, pady=5)
            self.color_labels.append(label)

            var = tk.StringVar(value="Black")  # Default value
            if i == 3:
                combo = ttk.Combobox(self.root, textvariable=var, values=list(multiplier.keys()), state="readonly")
            elif i == 4:
                combo = ttk.Combobox(self.root, textvariable=var, values=list(tolerance_values.keys()), state="readonly")
            elif num_bands == 6 and i == 5:
                combo = ttk.Combobox(self.root, textvariable=var, values=temp_coeff_colors, state="readonly")
            else:
                combo = ttk.Combobox(self.root, textvariable=var, values=list(color_code.keys()), state="readonly")
            combo.grid(row=i+1, column=2, padx=5, pady=5)
            self.color_vars.append(var)
            self.color_combos.append(combo)

        # Update image when the number of bands changes
        self.update_image()

    def update_image(self):
        num_bands = self.num_bands_var.get()
        image_path = image_paths.get(num_bands)
        if image_path:
            try:
                image = Image.open(image_path)
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo
            except FileNotFoundError:
                print(f"Image file not found: {image_path}")
        else:
            print(f"Image path not found for {num_bands} bands")

    def calculate_resistance(self):
        num_bands = self.num_bands_var.get()
        bands = [self.color_vars[i].get() for i in range(num_bands)]
    
        if num_bands == 3:
            value = color_code[bands[0]] * 10 + color_code[bands[1]]
            tolerance = tolerance_values[bands[2]]
        elif num_bands == 4:
            value = (color_code[bands[0]] * 10 + color_code[bands[1]]) * multiplier[bands[2]]
            tolerance = tolerance_values[bands[3]]
        elif num_bands == 5:
            value = (color_code[bands[0]] * 100 + color_code[bands[1]] * 10 + color_code[bands[2]]) * multiplier[bands[3]]
            tolerance = tolerance_values[bands[4]]
        elif num_bands == 6:
            value = (color_code[bands[0]] * 100 + color_code[bands[1]] * 10 + color_code[bands[2]]) * multiplier[bands[3]]
            tolerance = tolerance_values[bands[4]]

        else:
            value = 0
            tolerance = 0

        # Convert to kiloohms if the value is too large
        if value >= 1000:
            value /= 1000
            unit = "kΩ"
        else:
            unit = "Ω"

        value_with_tolerance = f"{value} {unit} ±{tolerance}%"
        self.result_label.config(text=value_with_tolerance)


# Resistor color code mapping
color_code = {
    "Black": 0, "Brown": 1, "Red": 2, "Orange": 3, "Yellow": 4,
    "Green": 5, "Blue": 6, "Violet": 7, "Gray": 8, "White": 9,
    "Gold": -1, "Silver": -2  # -1 for Gold and -2 for Silver as they are special cases
}

# Resistance multiplier mapping
multiplier = {
    "Black": 1, "Brown": 10, "Red": 100, "Orange": 1000, "Yellow": 10000,
    "Green": 100000, "Blue": 1000000, "Violet": 10000000, "Gray": 100000000, "White": 1000000000,
    "Gold": 0.1, "Silver": 0.01
}

# Tolerance values
tolerance_values = {
    "Brown": 1, "Red": 2, "Green": 0.5, "Blue": 0.25, "Violet": 0.1,
    "Orange": 0.05 ,"Gray": 0.01, "Gold": 5, "Silver": 10, "Yellow": 0.02
}

# Temperature coefficient colors
temp_coeff_colors = ["Black", "Brown", "Red", "Orange", "Yellow", "Green", "Blue", "Violet", "Gray"]

# Image paths
current_dir = os.path.dirname(os.path.abspath(__file__))
image_paths = {
    3: os.path.join(current_dir, "assets\\img\\3-band.png"),
    4: os.path.join(current_dir, "assets\\img\\4-band.png"),
    5: os.path.join(current_dir, "assets\\img\\5-band.png"),
    6: os.path.join(current_dir, "assets\\img\\6-band.png")
}


if __name__ == "__main__":
    root = tk.Tk()
    app = ResistorCalculator(root)
    root.mainloop()
