import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Resistor color code mapping
color_code = {
    "Black": 0, "Brown": 1, "Red": 2, "Orange": 3, "Yellow": 4,
    "Green": 5, "Blue": 6, "Violet": 7, "Gray": 8, "White": 9,
    "Gold": 10, "Silver": 11
}

# Resistance multiplier mapping
multiplier = {
    "Black": 1, "Brown": 10, "Red": 100, "Orange": 1000, "Yellow": 10000,
    "Green": 100000, "Blue": 1000000, "Violet": 10000000, "Gray": 100000000, "White": 1000000000,
    "Gold": 0.1, "Silver": 0.01
}

# Tolerance colors
tolerance_colors = ["Brown", "Red", "Orange", "Yellow", "Green", "Blue", "Violet", "Gray", "Gold", "Silver"]

# Temperature coefficient colors
temp_coeff_colors = ["Black", "Brown", "Red", "Orange", "Yellow", "Green", "Blue", "Violet", "Gray"]

# Image paths
image_paths = {
    3: "C:/Users/atsl/Desktop/projects/python/resistor-calculator/assets/img/3-band.png",
    4: "C:/Users/atsl/Desktop/projects/python/resistor-calculator/assets/img/4-band.png",
    5: "C:/Users/atsl/Desktop/projects/python/resistor-calculator/assets/img/5-band.png",
    6: "C:/Users/atsl/Desktop/projects/python/resistor-calculator/assets/img/6-band.png"
}

class ResistorCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Resistor Calculator")

        self.image_label = tk.Label(root)
        self.image_label.grid(row=1, column=4, rowspan=6, padx=5, pady=5)

        self.num_bands_label = ttk.Label(root, text="Number of Bands:")
        self.num_bands_label.grid(row=0, column=1, padx=5, pady=5)

        self.num_bands_var = tk.IntVar(value=3)  # Default value
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
            if num_bands == 3 and i == 2:
                label_text = "Multiplier Color:"
            elif num_bands == 4 and i == 2:
                label_text = "Multiplier Color:"
            elif num_bands >= 4 and i == 3:
                label_text = "Tolerance Color:"
            elif num_bands == 6 and i == 5:
                label_text = "Temperature Coefficient Color:"
            label = ttk.Label(self.root, text=label_text)
            label.grid(row=i+1, column=1, padx=5, pady=5)
            self.color_labels.append(label)

            var = tk.StringVar(value="Black")  # Default value
            if num_bands == 3 and i == 2:
                combo = ttk.Combobox(self.root, textvariable=var, values=list(multiplier.keys()), state="readonly")
            elif num_bands == 4 and i == 2:
                combo = ttk.Combobox(self.root, textvariable=var, values=list(multiplier.keys()), state="readonly")
            elif num_bands >= 4 and i == 3:
                combo = ttk.Combobox(self.root, textvariable=var, values=tolerance_colors, state="readonly")
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
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
        else:
            print(f"Image path not found for {num_bands} bands")

    def calculate_resistance(self):
        num_bands = self.num_bands_var.get()
        bands = [self.color_vars[i].get() for i in range(num_bands)]
        value = sum(color_code[bands[i]] * 10**(num_bands-i-2) for i in range(num_bands-1)) * multiplier[bands[num_bands-1]]
        tolerance = "±" + str(color_code[bands[-1]]) + "%"
        if num_bands == 3:
            result_text = f"{value} Ω {tolerance} ({bands[2]})"
        elif num_bands == 4:
            result_text = f"{value} Ω {tolerance} ({bands[2]}) ({bands[3]})"
        elif num_bands == 5 or num_bands == 6:
            result_text = f"{value} Ω {tolerance} ({bands[3]}) ({bands[4]})"
        self.result_label.config(text=result_text)      

if __name__ == "__main__":
    root = tk.Tk()
    app = ResistorCalculator(root)
    root.mainloop()
