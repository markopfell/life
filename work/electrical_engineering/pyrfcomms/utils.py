import scipy
import numpy
from scipy import constants
from scipy import special
import matplotlib.pyplot as plt
import pandas
import os

EARTH_RADIUS = 6378 * 1000
BOLTZMANN = -10 * numpy.log10(scipy.constants.value(u'Boltzmann constant'))


def current_working_directory():
    return os.path.dirname(os.path.abspath(__file__))


def dvb_s2_modcod_searcher(df, _modcod):
    for i, j in df.iterrows():
        if df.iloc[i, 0] == _modcod['modulation'] and df.iloc[i, 1] == _modcod['error correction rate']:
            spectral_efficiency = df.iloc[i, 2]
            esn0 = df.iloc[i, 3]
            _modcod.update({'spectral efficiency': spectral_efficiency, 'esn0': esn0})
    return _modcod


def esn0_to_ebn0(esn0, spectral_efficiency):
    return esn0-10*numpy.log10(spectral_efficiency)


def coding_gain(_modcod):
    _coding_gain = 0
    if _modcod['standard'] == 'ccsds':
        if _modcod['error correction rate'] == 3/4:
            _coding_gain = 14

    elif _modcod['standard'] == 'dvbs2':
        # Final draft ETSI EN 302 307 V1.2.1 (2009-04)
        pass
    _modcod.update({'coding gain': _coding_gain})
    return _modcod


def eirp(power_transmit, loss, gain_transmit):  # dBW, dB, dBi
    return power_transmit - loss + gain_transmit


def g_over_t(gain_receive, noise_temperature):  # dB, dBK
    return gain_receive - 10*numpy.log10(noise_temperature)


def ebn0(bit_error_rate, modulation):
    # http://140.113.144.123/105%20introduction%20to%20digital%20communications/Unit%201-7%20GMSK.pdf
    # https://www.edn.com/design/communications-design/4017668/3/Modulation-roundup-error-rates-noise-and-capacity
    # PCM/PM/NRZ/SP-L ~= BPSK
    # https://deepspace.jpl.nasa.gov/files/phase1.pdf

    _ebn0 = 0

    if modulation == 'GMSK':
        _ebn0 = 10 * numpy.log10(((scipy.special.erfcinv(bit_error_rate * 2)) ** 2) / 0.9)
    elif modulation == 'BPSK' or modulation == 'QPSK' or modulation == 'OQPSK' or modulation == 'PCM':
        _ebn0 = 10 * numpy.log10((scipy.special.erfcinv(bit_error_rate * 2)) ** 2)
    elif modulation == '8PSK' or modulation == '8APSK':
        _ebn0 = 10 * numpy.log10(((scipy.special.erfcinv(bit_error_rate * numpy.log2(8))) ** 2) /
                                (numpy.log2(8) * numpy.sin(numpy.pi / 8)))
    elif modulation == '16QAM' or modulation == '16APSK':
        _ebn0 = 10 * numpy.log10(((scipy.special.erfcinv(bit_error_rate * (8 / 3))) ** 2) * (10 / 4))
        # TODO:  16 APSK = Guess
    elif modulation == '16APSK' or modulation == '16PSK':
        _ebn0 = 10 * numpy.log10(((scipy.special.erfcinv(bit_error_rate * numpy.log2(16))) ** 2) /
                                (numpy.log2(16) * numpy.sin(numpy.pi / 16)))
        # TODO:  32APSK = Guess
    elif modulation == '32APSK':
        _ebn0 = 10 * numpy.log10(((scipy.special.erfcinv(bit_error_rate * numpy.log2(32))) ** 2) /
                                (numpy.log2(32) * numpy.sin(numpy.pi / 32)))
        # TODO:  64APSK = Guess
    elif modulation == '64APSK':
        _ebn0 = 10 * numpy.log10(((scipy.special.erfcinv(bit_error_rate * numpy.log2(64))) ** 2) /
                                (numpy.log2(64) * numpy.sin(numpy.pi / 64)))
        # TODO:  128APSK = Guess
    elif modulation == '128APSK':
        _ebn0 = 10 * numpy.log10(((scipy.special.erfcinv(bit_error_rate * numpy.log2(128))) ** 2) /
                                (numpy.log2(128) * numpy.sin(numpy.pi / 128)))
        # TODO:  256APSK = Guess
    elif modulation == '256APSK':
        _ebn0 = 10 * numpy.log10(((scipy.special.erfcinv(bit_error_rate * numpy.log2(256))) ** 2) /
                                (numpy.log2(256) * numpy.sin(numpy.pi / 256)))

    return _ebn0


