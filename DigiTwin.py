import pandas as pd
import numpy as np

def DigiTwin(pole, Vm, DTtab):
    DTtab =  np.array(DTtab)
    # Obtain original Ψ values from the input excel file and calculate rpm
    # Psi_d sheet and Psi_q sheet
    # Psid = pd.read_excel("InputTableFile.xlsx", sheet_name="Psi_d", header=None).iloc[2:, 2:].values
    # Psiq = pd.read_excel("InputTableFile.xlsx", sheet_name="Psi_q", header=None).iloc[2:, 2:].values

    # # The Id and Iq array against which all calculations are done
    # Idarr = np.arange(-650, 1, 25)
    # Iqarr = np.arange(650, -1, -25)

    # ω = Vm / sqrt(Ψd^2 + Ψq^2) sheet
    # Solver results
    #brr = [0.968309, 1.104116, 0.0002893285134, 0.0003828048541, 0.12618807, 0.0]
    brr = [0.968309134210145, 1.10411600242257, 0.000289328513383774, 0.000382804854148081, 0.126188070323104, 0.000000]
    arr = brr
    arr[0] = arr[0] / (3 / 2 * pole / 2)
    arr[1] = arr[1] / (3 / 2 * pole / 2)
    arr[2] = arr[2] * 1000000
    arr[3] = arr[3] * 1000000

    # k1Omega1 = Psid**2 + Psiq**2
    # k1Omega1 = np.array(k1Omega1)
    # k1Omega2 = Vm / np.sqrt(k1Omega1.astype(float)) * 60 / (pole * np.pi)
    

    # # Solver calculations
    # k1Omega3 = np.zeros_like(k1Omega1)
    # for ind, Id in enumerate(Idarr):
    #     for idx, Iq in enumerate(Iqarr):
    #         k1Omega3[idx, ind] = ((brr[2] * Id + brr[4]) / brr[0])**2 + ((brr[3] * Iq + brr[5]) / brr[1])**2

    # k1Omega4 = Vm / np.sqrt(k1Omega3.astype(float)) * 60 / (pole * np.pi)

    # # T-ave(A12) sheet
    # tave1 = pd.read_excel("InputTableFile.xlsx", sheet_name="T_ave_matrix", header=None).iloc[2:, 2:].values
    # maxtave1 = np.max(tave1)

    # tave2 = 3 / 2 * pole / 2 * (Iqarr[:, None] * Psid - Idarr * Psiq)
    # maxtave2 = np.max(tave2)

    # tave3 = tave1 - tave2

    # Excel solver results
    # Ld1, Lq1, psi1 = 0.000212869382567803, 0.000311107068691025, 0.0725264786399191
    # Ld2, Lq2, psi2 = 0.000212744959421379, 0.000311235559094195, 0.0729606243955028
    Ld2 = 0.000212744959421379;
    Lq2 = 0.000311235559094195;
    psi2 = 0.0729606243955028;

    # Update digital twin table
    DTtab[2, 0:6] = arr
    #print(DTtab)
    DTtab[5, 2:5] = [Ld2 * 1000000, Lq2 * 1000000, psi2]
    

    # tave4 = 3 / 2 * pole / 2 * ((psi1 + Ld1 * Idarr)[:, None] * Iqarr - Lq1 * Iqarr * Idarr)
    # tave5 = 3 / 2 * pole / 2 * ((psi2 + Ld2 * Idarr)[:, None] * Iqarr - Lq2 * Iqarr * Idarr)
    
    # tave6 = np.where(np.isnan(tave4), np.nan, (tave2 - tave5)**2)

    # tave7 = (tave1 - tave4)**2

    return DTtab
