import math
import scipy
from scipy import constants
from scipy import special


def eirp(power_transmit, loss, gain_transmit):  # dBW, dB, dBi
    return power_transmit - loss + gain_transmit


def g_over_t(gain_receive, noise_temperature):  # dB, dBK
    return gain_receive - 10*math.log10(noise_temperature)


def ebn0(bit_error_rate, modulation):
    # http://140.113.144.123/105%20introduction%20to%20digital%20communications/Unit%201-7%20GMSK.pdf
    # https://www.edn.com/design/communications-design/4017668/3/Modulation-roundup-error-rates-noise-and-capacity
    # PCM/PM/NRZ/SP-L ~= BPSK
    # https://deepspace.jpl.nasa.gov/files/phase1.pdf

    _ebn0 = 0

    if modulation == 'GMSK':
        _ebn0 = 10 * math.log10(((scipy.special.erfcinv(bit_error_rate * 2)) ** 2) / 0.9)
    elif modulation == 'BPSK' or modulation == 'QPSK' or modulation == 'OQPSK' or modulation == 'PCM':
        _ebn0 = 10 * math.log10((scipy.special.erfcinv(bit_error_rate * 2)) ** 2)
    elif modulation == '8PSK' or modulation == '8APSK':
        _ebn0 = 10 * math.log10(((scipy.special.erfcinv(bit_error_rate * math.log2(8))) ** 2) /
                                (math.log2(8) * math.sin(math.pi / 8)))
    elif modulation == '16QAM' or modulation == '16APSK':
        _ebn0 = 10 * math.log10(((scipy.special.erfcinv(bit_error_rate * (8 / 3))) ** 2) * (10 / 4))
        # TODO:  16APSK = Guess
    elif modulation == '16APSK' or modulation == '16PSK':
        _ebn0 = 10 * math.log10(((scipy.special.erfcinv(bit_error_rate * math.log2(16))) ** 2) /
                                (math.log2(16) * math.sin(math.pi / 16)))
        # TODO:  32APSK = Guess
    elif modulation == '32APSK':
        _ebn0 = 10 * math.log10(((scipy.special.erfcinv(bit_error_rate * math.log2(32))) ** 2) /
                                (math.log2(32) * math.sin(math.pi / 32)))
        # TODO:  64APSK = Guess
    elif modulation == '64APSK':
        _ebn0 = 10 * math.log10(((scipy.special.erfcinv(bit_error_rate * math.log2(64))) ** 2) /
                                (math.log2(64) * math.sin(math.pi / 64)))
        # TODO:  128APSK = Guess
    elif modulation == '128APSK':
        _ebn0 = 10 * math.log10(((scipy.special.erfcinv(bit_error_rate * math.log2(128))) ** 2) /
                                (math.log2(128) * math.sin(math.pi / 128)))
        # TODO:  256APSK = Guess
    elif modulation == '256APSK':
        _ebn0 = 10 * math.log10(((scipy.special.erfcinv(bit_error_rate * math.log2(256))) ** 2) /
                                (math.log2(256) * math.sin(math.pi / 256)))

    return _ebn0


def path_loss_troposphere():
    return 0


def path_loss_ionosphere():
    return 0


def path_loss_free_space(distance, frequency):
    _path_loss_free_space = 20 * math.log10((4 * math.pi * distance * frequency) /
                                            scipy.constants.value(u'speed of light in vacuum'))
    return -1*_path_loss_free_space


def slant_range(mean_orbit_altitude, elevation_angle_degrees, object_radius):
    mean_orbit_radius = mean_orbit_altitude + object_radius
    elevation_angle_radians = math.radians(elevation_angle_degrees)
    _slant_range = object_radius * ((((mean_orbit_radius ** 2 / object_radius ** 2) -
                                      (math.cos(elevation_angle_radians)) ** 2) ** 0.5) -
                                    math.sin(elevation_angle_radians))
    return _slant_range


EARTH_RADIUS = 6378*1000
BOLTZMANN = -10*math.log10(scipy.constants.value(u'Boltzmann constant'))

modulated_bit_rate = 100E6
altitude = 1000E3
elevation_angle = 10
center_frequency = 8000E6
implementation_margin = 1
mission_bit_error_rate = 2E-11
coding_gain = 14
ground_station_g_over_t = 20

satellite_slant_range = slant_range(altitude, elevation_angle, EARTH_RADIUS)
minimum_ebn0 = ebn0(mission_bit_error_rate, 'OQPSK')
space_craft_eirp = eirp(20, 2, 10)

c_over_N0 = space_craft_eirp + \
            ground_station_g_over_t + \
            path_loss_free_space(satellite_slant_range, center_frequency) + \
            path_loss_troposphere() + \
            path_loss_troposphere() + \
            BOLTZMANN

ebn0 = c_over_N0 - 10*math.log10(modulated_bit_rate)
link_margin = ebn0 - implementation_margin - minimum_ebn0 + coding_gain

print(c_over_N0)
print(ebn0)
print(link_margin)
