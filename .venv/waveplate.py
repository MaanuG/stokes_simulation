import numpy as np

class Waveplate:
    def choose_waveplate(self, jones_vector):
        print("Choose a Waveplate to Transform: ")
        print("1) Half Wave Plate")
        print("2) Quarter Wave Plate")
        waveplate_input = int(input("Enter the number of the waveplate you wish to use: "))
        if waveplate_input == 1:
            transformed_jones_vector = self.hwp_transform(jones_vector)
        if waveplate_input == 2:
            transformed_jones_vector = self.qwp_transform(jones_vector)
        return transformed_jones_vector
    def qwp_transform(self,jones_vector, theta=0):
        """
        Transforms a Jones vector through a quarter-wave plate (QWP).

        Parameters:
            jones_vector : array-like
                2-element complex array representing the Jones vector [Ex, Ey].
            theta : float
                Angle of the QWP fast axis relative to x-axis in radians (default=0).

        Returns:
            np.ndarray
                Transformed Jones vector after passing through the QWP.
        """
        # Jones matrix for QWP at angle theta
        c, s = np.cos(theta), np.sin(theta)

        # Rotation matrices
        R = np.array([[c, -s],
                      [s,  c]])
        R_inv = np.array([[c, s],
                          [-s, c]])

        # QWP in its principal axes (phase shift of pi/2 along y-axis)
        QWP = np.array([[1, 0],
                        [0, 1j]])

        # Total transformation
        transformed = R_inv @ QWP @ R @ jones_vector
        return transformed

    def hwp_transform(self, jones_vector, theta=0):
        """
        Transform a Jones vector through a half-wave plate.

        Parameters:
        jones_vector : np.array of shape (2,)
            Input Jones vector [Ex, Ey].
        theta_deg : float
            Angle of the HWP fast axis with respect to x-axis in degrees.

        Returns:
        np.array
            Output Jones vector after the half-wave plate.
        """
        J_hwp = np.array([
            [np.cos(2*theta), np.sin(2*theta)],
            [np.sin(2*theta), -np.cos(2*theta)]
        ])

        # Apply HWP to input Jones vector
        return J_hwp @ jones_vector


