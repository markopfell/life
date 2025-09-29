**Error Vector Magntiude**
```math
SNR = PAPR - EVM_\text{ white noise} + 3
```

$SNR$ is the signal to noise ratio given in (dB)

$EVM$ is the error vector magnitude.  The error vector being the error in both the amplitude and phase in a recieved symbol compared to the ideal symbol.

$PAPR$ is the peak average power ratio.  The 3 (dB) is for a single unmodulated tone (sine wave).  Binary phase shift keying (BPSK) theoretically has a PAPR of 0 dB similar to a square wave, and QPSK has around 1.7 dB.  Multi carrier scenarios like orthogonal frequency domain access (OFDMA) have an order of magnitude PAPR around 12 dB since the average energy and symbol varies so widly.


**Noise Temperature**
```math
T_{\text { Noise}}(K) = T_\text{REF}(K)\left[10^\frac{\text{NF (dB)}}{10}-1\right]
```
$T_\text{REF}$ is the reference temperature of the system.  Typically taken at the Earth's noise temperature of 290 K. 

NF is the noise figure of the system.  The first term in the series expanion of a cascaded noise figure is the noise figure of the first element.  Typically a low noise amplifier (LNA).  Additional element noise contributions are reduced by the cascaded gain.

**Effective Isotropic Radiated Power**
```math
EIRP = P_T + G_T + L_\text{ output}
```
$P_T$ is the output power of typically the final power amplfier in the cascade. 

$L_\text{ output}$ is the loss post power amplifier, which could include cableing, duplexer, antenna ohmic, and other loss contribution elements in the chain.



**Free Space Path Loss**
```math
L_{\text { free space}} = 20\log_{10}\left(\frac{\frac{f}{c}}{4\pi R}\right) 
```

$f$ is the frequency of the signal in Hz

$c$ is the speed of light 

$d$ is the distance between the two receiving antennas.  In the context of rockets and low earth orbit satellites d refers to the geometric slant range.

**Friis Link Equation**
```math

\frac{C}{N_0} = EIRP + 
                \frac{G_R}{T_\text{Noise}} + 
                L_{\text { free space}} +
                L_{\text { troposphere}} -
                10\log_{10}(k)
```
$C$ is the carrier

$N_0$ is the noise density

L is the tropospheric loss (atmospheric gasses N2, O2, CO2, .. etc.) 

$k$ is Boltzmann's constant
<br>
<br>
**Energy per bit noise density (Desired)**
```math
\frac{E_b}{N_0}_{\text {Desired}}(\text{modulation}, \text{BER}) 
```
BER is the bit error rate
<br>
<br>
**Energy per bit noise density (Actual)**
```math
\frac{E_b}{N_0}_{\text {Actual}} = \frac{C}{N_0} - 10\log_{10}(\text{modulated bit rate})
```
**Link Margin**
```math
\text{Link margin} = \frac{E_b}{N_0}_{\text {Actual}} -  
                     \frac{E_b}{N_0}_{\text {Desired}} +
                     G_\text{ coding} +
                     L_\text{ implementation} +
                     L_\text{ link} +
                     L_\text{ fade}
```
$G_\text{ coding}$ is the coding gain of the forward error correction

$L_\text{ implementation}$ is the loss of the receiver used to demodulate and decode the waveform

$L_\text{ link}$ are miscellaneous losses like pointing error, depolarization, cross-polarization, radome losses, ... etc. 

$L_\text{ fade}$ could be: rain/cloud, scintillation, or other dynamic link effects like interference.  Most links assume a clear skies 99% probability and do not take into account additional link margin for degradation.  Probabilities in the 3 or higher nines (99.9%, 99.99%, 99.999% ...) typically start with 3 dB of margin and then increase exponentially.
