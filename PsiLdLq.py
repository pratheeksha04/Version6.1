import pandas as pd
import numpy as np

def PsiLdLq(pole,DTtab,Hdcalf,Hqcalf,type,DTnum,AdjPM,AdjLd,AdjLq,Psid,Psiq,Omega):
    global PLmat
    PLmat={}
    

    # Psid = pd.read_excel("InputTableFile.xlsx", sheet_name="Psi_d", header=None).iloc[2:, 2:].values
    # Psiq = pd.read_excel("InputTableFile.xlsx", sheet_name="Psi_q", header=None).iloc[2:, 2:].values
    # k1Omega1 = Psid**2 + Psiq**2

    Idarr = np.arange(-650, 1, 25)
    Iqarr = np.arange(650, -1, -25)
    ndrr = len(Idarr)
    nqrr = len(Iqarr)


    AdjPM = AdjPM / 100
    AdjLd = AdjLd / 100
    AdjLq = AdjLq / 100

    Hdmat = np.zeros((6, len(Idarr)))
    for ind in range(len(Idarr)):
        for idx in range(6):
            Hdmat[idx][ind] = DTtab[idx][4] + 0.000001 * DTtab[idx][2] * Idarr[ind]
        if Hdcalf == 2:
            Hdmat[5][ind] = 5.375 * 10**(-8) * (Idarr[ind])**2 + 2.11 * 10**(-4) * Idarr[ind] + 7.305 * 10**(-2)
    

    Hqmat = np.zeros((6, len(Iqarr)))
    for ind in range(len(Iqarr)):
        for idx in range(6):
            Hqmat[idx][ind]  = 0.000001 * DTtab[idx][ 3] * Iqarr[ind] + DTtab[idx][ 5]
        if Hqcalf == 2:
            Hqmat[5][ ind] = 4.903 * 10**(-13) * (Iqarr[ind])**3 + 1.468 * 10**(-6) * (Iqarr[ind])**2 + 6.678 * 10**(-4) * Iqarr[ind]


    solverA = 0.845762136019501;
    solverB = 1.37338000111102;

    
    # Assuming numel(Iqarr) and numel(Idarr) are defined before this code block
    H2onemat = np.zeros((len(Iqarr), len(Idarr)))
    H2twomat = np.zeros((len(Iqarr), len(Idarr)))
    H2threemat = np.zeros((len(Iqarr), len(Idarr)))
    H2fourmat = np.zeros((len(Iqarr), len(Idarr)))
    H2fivemat = np.zeros((len(Iqarr), len(Idarr)))
    H2sixmat = np.zeros((len(Iqarr), len(Idarr)))
    H2sevenmat = np.zeros((len(Iqarr), len(Idarr)))


   
    for ind in range(len(Idarr)):
        for idx in range(len(Iqarr)):
            H2onemat[idx][ind]  = (Hdmat[0][ ind] / DTtab[0][ 0])**2 + (Hqmat[0][idx] / DTtab[0][1])**2
            H2twomat[idx][ind]  = (Hdmat[1][ind] / DTtab[1][0])**2 + (Hqmat[1][idx] / DTtab[1][1])**2
            H2threemat[idx][ind]  = (Hdmat[2][ind] / DTtab[2][0])**2 + (Hqmat[2][idx] / DTtab[2][ 1])**2
            H2fourmat[idx][ind]  = (Hdmat[3][ind] / DTtab[3][0])**2 + (Hqmat[3][idx] / DTtab[3][1])**2
            H2fivemat[idx][ind]  = (Hdmat[4][ind] / DTtab[4][0])**2 + (Hqmat[4][idx] / DTtab[4][1])**2
            H2sixmat[idx][ind] = Omega[idx][ind] * (pole / 2 * 3 / 2) **2
            H2sevenmat[idx][ind]  = (pole / 2 * 3 / 2) ** 2 * ((Hdmat[5][ind] / solverA)**2 + (np.transpose(Hqmat[5][idx]) / solverB)**2)

    oneK0 = np.sqrt(H2onemat)
    twoK0 = np.sqrt(H2twomat)
    threeK0 = np.sqrt(H2threemat)
    fourK0 = np.sqrt(H2fourmat)
    fiveK0 = np.sqrt(H2fivemat)
    sixK0 = np.sqrt(H2sixmat)
    sevenK0 = np.sqrt(H2sevenmat)
    #print("sixK0", sixK0)

    # aval = pd.read_excel("InputTableFile.xlsx", sheet_name="a(k)", header=None).iloc[:, 2:].values
    aval = pd.read_excel("InputTableFile.xlsx", sheet_name="a(k)", header=None).iloc[1:, 0:].values


    oneKmat = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    Kk0one = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    twoKmat = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    Kk0two = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    threeKmat = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    Kk0three = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    fourKmat = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    Kk0four = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
   
    fiveKmat = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    Kk0five = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    sixKmat = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    Kk0six = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    sevenKmat = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    Kk0seven = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    eightKmat = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    Kk0eight = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]



   
    for idx in range(len(Iqarr)):
        for ind in range(len(Idarr)):
            # C3:AC29
            oneKmat[idx][ind] = DTtab[0][6] * oneK0[idx][ind] / np.sqrt(1 + (DTtab[0][6] * oneK0[idx][ind])**2)
            Kk0one[idx][ind] = oneKmat[idx][ind] / oneK0[idx][ind]
   
            twoKmat[idx][ind] = np.tanh(DTtab[1][ 6] * twoK0[idx][ind])
            Kk0two[idx][ind] = twoKmat[idx][ind] / twoK0[idx][ind]
   
            threeKmat[idx][ind] = DTtab[2][ 6] * threeK0[idx][ind] / np.sqrt(1 + (DTtab[2][6] * threeK0[idx][ind])**2)
            Kk0three[idx][ind] = threeKmat[idx][ind] / threeK0[idx][ind]
   
            fourKmat[idx][ind] = np.arctan(DTtab[3][6] * fourK0[idx][ind])
            Kk0four[idx][ind] = fourKmat[idx][ind] / fourK0[idx][ind]
   
            fiveKmat[idx][ind] = 1 - np.exp(-DTtab[4][6] * fiveK0[idx][ind])
            Kk0five[idx][ind] = fiveKmat[idx][ind] / fiveK0[idx][ind]
   
            sixKmat[idx][ind] = (1.32962896540908) * sixK0[idx][ind] / np.sqrt(1 + ((1.32962896540908) * sixK0[idx][ind])**2)
            Kk0six[idx][ind] = sixKmat[idx][ind] / sixK0[idx][ind]
   
            sevenKmat[idx][ind] = DTtab[5][6] * sevenK0[idx][ind] / np.sqrt(1 + (DTtab[5][6] * sevenK0[idx][ind])**2)
            Kk0seven[idx][ind] = sevenKmat[idx][ind] / sevenK0[idx][ind]
   
            eightKmat[idx][ind] = np.arctan(aval[idx][0] * sevenK0[idx][ind]) #.astype(float)
            Kk0eight[idx][ind] = eightKmat[idx][ind] / sevenK0[idx][ind]


    Tlin1 = np.zeros((len(Iqarr), len(Idarr)))
    Tlin2 = np.zeros((len(Iqarr), len(Idarr)))
    Tlin3 = np.zeros((len(Iqarr), len(Idarr)))
    Tlin4 = np.zeros((len(Iqarr), len(Idarr)))
    Tlin5 = np.zeros((len(Iqarr), len(Idarr)))
    Tlin7 = np.zeros((len(Iqarr), len(Idarr)))
    TKk0cal6 = np.zeros((len(Iqarr), len(Idarr)))

    # Kk0eight = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
   
    for ind in range(len(Idarr)):
        for idx in range(len(Iqarr)):
            Tlin1[idx][ind] = 3/2 * (pole/2) * (Hdmat[0][ind]*Iqarr[idx] - Hqmat[0][idx]*Idarr[ind])
            Tlin2[idx][ind] = 3/2 * (pole/2) * (Hdmat[1][ind]*Iqarr[idx] - Hqmat[1][idx]*Idarr[ind])
            Tlin3[idx][ind] = 3/2 * (pole/2) * (Hdmat[2][ind]*Iqarr[idx] - Hqmat[2][idx]*Idarr[ind])
            Tlin4[idx][ind] = 3/2 * (pole/2) * (Hdmat[3][ind]*Iqarr[idx] - Hqmat[3][idx]*Idarr[ind])
            Tlin5[idx][ind] = 3/2 * (pole/2) * (Hdmat[4][ind]*Iqarr[idx] - Hqmat[4][idx]*Idarr[ind])
            Tlin7[idx][ind] = 3/2 * (pole/2) * (Hdmat[5][ind]*Iqarr[idx] - Hqmat[5][idx]*Idarr[ind])
            TKk0cal6[idx][ind] = 3/2 * (pole/2) * (Iqarr[idx]*Psid[idx][ind] - Idarr[ind]*Psiq[idx][ind])
    #Tlin6 = TKk0cal6 / Kk0six

    t_ave_df = pd.read_excel("InputTableFile.xlsx",  sheet_name="T_ave_matrix", header=None)
    t_ave = t_ave_df.iloc[2:, 2:].values
       
    TKk0cal1 = Tlin1 * Kk0one
    TKk0cal2 = Tlin2 * Kk0two
    TKk0cal3 = Tlin3 * Kk0three
    TKk0cal4 = Tlin4 * Kk0four
    TKk0cal5 = Tlin5 * Kk0five
    TKk0cal7 = Tlin7 * Kk0seven
    TKk0cal8 = Tlin7 * Kk0eight
   
       
    DTKk0 = np.zeros((8, *t_ave.shape))

    # print(DTKk0)
   
    DTKk0[0, :, :] = TKk0cal1 - t_ave
    DTKk0[1, :, :] = TKk0cal2 - t_ave
    DTKk0[2, :, :] = TKk0cal3 - t_ave
    DTKk0[3, :, :] = TKk0cal4 - t_ave
    DTKk0[4, :, :] = TKk0cal5 - t_ave
    DTKk0[5, :, :] = TKk0cal6 - t_ave
    DTKk0[6, :, :] = TKk0cal7 - t_ave
    DTKk0[7, :, :] = TKk0cal8 - t_ave

 

    xPsimOne = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xPsimTwo = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xPsimThree = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xPsimFour = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xPsimFive = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xPsimSix = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xPsimSeven = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]

    xLd1 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xLd2 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xLd3 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xLd4 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xLd5 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xLd6 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xLd7 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]

    xLq1 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xLq2 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xLq3 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xLq4 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xLq5 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xLq6 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]
    xLq7 = [[0 for _ in range(len(Idarr))] for _ in range(len(Iqarr))]

   
    for ind in range(len(Idarr)):
        for idx in range(len(Iqarr)):
            xPsimOne[ind][idx] = Kk0one[ind][idx] * DTtab[0][4]
            xPsimTwo[ind][idx] = Kk0two[ind][idx] * DTtab[1][4]
            xPsimThree[ind][idx] = Kk0three[ind][idx] * DTtab[2][4]
            xPsimFour[ind][idx] = Kk0four[ind][idx] * DTtab[3][4]
            xPsimFive[ind][idx] = Kk0five[ind][idx] * DTtab[4][4]
            xPsimSix[ind][idx] = Kk0six[ind][idx] * DTtab[4][4]
            xPsimSeven[ind][idx] = Kk0seven[ind][idx] * DTtab[4][4]
   
            xLd1[ind][idx] = Kk0one[ind][idx] * DTtab[0][2] * 0.000001
            xLd2[ind][idx] = Kk0two[ind][idx] * DTtab[1][2] * 0.000001
            xLd3[ind][idx] = Kk0three[ind][idx] * DTtab[2][ 2] * 0.000001
            xLd4[ind][idx] = Kk0four[ind][idx] * DTtab[3][2] * 0.000001
            xLd5[ind][idx] = Kk0five[ind][idx] * DTtab[0][2] * 0.000001
            xLd6[ind][idx] = Kk0six[ind][idx] * DTtab[5][2] * 0.000001
            xLd7[ind][idx] = Kk0seven[ind][idx] * DTtab[5][2] * 0.000001
           
            xLq1[ind][idx] = Kk0one[ind][idx] * DTtab[0][3] * 0.000001
            xLq2[ind][idx] = Kk0two[ind][idx] * DTtab[1][3] * 0.000001
            xLq3[ind][idx] = Kk0three[ind][idx] * DTtab[2][3] * 0.000001
            xLq4[ind][idx] = Kk0four[ind][idx] * DTtab[3][3] * 0.000001
            xLq5[ind][idx] = Kk0five[ind][idx] * DTtab[4][3] * 0.000001
            xLq6[ind][idx] = Kk0six[ind][idx]* DTtab[5][3] * 0.000001
            xLq7[ind][idx] = Kk0seven[ind][idx] * DTtab[5][3] * 0.000001

