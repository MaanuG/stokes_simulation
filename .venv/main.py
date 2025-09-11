from stokes_to_jones import StokesToJones
from visualize import JonesWave3D
from waveplate import Waveplate
from wave_waveplate_wave import JonesWaveplateAnimation
# call StokesToJones to create jones vector
sj = StokesToJones()
stokes_vector = sj.define_stokes_vector()
jones_vector = sj.stokes_to_jones(stokes_vector)
print(jones_vector)
# animate independently jones vector 1
wave1 = JonesWave3D(jones_vector)
wave1.animate_with_ellipse()

# transform jones vector 1 with waveplate
waveplate = Waveplate()
new_jones_vector = waveplate.choose_waveplate(jones_vector)
# animate independently jones vector 2
wave2 = JonesWave3D(new_jones_vector)
wave2.animate_with_ellipse()
# show continuous animation of wave passing through waveplate to polarize
waveplate_sim = JonesWaveplateAnimation(jones_vector, new_jones_vector, freq=1.0, wavelength=1.0, ncycles=10)
waveplate_sim.animate(title="Wave Passing Through Waveplate")


