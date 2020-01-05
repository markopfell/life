import math


def eirp(power_transmit, loss, gain_transmit):  # dBW, dB, dBi
    return power_transmit + loss + gain_transmit


def g_over_t(gain_receive, noise_temperature): # dB, dBK
    return gain_receive - 10*math.log10(noise_temperature)


def ebn0():
    return


def path_loss_troposphere():
    return


def path_loss_ionosphere():
    return


def path_loss_free_space():
    return


def slant_range():
    return



