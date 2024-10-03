import numpy as np

def LossTypeCalc(freqmap, avg, losstype, TnorIm, werpm, xax):
    # Create the yax array
    yax = np.arange(0, 21) * 1000
 
    # Initialize mat with zeros (similar to MATLAB's 'mat(1:numel(xax)-1,1:numel(yax)-1) = zeros(...)')
    mat = np.zeros((len(xax) - 1, len(yax) - 1))
 
    # Loop over xax and yax indices
    for ind in range(len(xax) - 1):
        for idx in range(len(yax) - 1):
            # If freqmap at current index is 0, val is 0; otherwise, calculate val based on conditions
            if freqmap[ind, idx] == 0:
                val = 0
            else:
                # Condition to select values in losstype
                condition = (werpm >= yax[idx]) & (werpm < yax[idx + 1]) & \
                            (TnorIm > xax[ind + 1]) & (TnorIm <= xax[ind])
                val = np.sum(losstype[condition])
 
            # Determine the divisor based on avg value
            if avg == 1:
                div = freqmap[ind, idx]
            else:
                div = 1
 
            # Calculate the value to be stored in mat
            mat[ind, idx] = round(val / div, 4)
 
    return mat