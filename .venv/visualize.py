import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class JonesWave3D:
    def __init__(self, J, freq=1.0, wavelength=1.0, ncycles=2, samples_per_cycle=200):
        """
        J : complex 2-element Jones vector [Ex, Ey]
        freq : frequency in Hz
        wavelength : wavelength (arbitrary units)
        ncycles : number of wavelengths to display along z
        samples_per_cycle : resolution per wavelength
        """
        self.J = np.asarray(J, dtype=complex).reshape(2)
        self.freq = freq
        self.wavelength = wavelength
        self.k = 2 * np.pi / wavelength
        self.omega = 2 * np.pi * freq

        self.z = np.linspace(0, ncycles * wavelength, ncycles * samples_per_cycle)

        # Jones vector components
        self.Ax, self.phix = np.abs(self.J[0]), np.angle(self.J[0])
        self.Ay, self.phiy = np.abs(self.J[1]), np.angle(self.J[1])

    def field_along_z(self, t=0.0):
        """Compute E_x(z), E_y(z) at fixed time t"""
        Ex = self.Ax * np.cos(self.k * self.z - self.omega * t - self.phix)
        Ey = self.Ay * np.cos(self.k * self.z - self.omega * t - self.phiy)
        return Ex, Ey

    def polarization_ellipse(self, samples=200):
        """Compute stationary polarization ellipse at z=0"""
        t = np.linspace(0, 2*np.pi/self.omega, samples)
        Ex = self.Ax * np.cos(-self.omega*t - self.phix)
        Ey = self.Ay * np.cos(-self.omega*t - self.phiy)
        return Ex, Ey

    def animate_with_ellipse(self, frames=100, interval=50, repeat=True, title="3D Jones Wave with Ellipse"):
        """Animate propagating wave along z with a stationary polarization ellipse at z=0"""
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Stationary ellipse
        Ex_ell, Ey_ell = self.polarization_ellipse()
        ax.plot(np.zeros_like(Ex_ell), Ex_ell, Ey_ell, 'r--', label='Polarization ellipse (stationary)')

        # Initial propagating wave
        Ex, Ey = self.field_along_z(0.0)
        line, = ax.plot(self.z, Ex, Ey, lw=2, label="Propagating wave")

        # Set limits
        maxAmp = 1.2 * max(self.Ax, self.Ay)
        ax.set_xlim(0, self.z.max())
        ax.set_ylim(-maxAmp, maxAmp)
        ax.set_zlim(-maxAmp, maxAmp)
        ax.set_xlabel("z (propagation)")
        ax.set_ylabel("E_x")
        ax.set_zlabel("E_y")
        ax.set_title(title)
        ax.legend()

        def update(frame):
            t = frame / frames * (2 * np.pi / self.omega) * 5  # ~5 periods
            Ex, Ey = self.field_along_z(t)
            line.set_data(self.z, Ex)
            line.set_3d_properties(Ey)
            return line,

        ani = FuncAnimation(fig, update, frames=frames, interval=interval, blit=False, repeat=repeat)
        plt.show()
        return ani


