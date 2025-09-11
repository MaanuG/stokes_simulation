import numpy as np

class StokesToJones():

    def define_stokes_vector(self):
        print("Common States of Polarization of Light")
        print("1) Linearly Polarized (Horizontal)")
        print("2) Linearly Polarized (Vertical)")
        print("3) Linearly Polarized (+45°)")
        print("4) Linearly Polarized (-45°)")
        print("5) Right Hand Circularly Polarized")
        print("6) Left Hand Circularly Polarized")
        print("7) Other")
        state_input = int(input("Enter the number of the state you wish to use: "))

        if state_input == 1:
            self.stoke_params = (1, 1, 0, 0)
        elif state_input == 2:
            self.stoke_params = (1, -1, 0, 0)
        elif state_input == 3:
            self.stoke_params = (1, 0, 1, 0)
        elif state_input == 4:
            self.stoke_params = (1, 0, -1, 0)
        elif state_input == 5:
            self.stoke_params = (1, 0, 0, 1)
        elif state_input == 6:
            self.stoke_params = (1, 0, 0, -1)
        elif state_input == 7:
            S0 = input("Enter S0: ")
            S1 = input("Enter S1: ")
            S2 = input("Enter S2: ")
            S3 = input("Enter S3: ")
            while S1 == 0 and S2 == 0 and S3 ==0:
                print("Sorry, you cannot normalize unpolarized light. Enter again. ")
                S0 = input("Enter S0: ")
                S1 = input("Enter S1: ")
                S2 = input("Enter S2: ")
                S3 = input("Enter S3: ")
            self.stoke_params = (S0,S1,S2,S3)
        return self.stoke_params
    
    def stokes_to_jones(self,S):
        """
        Convert a Stokes vector [S0, S1, S2, S3] to a Jones vector [z1, z2].
        Fully polarized case only.
        
        Parameters
        ----------
        S : array_like
            Stokes vector (S0, S1, S2, S3).
        
        Returns
        -------
        jones : np.ndarray
            Complex Jones vector [z1, z2], scaled so that |z1|^2 + |z2|^2 = S0.
        """
        S0, S1, S2, S3 = S
    
        # Normalize polarization part
        s1, s2, s3 = S1/S0, S2/S0, S3/S0
    
        # Handle the south pole case (s3 = -1)
        if np.isclose(s3, -1.0):
            jones = np.array([1j, 0.0], dtype=complex)
        else:
            denom = np.sqrt(2 * (1 + s3))
            z1 = (s1 + 1j*s2) / denom
            z2 = np.sqrt((1 + s3) / 2.0)
            jones = np.array([z1, z2], dtype=complex)
    
        # Scale so total power matches S0
        norm = np.abs(jones[0])**2 + np.abs(jones[1])**2
        jones *= np.sqrt(S0 / norm)
    
        return jones

