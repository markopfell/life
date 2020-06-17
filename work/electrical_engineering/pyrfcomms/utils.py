import math
import scipy
import numpy
from scipy import constants
from scipy import special
import matplotlib.pyplot as plt


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
        # TODO:  16 APSK = Guess
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


# TODO refine estimate
def path_loss_troposphere(distance, frequency):
    return 0


# TODO refine estimate
def path_loss_ionosphere(distance, frequency):
    return 0


def path_loss_free_space(distance, frequency):
    _path_loss_free_space = 20 * numpy.log10((4 * math.pi * distance * frequency) /
                                             scipy.constants.value(u'speed of light in vacuum'))
    return -1*_path_loss_free_space


def slant_range(mean_orbit_altitude, elevation_angle_degrees, object_radius):
    mean_orbit_radius = mean_orbit_altitude + object_radius
    elevation_angle_radians = math.radians(elevation_angle_degrees)
    _slant_range = object_radius * ((((mean_orbit_radius ** 2 / object_radius ** 2) -
                                      (math.cos(elevation_angle_radians)) ** 2) ** 0.5) -
                                    math.sin(elevation_angle_radians))
    return _slant_range


# http://www.tscm.com/antennas.pdf
def antenna_gain(beamwidths):
    antenna_efficiency = 0.6  # Rectangular area model is more conservative
    beamwidth_theta = beamwidths
    beamwidth_phi = beamwidths # Assuming symmetrical response
    # Rectangular area model is more conservative
    _antenna_gains = 41253/(numpy.multiply(beamwidth_theta, beamwidth_phi))

    return 10 * numpy.log10(_antenna_gains*antenna_efficiency)



def parameterizer(key, values):

    link_margins = []

    # TODO Arbitrary parameter value handling
    for value in values:

        satellite_slant_range = slant_range(value, elevation_angle, EARTH_RADIUS)

        minimum_ebn0 = ebn0(mission_bit_error_rate, modulation_type)
        spacecraft_eirp = eirp(spacecraft_transmit_power,
                               spacecraft_transmit_losses,
                               spacecraft_transmit_antenna_gains[:, 0])

        c_over_n0 = \
            spacecraft_eirp + \
            ground_station_g_over_t + \
            path_loss_free_space(satellite_slant_range, center_frequency) + \
            path_loss_troposphere() + \
            path_loss_troposphere() + \
            BOLTZMANN

        actual_ebn0 = c_over_n0 - 10 * math.log10(modulated_bit_rate)
        link_margins.append(actual_ebn0 - implementation_margin - minimum_ebn0 + coding_gain)

    plt.plot(numpy.array(altitudes, dtype='float') / 1E3, link_margins)
    plt.plot(numpy.array(altitudes, dtype='float') / 1E3, sdr_specs, color='green')
    plt.plot(numpy.array(altitudes, dtype='float') / 1E3, cdr_specs, color='orange')
    plt.plot(numpy.array(altitudes, dtype='float') / 1E3, min_specs, color='red')
    plt.title(link_name)
    plt.xlabel(key)
    plt.ylabel('Link Margin (dB)')
    plt.show()

    return


EARTH_RADIUS = 6378*1000
BOLTZMANN = -10*math.log10(scipy.constants.value(u'Boltzmann constant'))

# ARC-STD-8070.1 : https://www.nasa.gov/sites/default/files/atoms/files/std8070.1.pdf
sdr_spec = 6  # dB
cdr_spec = 3  # dB
min_spec = 0  # 100% likely bit drops here (dB)

