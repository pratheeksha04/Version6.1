import numpy as np
import openpyxl

def stdnm_omega(Vm, pole, mode, DTlow, DThigh, Omega1, simtab, DTKk0, k0mat):
    """
    Function to calculate standard deviation by torque and (ω) range by A12 speed

    Input:
      - Vm         : Voltage
      - pole       : Number of poles
      - mode       : 0=Off, 1=On, 2=idiq; For (ω)range; WLTC-Q40 
      - DTlow      : (ω)range low
      - DThigh     : (ω)range high
      - Omega1     : Ψd² + Ψq²
      - simtab     : Simulation id iq matrix
      - DTKk0      : Real Motor Torque Vs Digital twin
      - k0mat      : k_0 = √(Ψ²)

    Output:
      - stdval     : Standard deviation by torque
      - maxval     : Maximum values for (ω) range by A12 speed
      - minval     : Minimum values for (ω) range by A12 speed
    """

    # Obtain original Ψ values from the input excel file and calculate rpm
    Omega2 = Vm / np.sqrt(Omega1) * 60 / (pole * np.pi)  # C34:AC60 - Orig:rpm=ωe*60/P*π

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"


    id = np.arange(-675, 1, 25)  # Horizontal columns
    iq = np.arange(675, -1, -25)  # Vertical rows

    # Process rpm table and k/k_0 table 
    # Col C65:AC91
    rpmtab = np.full((len(id)-1, len(iq)-1), np.nan)  # Initialization
    if mode == 2:
        rpmtab[simtab != 0] = Omega2[simtab != 0]
    elif mode == 0:
        rpmtab = Omega2
    elif mode == 1:
        rpmtab[(Omega2 > DTlow) & (Omega2 < DThigh)] = Omega2[(Omega2 > DTlow) & (Omega2 < DThigh)]

    # Calculate standard deviation by Nm and display the results on DigitalTwin tab UI
    # Col AH:BH - 'D_T(ω)' sheet in excel
    for indx in range(7):
        DTKk0[indx][np.isnan(rpmtab)] = np.nan

    stdval = [
        np.nanstd(DTKk0[0]),
        np.nanstd(DTKk0[1]),
        np.nanstd(DTKk0[2]),
        np.nanstd(DTKk0[3]),
        np.nanstd(DTKk0[4]),
        np.nanstd(DTKk0[6]),
    ]

    # Calculate Digital Twin(ω) range by A12 speed
    # Col BP:CQ - 'H2＆K0(ω)' sheet in excel
    for indx in range(6):
        k0mat[indx][np.isnan(rpmtab)] = np.nan

    poleno = pole / 2 * 3 / 2
    k0 = Vm / (k0mat / poleno) * 60 / (pole * np.pi)
    mat = np.transpose(k0, (1, 2, 0))
    maxval = np.nanmax(mat, axis=(0, 1))
    minval = np.nanmin(mat, axis=(0, 1))

    return stdval, maxval, minval
