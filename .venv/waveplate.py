import numpy as np
import math

class Waveplate:
    def choose_waveplate(self, jones_vector):
        print("Choose a Waveplate to Transform: ")
        print("1) Half Wave Plate")
        print("2) Quarter Wave Plate")
        print("3) Linear Polarizer")
        waveplate_input = int(input("Enter the number of the waveplate you wish to use: "))

        if waveplate_input == 1:
            theta_input = float(input("Enter theta value for HWP (degrees): "))
            transformed_jones_vector = self.hwp_transform(jones_vector, theta_input*math.pi/180)
        elif waveplate_input == 2:
            theta_input = float(input("Enter theta value for QWP (degrees): "))
            transformed_jones_vector = self.qwp_transform(jones_vector, theta_input*math.pi/180)
        elif waveplate_input == 3:
            theta_input = float(input("Enter theta value for polarizer (degrees): "))
            transformed_jones_vector = self.linear_polarize(jones_vector, theta_input*math.pi/180)
        else:
            raise ValueError("Invalid input. Choose 1, 2, or 3.")

        return transformed_jones_vector

    def qwp_transform(self, jones_vector, theta=0):
        c, s = np.cos(theta), np.sin(theta)
        R = np.array([[c, -s],
                      [s,  c]])
        R_inv = np.array([[c, s],
                          [-s, c]])
        QWP = np.array([[1, 0],
                        [0, 1j]])
        return R_inv @ QWP @ R @ jones_vector

    def hwp_transform(self, jones_vector, theta=0):
        c, s = np.cos(theta), np.sin(theta)
        R = np.array([[c, -s],
                      [s,  c]])
        R_inv = np.array([[c, s],
                          [-s, c]])
        HWP = np.array([[1, 0],
                        [0, -1]])
        return R_inv @ HWP @ R @ jones_vector

    def linear_polarize(self, jones_vector, theta=0):
        c, s = np.cos(theta), np.sin(theta)
        P = np.array([[c**2, c*s],
                      [c*s,  s**2]], dtype=complex)
        return P @ jones_vector