# Assuming xPsimOne, xPsimTwo, ..., xPsimSeven are NumPy arrays
# Assuming xLd1, xLd2, ..., xLd7 are NumPy arrays
# Assuming xLq1, xLq2, ..., xLq7 are NumPy arrays
# Assuming mode is an integer variable

    xPsimOnearr = np.array(xPsimOne)
    xLd1arr = np.array(xLd1)
    xLq1arr = np.array(xLq1)
   
    xPsiMode = np.zeros((7, xPsimOnearr.shape[1]))
    xLdMode = np.zeros((7, xLd1arr.shape[1]))
    xLqMode = np.zeros((7, xLq1arr.shape[1]))
   
    if type == 1:
        xPsiMode[0, :] = np.mean(xPsimOne, axis=1)
        xPsiMode[1, :] = np.mean(xPsimTwo, axis=1)
        xPsiMode[2, :] = np.mean(xPsimThree, axis=1)
        xPsiMode[3, :] = np.mean(xPsimFour, axis=1)
        xPsiMode[4, :] = np.mean(xPsimFive, axis=1)
        xPsiMode[5, :] = np.mean(xPsimSix, axis=1)
        xPsiMode[6, :] = np.mean(xPsimSeven, axis=1)
       
        xLdMode[0, :] = np.mean(xLd1, axis=1)
        xLdMode[1, :] = np.mean(xLd2, axis=1)
        xLdMode[2, :] = np.mean(xLd3, axis=1)
        xLdMode[3, :] = np.mean(xLd4, axis=1)
        xLdMode[4, :] = np.mean(xLd5, axis=1)
        xLdMode[5, :] = np.mean(xLd6, axis=1)
        xLdMode[6, :] = np.mean(xLd7, axis=1)
       
        xLqMode[0, :] = np.mean(xLq1, axis=1)
        xLqMode[1, :] = np.mean(xLq2, axis=1)
        xLqMode[2, :] = np.mean(xLq3, axis=1)
        xLqMode[3, :] = np.mean(xLq4, axis=1)
        xLqMode[4, :] = np.mean(xLq5, axis=1)
        xLqMode[5, :] = np.mean(xLq6, axis=1)
        xLqMode[6, :] = np.mean(xLq7, axis=1)
   
    elif type == 2:
        xPsiMode[0, :] = np.max(xPsimOne, axis=1)
        xPsiMode[1, :] = np.nanmax(xPsimTwo, axis=1)
        xPsiMode[2, :] = np.max(xPsimThree, axis=1)
        xPsiMode[3, :] = np.max(xPsimFour, axis=1)
        xPsiMode[4, :] = np.max(xPsimFive, axis=1)
        xPsiMode[5, :] = np.max(xPsimSix, axis=1)
        xPsiMode[6, :] = np.max(xPsimSeven, axis=1)
       
        xLdMode[0, :] = np.max(xLd1, axis=1)
        xLdMode[1, :] = np.nanmax(xLd2, axis=1)
        xLdMode[2, :] = np.max(xLd3, axis=1)
        xLdMode[3, :] = np.max(xLd4, axis=1)
        xLdMode[4, :] = np.max(xLd5, axis=1)
        xLdMode[5, :] = np.max(xLd6, axis=1)
        xLdMode[6, :] = np.max(xLd7, axis=1)
       
        xLqMode[0, :] = np.max(xLq1, axis=1)
        xLqMode[1, :] = np.nanmax(xLq2, axis=1)
        xLqMode[2, :] = np.max(xLq3, axis=1)
        xLqMode[3, :] = np.max(xLq4, axis=1)
        xLqMode[4, :] = np.max(xLq5, axis=1)
        xLqMode[5, :] = np.max(xLq6, axis=1)
        xLqMode[6, :] = np.max(xLq7, axis=1)
   
    else:
        xPsiMode[0, :] = xPsimOne[:, -1]
        xPsiMode[1, :] = xPsimTwo[:, -1]
        xPsiMode[2, :] = xPsimThree[:, -1]
        xPsiMode[3, :] = xPsimFour[:, -1]
        xPsiMode[4, :] = xPsimFive[:, -1]
        xPsiMode[5, :] = xPsimSix[:, -1]
        xPsiMode[6, :] = xPsimSeven[:, -1]
   
        xLdMode[0, :] = xLd1[:, -1]
        xLdMode[1, :] = xLd2[:, -1]
        xLdMode[2, :] = xLd3[:, -1]
        xLdMode[3, :] = xLd4[:, -1]
        xLdMode[4, :] = xLd5[:, -1]
        xLdMode[5, :] = xLd6[:, -1]
        xLdMode[6, :] = xLd7[:, -1]
   
        xLqMode[0, :] = xLq1[:, -1]
        xLqMode[1, :] = xLq2[:, -1]
        xLqMode[2, :] = xLq3[:, -1]
        xLqMode[3, :] = xLq4[:, -1]
        xLqMode[4, :] = xLq5[:, -1]
        xLqMode[5, :] = xLq6[:, -1]
        xLqMode[6, :] = xLq7[:, -1]

    #print(xLqMode)

    # Psi_PM sheet
    PsiPm = np.zeros((6, xPsiMode.shape[1] + 1))  # Initialize PsiPm array
   
    # Calculate Psi arrays for all 6 rows of the digital twin table
    PsiPm[0, :] = np.concatenate([[xPsiMode[0][0]**2 / xPsiMode[0][1]], xPsiMode[0, :]])  # Col H
    PsiPm[1, :] = np.concatenate([[xPsiMode[1][0]**2 / xPsiMode[1][1]], xPsiMode[1, :]])  # Col I
    PsiPm[2, :] = np.concatenate([[xPsiMode[2][0]**2 / xPsiMode[2][1]], xPsiMode[2, :]])  # Col J
    PsiPm[3, :] = np.concatenate([[xPsiMode[3][0]**2 / xPsiMode[3][1]], xPsiMode[3, :]])  # Col K
    PsiPm[4, :] = np.concatenate([[xPsiMode[4][0]**2 / xPsiMode[4][1]], xPsiMode[4, :]])  # Col L
    PsiPm[5, :] = np.concatenate([[xPsiMode[6][0]**2 / xPsiMode[6][1]], xPsiMode[6, :]])  # Col M

    # The selected row is adjusted and returned
    # print("PsiPm[DTnum, :]",PsiPm[DTnum, :])
    PLmat['PsiArr'] = PsiPm[DTnum, :] * (1 + AdjPM)  # Col C
   
    # LUT(Ld,Lq) sheet
    LUTLd = np.zeros((6, xLdMode.shape[1] + 1))  # Initialize LUTLd array
    LUTLq = np.zeros((6, xLqMode.shape[1] + 1))  # Initialize LUTLq array
   
    # Calculate Ld arrays for all 6 rows of the digital twin table
    LUTLd[0, :] = np.concatenate([[xLdMode[0][0]**2 / xLdMode[0][1]], xLdMode[0, :]])  # Col D
    LUTLd[1, :] = np.concatenate([[xLdMode[1][0]**2 / xLdMode[1][1]], xLdMode[1, :]])  # Col E
    LUTLd[2, :] = np.concatenate([[xLdMode[2][0]**2 / xLdMode[2][1]], xLdMode[2, :]])  # Col F
    LUTLd[3, :] = np.concatenate([[xLdMode[3][0]**2 / xLdMode[3][1]], xLdMode[3, :]])  # Col G
    LUTLd[4, :] = np.concatenate([[xLdMode[4][0]**2 / xLdMode[4][1]], xLdMode[4, :]])  # Col H
    LUTLd[5, :] = np.concatenate([[xLdMode[6][0]**2 / xLdMode[6][1]], xLdMode[6, :]])  # Col I
   
    # Calculate Lq arrays for all 6 rows of the digital twin table
    LUTLq[0, :] = np.concatenate([[xLqMode[0][0]**2 / xLqMode[0, 1]], xLqMode[0, :]])  # Col O
    LUTLq[1, :] = np.concatenate([[xLqMode[1][0]**2 / xLqMode[1, 1]], xLqMode[1, :]])  # Col P
    LUTLq[2, :] = np.concatenate([[xLqMode[2][0]**2 / xLqMode[2, 1]], xLqMode[2, :]])  # Col Q
    LUTLq[3, :] = np.concatenate([[xLqMode[3][0]**2 / xLqMode[3, 1]], xLqMode[3, :]])  # Col R
    LUTLq[4, :] = np.concatenate([[xLqMode[4][0]**2 / xLqMode[4, 1]], xLqMode[4, :]])  # Col S
    LUTLq[5, :] = np.concatenate([[xLqMode[6][0]**2 / xLqMode[6, 1]], xLqMode[6, :]])  # Col T

   
    # Adjust LdArr and LqArr and return
    PLmat['LdArr'] = LUTLd[DTnum, :] * (1 + AdjLd)  # Col J
    PLmat['LqArr'] = LUTLq[DTnum, :] * (1 + AdjLq)  # Col U
    
    PLmat['DTKk0'] = np.zeros((8, *t_ave.shape))
    PLmat['Hdmat'] = np.zeros((6, len(Idarr)))
    PLmat['Hqmat'] = np.zeros((6, len(Iqarr)))
    PLmat['Ld'] = np.zeros((6, xLdMode.shape[1] + 1))
    PLmat['Lq'] = np.zeros((6, xLqMode.shape[1] + 1))
    PLmat['Psi'] = np.zeros((6, xPsiMode.shape[1] + 1))
    PLmat['k0mat'] =  np.zeros((6, 27, 27))
    
    PLmat['DTKk0'] = DTKk0
    PLmat['Hdmat'] = Hdmat
    PLmat['Hqmat'] = Hqmat
    PLmat['Ld'] = LUTLd
    PLmat['Lq'] = LUTLq
    PLmat['Psi'] = PsiPm

    PLmat['k0mat'][0, :, :] = oneK0
    PLmat['k0mat'][1, :, :] = twoK0
    PLmat['k0mat'][2, :, :] = threeK0
    PLmat['k0mat'][3, :, :] = fourK0
    PLmat['k0mat'][4, :, :] = fiveK0
    PLmat['k0mat'][5, :, :] = sevenK0

    return PLmat