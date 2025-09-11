import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

class JonesWaveplateAnimation:
    def __init__(self, J_in, J_out, freq=1.0, wavelength=1.0, ncycles=2, samples_per_cycle=200):
        """
        J_in : complex 2-element Jones vector for input wave
        J_out: complex 2-element Jones vector for output wave
        freq : frequency in Hz
        wavelength : wavelength (arbitrary units)
        ncycles : number of wavelengths to display in each segment
        samples_per_cycle : resolution per wavelength
        """
        self.J_in = np.asarray(J_in, dtype=complex).reshape(2)
        self.J_out = np.asarray(J_out, dtype=complex).reshape(2)
        self.freq = freq
        self.wavelength = wavelength
        self.k = 2*np.pi / wavelength
        self.omega = 2*np.pi * freq

        # Z axes for input and output
        self.z_in = np.linspace(-ncycles*wavelength, 0, ncycles*samples_per_cycle)
        self.z_out = np.linspace(0, ncycles*wavelength, ncycles*samples_per_cycle)

        # Amplitudes and phases
        self.Ax_in, self.phix_in = np.abs(self.J_in[0]), np.angle(self.J_in[0])
        self.Ay_in, self.phiy_in = np.abs(self.J_in[1]), np.angle(self.J_in[1])
        self.Ax_out, self.phix_out = np.abs(self.J_out[0]), np.angle(self.J_out[0])
        self.Ay_out, self.phiy_out = np.abs(self.J_out[1]), np.angle(self.J_out[1])

    def field_segment(self, z, Ax, phix, Ay, phiy, t):
        Ex = Ax * np.cos(self.k*z - self.omega*t - phix)
        Ey = Ay * np.cos(self.k*z - self.omega*t - phiy)
        return Ex, Ey

    def animate(self, frames=100, interval=50, repeat=True, title="Wave through Waveplate"):
        fig = plt.figure(figsize=(10,6))
        ax = fig.add_subplot(111, projection='3d')

        # Draw semi-transparent waveplate as a plane at z=0
        maxAmp = 1.2 * max(self.Ax_in, self.Ay_in, self.Ax_out, self.Ay_out)
        Ex_plane = np.array([[-maxAmp, maxAmp], [-maxAmp, maxAmp]])
        Ey_plane = np.array([[-maxAmp, -maxAmp], [maxAmp, maxAmp]])
        Z_plane = np.zeros_like(Ex_plane)
        ax.plot_surface(Z_plane, Ex_plane, Ey_plane, color='orange', alpha=0.3, label='Waveplate')

        # Initial fields
        Ex_in, Ey_in = self.field_segment(self.z_in, self.Ax_in, self.phix_in, self.Ay_in, self.phiy_in, 0.0)
        Ex_out, Ey_out = self.field_segment(self.z_out, self.Ax_out, self.phix_out, self.Ay_out, self.phiy_out, 0.0)
        line_in, = ax.plot(self.z_in, Ex_in, Ey_in, lw=2, label="Input wave")
        line_out, = ax.plot(self.z_out, Ex_out, Ey_out, lw=2, label="Output wave")

        # Set limits
        ax.set_xlim(self.z_in.min(), self.z_out.max())
        ax.set_ylim(-maxAmp, maxAmp)
        ax.set_zlim(-maxAmp, maxAmp)
        ax.set_xlabel("z (propagation)")
        ax.set_ylabel("E_x")
        ax.set_zlabel("E_y")
        ax.set_title(title)
        ax.legend()

        def update(frame):
            t = frame / frames * (2*np.pi/self.omega) * 5
            Ex_in, Ey_in = self.field_segment(self.z_in, self.Ax_in, self.phix_in, self.Ay_in, self.phiy_in, t)
            Ex_out, Ey_out = self.field_segment(self.z_out, self.Ax_out, self.phix_out, self.Ay_out, self.phiy_out, t)
            line_in.set_data(self.z_in, Ex_in)
            line_in.set_3d_properties(Ey_in)
            line_out.set_data(self.z_out, Ex_out)
            line_out.set_3d_properties(Ey_out)
            return line_in, line_out

        ani = FuncAnimation(fig, update, frames=frames, interval=interval, blit=False, repeat=repeat)
        plt.show()
        return ani


