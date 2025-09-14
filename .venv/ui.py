import tkinter as tk
from tkinter import messagebox
from stokes_to_jones import StokesToJones
from waveplate import Waveplate
from wave_waveplate_wave import JonesWaveplateAnimation

# ---------------------------- CONSTANTS ------------------------------- #
BG_COLOR = "#fffaf5"
ACCENT_COLOR = "#a29bfe"
HEADER_COLOR = "#ffb8b8"
FONT_MAIN = ("Comic Sans MS", 12)
FONT_HEADER = ("Comic Sans MS", 14, "bold")
FONT_TITLE = ("Comic Sans MS", 26, "bold")


class PolarizationUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Polarization & Waveplate Selector")
        self.root.config(bg=BG_COLOR, padx=20, pady=20)

        # --- Stokes state dropdown ---
        tk.Label(root, text="Common States of Polarization of Light",
                 font=FONT_TITLE, bg=BG_COLOR).pack(pady=(0, 20))

        self.states_dict = {
            "Linearly Polarized (Horizontal)": (1, 1, 0, 0),
            "Linearly Polarized (Vertical)": (1, -1, 0, 0),
            "Linearly Polarized (+45°)": (1, 0, 1, 0),
            "Linearly Polarized (-45°)": (1, 0, -1, 0),
            "Right Hand Circularly Polarized": (1, 0, 0, 1),
            "Left Hand Circularly Polarized": (1, 0, 0, -1),
            "Other (Custom)": None
        }

        self.selected_state = tk.StringVar()
        self.selected_state.set("Linearly Polarized (Horizontal)")

        self.dropdown = tk.OptionMenu(
            root, self.selected_state, *self.states_dict.keys(),
            command=self.dropdown_changed
        )
        self.dropdown.config(font=FONT_MAIN, bg=ACCENT_COLOR, relief="flat")
        self.dropdown.pack(pady=10)

        # Custom entries for Stokes (hidden by default)
        self.custom_frame = tk.Frame(root, bg=BG_COLOR)
        self.entries = {}
        for s in ["S0", "S1", "S2", "S3"]:
            frame = tk.Frame(self.custom_frame, bg=BG_COLOR)
            frame.pack(pady=2, fill="x")
            tk.Label(frame, text=f"{s}:", font=FONT_MAIN, bg=BG_COLOR).pack(side="left")
            entry = tk.Entry(frame, font=FONT_MAIN, width=10)
            entry.pack(side="left", padx=5)
            self.entries[s] = entry

        self.submit_btn = tk.Button(
            self.custom_frame, text="Submit Custom", font=FONT_MAIN,
            bg=ACCENT_COLOR, relief="flat", padx=10, pady=5,
            command=self.submit_custom
        )
        self.submit_btn.pack(pady=10)

        # Output label for Stokes parameters
        self.output_label = tk.Label(
            root, text="Selected Stokes Parameters: None",
            font=FONT_HEADER, bg=BG_COLOR, fg="black", wraplength=400
        )
        self.output_label.pack(pady=20)

        self.stokes_params = None
        self.dropdown_changed(self.selected_state.get())

        # --- Waveplate dropdown ---
        tk.Label(root, text="Choose a Waveplate to Transform:", font=FONT_HEADER, bg=BG_COLOR).pack(pady=(20, 5))

        self.waveplates_dict = {
            "Half Wave Plate": "HWP",
            "Quarter Wave Plate": "QWP",
            "Linear Polarizer": "POL"
        }

        self.selected_waveplate = tk.StringVar()
        self.selected_waveplate.set("Half Wave Plate")

        self.waveplate_dropdown = tk.OptionMenu(
            root, self.selected_waveplate, *self.waveplates_dict.keys()
        )
        self.waveplate_dropdown.config(font=FONT_MAIN, bg=ACCENT_COLOR, relief="flat")
        self.waveplate_dropdown.pack(pady=5)

        # Theta input
        theta_frame = tk.Frame(root, bg=BG_COLOR)
        theta_frame.pack(pady=5)
        tk.Label(theta_frame, text="Enter θ (degrees):", font=FONT_MAIN, bg=BG_COLOR).pack(side="left")
        self.theta_entry = tk.Entry(theta_frame, font=FONT_MAIN, width=10)
        self.theta_entry.pack(side="left", padx=5)

        # Button to "apply" waveplate selection
        self.apply_waveplate_btn = tk.Button(
            root, text="Apply Waveplate", font=FONT_MAIN,
            bg=ACCENT_COLOR, relief="flat", padx=10, pady=5,
            command=self.apply_waveplate
        )
        self.apply_waveplate_btn.pack(pady=10)

        # Output label for waveplate
        self.waveplate_output_label = tk.Label(
            root, text="Selected Waveplate: None", font=FONT_HEADER, bg=BG_COLOR, fg="black", wraplength=400
        )
        self.waveplate_output_label.pack(pady=10)

    # --------------------- FUNCTIONS --------------------- #
    def dropdown_changed(self, value):
        if self.states_dict[value] is None:
            self.custom_frame.pack(pady=10)
            self.stokes_params = None
        else:
            self.custom_frame.pack_forget()
            self.stokes_params = self.states_dict[value]
            self.output_label.config(text=f"Selected Stokes Parameters: {self.stokes_params}")

    def submit_custom(self):
        try:
            S0 = float(self.entries["S0"].get())
            S1 = float(self.entries["S1"].get())
            S2 = float(self.entries["S2"].get())
            S3 = float(self.entries["S3"].get())

            if S1 == 0 and S2 == 0 and S3 == 0:
                messagebox.showerror("Error", "Cannot normalize unpolarized light. Please try again.")
                return
            if S0 == 0:
                messagebox.showerror("Error", "S0 cannot be 0. Please enter a valid Stokes vector.")
                return

            self.stokes_params = (S0, S1, S2, S3)
            self.output_label.config(text=f"Selected Stokes Parameters: {self.stokes_params}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for S0, S1, S2, and S3.")

    def apply_waveplate(self):
        waveplate = self.selected_waveplate.get()
        theta_str = self.theta_entry.get()

        try:
            theta = float(theta_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value for θ.")
            return

        # Store stokes and theta in variables
        selected_stokes = self.stokes_params
        selected_theta = theta

        sj = StokesToJones()
        jones_vector_1 = sj.stokes_to_jones(selected_stokes)
        waveplate_input = Waveplate()


# Conditional logic for waveplates
        if waveplate == "Half Wave Plate":
            jones_vector_2 = waveplate_input.hwp_transform(jones_vector_1, selected_theta)
        elif waveplate == "Quarter Wave Plate":
            jones_vector_2 = waveplate_input.qwp_transform(jones_vector_1, selected_theta)
        elif waveplate == "Linear Polarizer":
            jones_vector_2 = waveplate_input.linear_polarize(jones_vector_1, selected_theta)

        waveplate_sim = JonesWaveplateAnimation(jones_vector_1, jones_vector_2, freq=1.0, wavelength=1.0, ncycles=10)
        waveplate_sim.animate(title="Wave Passing Through Waveplate")


# ---------------------------- RUN APP ------------------------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = PolarizationUI(root)
    root.mainloop()