frequency_name = 'X-band Downlink'
mission_name = 'AnyMission™'
link_name = frequency_name + ': ' + mission_name
modulated_bit_rate = 100E6
modulation_type = 'QPSK'
altitude = 600E3
elevation_angle = 10
center_frequency = 8025E6
implementation_margin = 1
mission_bit_error_rate = 1E-12
coding_gain = 14  # rate 1/2
ground_station_g_over_t = 20
spacecraft_transmit_power = 10  # dBW
spacecraft_transmit_losses = 2
# [gains, 3 dB coverage angle +/- = half power beamwidth]
spacecraft_transmit_antenna_pattern = numpy.array([10])
spacecraft_transmit_antenna_pattern = numpy.append(spacecraft_transmit_antenna_pattern, numpy.array(list(zip(antenna_gain(numpy.linspace(11, 90, num=2)),numpy.linspace(11, 90, num=2)))))
spacecraft_transmit_antenna_beamwidths = 0
spacecraft_transmit_antenna_gains = 0
altitudes = numpy.linspace(300E3, 1200E3, num=50)

swept_parameter_xlabel = 'Altitude (km)'
swept_parameter_xlabel = 'Beamwidth (+/- Degrees'

# parameterizer(swept_parameter_xlabel, swept_parameter)


# TODO move this to a function
if swept_parameter_xlabel == 'Altitude (km)':
    spacecraft_transmit_antenna_gains = 10 #TODO fix this hack
    sdr_specs = [sdr_spec] * len(altitudes)
    cdr_specs = [cdr_spec] * len(altitudes)
    min_specs = [min_spec] * len(altitudes)
elif swept_parameter_xlabel == 'Beamwidth (+/- Degrees':
    altitudes = 500E3
    spacecraft_transmit_antenna_gains = spacecraft_transmit_antenna_pattern[:, 0]  # Shape = 2 gains vs 50 for altitudes
    spacecraft_transmit_antenna_beamwidths = spacecraft_transmit_antenna_pattern[:, 1]
    sdr_specs = [sdr_spec] * len(spacecraft_transmit_antenna_gains)
    cdr_specs = [cdr_spec] * len(spacecraft_transmit_antenna_gains)
    min_specs = [min_spec] * len(spacecraft_transmit_antenna_gains)

satellite_slant_range = slant_range(altitudes, elevation_angle, EARTH_RADIUS)
minimum_ebn0 = ebn0(mission_bit_error_rate, modulation_type)
spacecraft_eirp = eirp(spacecraft_transmit_power,
                       spacecraft_transmit_losses,
                       spacecraft_transmit_antenna_gains)

c_over_n0 = \
    spacecraft_eirp + \
    ground_station_g_over_t + \
    path_loss_free_space(satellite_slant_range, center_frequency) + \
    path_loss_troposphere(satellite_slant_range, center_frequency) + \
    path_loss_ionosphere(satellite_slant_range, center_frequency) + \
    BOLTZMANN

actual_ebn0 = c_over_n0 - 10 * math.log10(modulated_bit_rate)
link_margins = actual_ebn0 - implementation_margin - minimum_ebn0 + coding_gain

# TODO move this to a function
if swept_parameter_xlabel == 'Altitude (km)':
    plt.plot(numpy.array(altitudes, dtype='float') / 1E3, link_margins)
    plt.plot(numpy.array(altitudes, dtype='float') / 1E3, sdr_specs, color='green')
    plt.plot(numpy.array(altitudes, dtype='float') / 1E3, cdr_specs, color='orange')
    plt.plot(numpy.array(altitudes, dtype='float') / 1E3, min_specs, color='red')
    plt.title(link_name)
    plt.xlabel(swept_parameter_xlabel)
    plt.ylabel('Link Margin (dB)')
    plt.show()

elif swept_parameter_xlabel == 'Beamwidth (+/- Degrees':
    plt.plot(numpy.array(spacecraft_transmit_antenna_beamwidths, dtype='float'), link_margins)
    plt.plot(numpy.array(spacecraft_transmit_antenna_beamwidths, dtype='float'), sdr_specs, color='green')
    plt.plot(numpy.array(spacecraft_transmit_antenna_beamwidths, dtype='float'), cdr_specs, color='orange')
    plt.plot(numpy.array(spacecraft_transmit_antenna_beamwidths, dtype='float'), min_specs, color='red')
    plt.title(link_name)
    plt.xlabel('Beamwidth')
    plt.ylabel('Link Margin (dB)')
    plt.show()