# TODO refine estimate
def path_loss_troposphere(distance, frequency):
    return 0


# TODO refine estimate
def path_loss_ionosphere(distance, frequency):
    return 0


def path_loss_free_space(distance, frequency):
    # If shape errors point here, it's likely the C/N sum in general terms -> eirp -> antenna gains
    _path_loss_free_space = 20 * numpy.log10((4 * numpy.pi * distance * frequency) /
                                             scipy.constants.value(u'speed of light in vacuum'))
    return -1*_path_loss_free_space


def slant_range(mean_orbit_altitude, elevation_angle_degrees, object_radius):
    mean_orbit_radius = mean_orbit_altitude + object_radius
    elevation_angle_radians = numpy.radians(elevation_angle_degrees)
    _slant_range = object_radius * ((((mean_orbit_radius ** 2 / object_radius ** 2) -
                                      (numpy.cos(elevation_angle_radians)) ** 2) ** 0.5) -
                                    numpy.sin(elevation_angle_radians))
    return _slant_range


# http://www.tscm.com/antennas.pdf
def antenna_gain(beamwidths):
    antenna_efficiency = 0.6  # Rectangular area model is more conservative
    beamwidth_theta = beamwidths
    beamwidth_phi = beamwidths # Assuming symmetrical response
    # Rectangular area model is more conservative
    _antenna_gains = 41253/(numpy.multiply(beamwidth_theta, beamwidth_phi))

    return 10 * numpy.log10(_antenna_gains*antenna_efficiency)


