import numpy as np
import pandas as pd

def OrdMatCalc(mode, mat, sumarray, sumPcu, sumPFe, sumPstr, sumPf, sumPw, sumPinv, ptx, pty):

    ord_array = np.zeros(20)
    
    if mode == 1:
        # Find top 10 and bottom 10 values
        uq = np.unique(sumarray[sumarray != 0])
        ord_array[:10] = np.flip(uq[-10:])  # Top 10
        ord_array[10:] = uq[:10]            # Bottom 10
    else:
        # Find the selected point values
        for idx in range(20):
            ord_array[idx] = mat[ptx[idx]][pty[idx]]
    
    # Get indices of ord_array in sumarray
    # idx = np.nonzero(np.isin(ord_array,sumarray))[0]
    idx = [np.where(sumarray == x)[0][0] for x in ord_array if x in sumarray]

   
    Pcuord = np.abs(sumPcu[idx])
    Pfeord = np.abs(sumPFe[idx])
    Pstrord = np.abs(sumPstr[idx])
    Pford = np.abs(sumPf[idx])
    Pword = np.abs(sumPw[idx])
    Pinvord = np.abs(sumPinv[idx])
   
    y1 = np.vstack((Pcuord, Pfeord, Pstrord, Pford, Pword, Pinvord)).T
   
    return ord_array, y1