**Noise Temperature**
```math
T_{\text { Noise}}
```

**Effective Isotropic Radiated Power**
```math
EIRP = P_T + G_T + L_\text{ output}
```
$P_T$ is the power transmitted
$L_\text{ output}$ is the loss



**Free Space Path Loss**
```math
L_{\text { free space}} = 20\log_{10}\left(\frac{\lambda}{4\pi R}\right) 
```

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
\frac{E_b}{N_0}_{\text {Actual}} = \frac{C}{N_0} - 10\log_{10}(\text{modualated bit rate})
```
**Energy per bit noise density (Actual)**
```math
\text{link margin} = \frac{E_b}{N_0}_{\text {Actual}} -  
                     \frac{E_b}{N_0}_{\text {Desired}} +
                     G_\text{ coding} +
                     L_\text{ implementation} +
                     L_\text{ link} +
                     L_\text{ fade}
```
$G_\text{ coding}$ is the coding gain of the forward error correction

$L_\text{ implementation}$ is the loss of the receiver used to demodulate and decode the waveform

$L_\text{ link}$ are miscallenous losses like pointing error, depolarization, cross-polarization, radome losses, ... etc. 

$L_\text{ fade}$ could be: rain/cloud, scintillation, or other dynamic link effects like interference.  Most links assume a clear skies 99% probability and do not take into account additional link margin for degradation.  Probabilities in the 3 or higher nines (99.9%, 99.99%, 99.999% ...) typically start with 3 dB of margin and then increase exponentially.
