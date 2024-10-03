import numpy as np

def stdrpm(Id, Iq, Tn, rpm, Irms, a12):

    """
    Function to calculate standard deviation by speed
    Input:
      - Id      : IPM modeled id
      - Iq      : IPM modeled iq
      - Tn      : IPM modeled Tn
      - rpm     : IPM modeled rpm
      - Irms    : IPM modeled Irms 
      - a12     : Object containing all A12 parameters

    Output:
      - stdspd  : Standard deviation by speed
      - simtab  : Simulation id iq matrix
    """

    # Compute - 'Efficiency graph' sheet of Excel
    C = np.ones(4100)  # Col BN
    D = np.ones(727)

    id = np.arange(-675, 1, 25)  # Horizontal columns
    iq = np.arange(675, -1, -25)  # Vertical rows

    # Initialize simulating tables
    simtab = np.zeros((len(id) - 1, len(iq) - 1 )) # frequency table
    simavgtrq = np.full_like(simtab, np.nan)
    simavgspd = np.full_like(simtab, np.nan)
    simirms = np.full_like(simtab, np.nan)

    # Initialize A12 tables
    a12tab = np.zeros_like(simtab)
    a12avgtrq = np.full_like(simtab, np.nan) # frequency table
    a12avgspd = np.full_like(simtab, np.nan)
    a12irms = np.full_like(simtab, np.nan)


    # Calculate frequency and accordingly calculate average_torque, average_speed & Irms
    for ind in range(len(id)-1):
        for idx in range(len(iq)-1):
            # Col BO:CQ
            mask = (Id >= id[ind]) & (Id < id[ind+1]) & (Iq > iq[idx+1]) & (Iq <= iq[idx])
            simtab[idx, ind] = np.sum(C[mask])
            if simtab[idx, ind] != 0:
                simavgtrq[idx, ind] = np.sum(Tn[mask]) / simtab[idx, ind]
                simavgspd[idx, ind] = np.sum(rpm[mask]) / simtab[idx, ind]
                simirms[idx, ind] = np.sum(Irms[mask]) / simtab[idx, ind]

            # Col CT:DV
            mask_a12 = (a12['negId'] >= id[ind]) & (a12['negId'] < id[ind+1]) & (a12['negIq'] > iq[idx+1]) & (a12['negIq'] <= iq[idx])
            a12tab[idx, ind] = np.sum(D[mask_a12])
            if a12tab[idx, ind] != 0:
                a12avgtrq[idx, ind] = np.sum(a12['Te'][mask_a12]) / a12tab[idx, ind]
                a12avgspd[idx, ind] = np.sum(a12['nrpm'][mask_a12]) / a12tab[idx, ind]
                a12irms[idx, ind] = np.sum(a12['I'][mask_a12]) / a12tab[idx, ind]

    # Col DY:FA
    # Initialize computing tables
    avgspd = np.full((len(iq)-1, len(id)-1), np.nan)
    mask_common = np.logical_and(simtab != 0, a12tab != 0)
    avgspd[mask_common] = a12avgspd[mask_common] - simavgspd[mask_common]
    
    # Calculate standard deviation by rpm
    stdspd = np.nanstd(avgspd)

    return stdspd, simtab