def output():

    mission_csv = r'any_mission.csv'
    mission_csv_file_path = current_working_directory() + '/' + mission_csv
    mission = pandas.read_csv(mission_csv_file_path, header=None, index_col=0, squeeze=True).to_dict()

    # TODO fix this stupidity
    frequency_name = mission['frequency_name']
    mission_name = mission['mission_name']
    modulated_bit_rate = float(mission['modulated_bit_rate'])
    elevation_angle = float(mission['elevation_angle'])
    center_frequency = float(mission['center_frequency'])
    implementation_margin = float(mission['implementation_margin'])
    mission_bit_error_rate = float(mission['mission_bit_error_rate'])
    ground_station_g_over_t = float(mission['ground_station_g_over_t'])
    spacecraft_transmit_power = float(mission['spacecraft_transmit_power'])
    spacecraft_transmit_antenna_gains = float(mission['spacecraft_transmit_antenna_gains'])
    spacecraft_transmit_losses = float(mission['spacecraft_transmit_losses'])
    sdr_spec = float(mission['sdr_spec'])
    cdr_spec = float(mission['cdr_spec'])
    modcod = {'modulation': '8PSK', 'error correction rate': '3/4', 'standard': 'dvbs2'}
    modcod = coding_gain(modcod)
    dvb_s2_modcods_csv = r'dvb_s2_modcods.csv'
    dvb_s2_modcods_csv_file_path = current_working_directory() + '/' + dvb_s2_modcods_csv
    _dvb_s2_modcods = pandas.read_csv(dvb_s2_modcods_csv_file_path, sep=",", )
    dvb_s2_modcod_searcher(_dvb_s2_modcods, modcod)
    ebn0 = esn0_to_ebn0(modcod['esn0'], modcod['spectral efficiency'])
    modcod.update({'ebn0': ebn0})

    # TODO: Build symmetrical antenna gain vs beamwidth
    # TODO: Lost 2 hr debugging as of 11/5/21
    # spacecraft_transmit_antenna_primary_beamwidths = numpy.array([-10, 0, 10])
    # spacecraft_transmit_antenna_primary_gains = numpy.array([13, 16, 13])
    # TODO fix broken distance append calcs
    # spacecraft_transmit_antenna_secondary_beamwidths = numpy.linspace(10, 180, num=PLOT_POINTS)
    # spacecraft_transmit_antenna_secondary_gains = antenna_gain(spacecraft_transmit_antenna_secondary_beamwidths)
    #
    # spacecraft_transmit_antenna_beamwidths = numpy.append(spacecraft_transmit_antenna_primary_beamwidths,
    #                                                       spacecraft_transmit_antenna_secondary_beamwidths)
    # spacecraft_transmit_antenna_gains = numpy.append(spacecraft_transmit_antenna_primary_gains,
    #                                                  spacecraft_transmit_antenna_secondary_gains)
    # # Assuming that the primary antenna gain is the greatest and most accurate, i.e. measured value,
    # # normalize the secondary modeled antenna gains to it
    # secondary_gain_start = len(spacecraft_transmit_antenna_primary_gains)
    # if spacecraft_transmit_antenna_gains[secondary_gain_start] > spacecraft_transmit_antenna_gains[
    #     secondary_gain_start - 1]:
    #     correction = spacecraft_transmit_antenna_gains[secondary_gain_start] - spacecraft_transmit_antenna_gains[
    #         secondary_gain_start - 1]
    #     spacecraft_transmit_antenna_gains[secondary_gain_start:] = spacecraft_transmit_antenna_gains[
    #                                                                secondary_gain_start:] - correction

    link_name = frequency_name + ': ' + mission_name
    min_spec = 0  # 100% likely bit drops here (dB)
    PLOT_POINTS = 100
    altitudes = numpy.linspace(300E3, 1200E3, num=PLOT_POINTS)

    swept_parameter_ylabel = 'Link Margin (dB)'
    # swept_parameter_ylabel = 'Throughput (Mbps)'
    # swept_parameter_ylabel = 'Combined Antenna Gain (dB)'
    # swept_parameter_xlabel = 'Altitude (km)'
    # swept_parameter_xlabel = 'Beamwidth (Absolute Degrees)'
    swept_parameter_xlabel = 'Elevation Angle (degrees)'

    satellite_slant_range = slant_range(altitudes, elevation_angle, EARTH_RADIUS)


    # parameterizer(swept_parameter_xlabel, swept_parameter)

    # TODO move this to a function
    if swept_parameter_xlabel == 'Altitude (km)':
        spacecraft_transmit_antenna_gains
        sdr_specs = [sdr_spec] * len(altitudes)
        cdr_specs = [cdr_spec] * len(altitudes)
        min_specs = [min_spec] * len(altitudes)
    elif swept_parameter_xlabel == 'Beamwidth (Absolute Degrees)':
        altitudes = 500E3
        sdr_specs = [sdr_spec] * len(spacecraft_transmit_antenna_gains)
        cdr_specs = [cdr_spec] * len(spacecraft_transmit_antenna_gains)
        min_specs = [min_spec] * len(spacecraft_transmit_antenna_gains)
    elif swept_parameter_xlabel == 'Elevation Angle (degrees)':
        # pass
        altitudes = 300E3
        elevation_angles = numpy.geomspace(1, 90, int(PLOT_POINTS/2))
        elevation_angles = numpy.concatenate((elevation_angles, numpy.flip(elevation_angles)))
        sdr_specs = [sdr_spec] * len(elevation_angles)
        cdr_specs = [cdr_spec] * len(elevation_angles)
        min_specs = [min_spec] * len(elevation_angles)
        satellite_slant_range = slant_range(altitudes, elevation_angles, EARTH_RADIUS)


    minimum_ebn0 = 0

    if modcod['standard'] == 'ccsds':
        minimum_ebn0 = ebn0(mission_bit_error_rate, modulation_type)
    elif modcod['standard'] == 'dvbs2':
        minimum_ebn0 = modcod['ebn0']

    spacecraft_eirp = eirp(spacecraft_transmit_power,
                           spacecraft_transmit_losses,
                           spacecraft_transmit_antenna_gains)

    # Careful here accidentally broadcasting matrix operations with WRONG DIMENSIONS = shapes
    # TODO: redo all linspace calls
    # TODO: Make this broadcast error catcher generalize ...
    # if numpy.size(satellite_slant_range) != numpy.size(spacecraft_transmit_antenna_gains):
    #     array_normalizer = numpy.size(spacecraft_transmit_antenna_gains) - numpy.size(satellite_slant_range)
    #
    #     for i in range(0,array_normalizer):
    #         satellite_slant_range = numpy.append(satellite_slant_range,satellite_slant_range[0])

    c_over_n0 = \
        spacecraft_eirp + \
        ground_station_g_over_t + \
        path_loss_free_space(satellite_slant_range, center_frequency) + \
        path_loss_troposphere(satellite_slant_range, center_frequency) + \
        path_loss_ionosphere(satellite_slant_range, center_frequency) + \
        BOLTZMANN

    actual_ebn0 = c_over_n0 - 10 * numpy.log10(modulated_bit_rate)
    link_margins = actual_ebn0 - implementation_margin - minimum_ebn0 + modcod['coding gain']

    # TODO move this to a function
    if swept_parameter_xlabel == 'Altitude (km)' and swept_parameter_ylabel == 'Link Margin (dB)':
        plt.plot(numpy.array(altitudes, dtype='float') / 1E3, link_margins)
        plt.plot(numpy.array(altitudes, dtype='float') / 1E3, sdr_specs, color='green')
        plt.plot(numpy.array(altitudes, dtype='float') / 1E3, cdr_specs, color='orange')
        plt.plot(numpy.array(altitudes, dtype='float') / 1E3, min_specs, color='red')
        plt.title(link_name)
        plt.xlabel(swept_parameter_xlabel)
        plt.ylabel('Link Margin (dB)')
        plt.show()

    elif swept_parameter_xlabel == 'Elevation Angle (degrees)' and swept_parameter_ylabel == 'Link Margin (dB)':
        plt.plot(link_margins)
        plt.plot(elevation_angles, sdr_specs, color='green')
        plt.plot(elevation_angles, cdr_specs, color='orange')
        plt.plot(elevation_angles, min_specs, color='red')
        plt.title(link_name)
        plt.xlabel(swept_parameter_xlabel)
        plt.ylabel('Link Margin (dB)')
        plt.show()


    elif swept_parameter_xlabel == 'Beamwidth (Absolute Degrees)' and swept_parameter_ylabel == 'Link Margin (dB)':
        plt.plot(numpy.array(spacecraft_transmit_antenna_beamwidths, dtype='float'), link_margins)
        plt.plot(numpy.array(spacecraft_transmit_antenna_beamwidths, dtype='float'), sdr_specs, color='green')
        plt.plot(numpy.array(spacecraft_transmit_antenna_beamwidths, dtype='float'), cdr_specs, color='orange')
        plt.plot(numpy.array(spacecraft_transmit_antenna_beamwidths, dtype='float'), min_specs, color='red')
        plt.title(link_name)
        plt.xlabel('Beamwidth (Absolute Degrees)')
        plt.ylabel('Link Margin (dB)')
        plt.show()

    elif swept_parameter_xlabel == 'Beamwidth (Absolute Degrees)' and swept_parameter_ylabel == 'Combined Antenna Gain (dB)':
        plt.plot(numpy.array(spacecraft_transmit_antenna_beamwidths, dtype='float'), spacecraft_transmit_antenna_gains)
        plt.title(link_name)
        plt.xlabel('Beamwidth (Absolute Degrees)')
        plt.ylabel('Combined Antenna Gain (dB)')
        plt.show()
    elif swept_parameter_xlabel == 'Elevation Angle (degrees)' and swept_parameter_ylabel == 'Throughput (Mbps)':
        pass

    return

output()