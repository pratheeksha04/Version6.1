import numpy as np
import pandas as pd
import math
import cmath
class wltcclass:
     def __init__(self):
        self.sec = None
        self.num = 1801
        self.rpmflag = None
        self.acckm = None
        self.wwrpm = None
        self.Fgravity = None
        self.Frolling = None
        self.FAero = None
        self.Fx = None
        self.werpm = None
        self.Tn = None
        self.condPe = None
        self.AccPe = None
        self.Id = None
        self.Iq = None
        self.Im = None
        self.Pekwh = None
        self.Pekws = None
        self.Ploss = None
        self.Pcu = None
        self.Pfe = None
        self.Pstr = None
        self.Pf = None
        self.Pw = None
        self.Pinv = None
        self.n = None
        self.cdcI = None
        self.Temp = None
        self.AccPbatt = None
        self.WLTCdist = None
        self.WLTCconpow = None
        self.bttcon = None
        self.crusdist = None
        self.ctId = None
        self.ctIq = None
        self.count=0
     def init(self, pole, btt, gear, tire, ip, ipm):
 
        self.acckm = np.zeros(self.num)
        self.wwrpm = np.zeros(self.num)
        self.Frolling = np.zeros(self.num)
        self.FAero = np.zeros(self.num)
        self.Fx = np.zeros(self.num)
        self.werpm = np.zeros(self.num)
        self.Tn = np.zeros(self.num)
        self.condPe = np.zeros(self.num)
        self.AccPe = np.zeros(self.num)
        self.AccPbatt = np.zeros(self.num)
        self.Temp = np.zeros(self.num)
        self.Temp[0] = 57.92  # 1st element here is a constant
 
        acc = np.zeros(self.num)
        dist = np.zeros(self.num)
        alpha = np.zeros(self.num)
        InertialL = np.zeros(self.num)
        ww = np.zeros(self.num)
        wr = np.zeros(self.num)
        we = np.zeros(self.num)
        Tw = np.zeros(self.num)
        Pe = np.zeros(self.num)
        circTn = np.zeros(self.num)
        regenDelay = np.zeros(self.num)
        Pn = np.ones(self.num)
 
        Pbatt = np.zeros(self.num)
        index = np.zeros(self.num, dtype=int)  # Pointer, using integer type
        Tnratio = np.zeros(self.num)
 
        self.Id = np.zeros(self.num)
        self.Iq = np.zeros(self.num)
        self.Pekwh = np.zeros(self.num)
        self.Pekws = np.zeros(self.num)
        self.Ploss = np.zeros(self.num)
        self.Pcu = np.zeros(self.num)
        self.Pfe = np.zeros(self.num)
        self.Pstr = np.zeros(self.num)
        self.Pf = np.zeros(self.num)
        self.Pw = np.zeros(self.num)
        self.Pinv = np.zeros(self.num)
        self.n = np.zeros(self.num)
        self.cdcI = np.zeros(self.num)
 
        self.rpmflag = np.ones(4100)
        tmprpm = np.zeros(4100)
        # ipm.rpm = np.append(ipm.rpm, 0)
        # ipm.Idc = np.append(ipm.Idc, 0)
        vx = np.array(ip['Vx'])
        self.acckm = np.diff(ip['Vx'], prepend=ip['Vx'][0])  # Calculate acceleration
        self.acckm[0] = 0  # Set the first element to 0
       
        acc = self.acckm / 3.6  # Col F - acceleration (m/s²)
       
        # # Col H - Cruising distance
        dist =vx * 1 / 3.6 * 1 + acc * 1/2
       
        # # Wheel shaft torque and power
        self.wwrpm = dist / (2 * np.pi * tire['Tirerw']) * 60  # Col I - ωw (rpm)
       
        ww = self.wwrpm / 60 * 2 * np.pi  # Col J - ωw
       
        alpha = acc / tire['Tirerw']  # Col K - angular acceleration
 
        angle = math.degrees(math.atan(ip['rdgrd']))  # E103
        slopesin = math.sin(math.radians(angle))  # D103
        slopecos = math.cos(math.radians(angle))  # D104
        InertialL =ip['GrossWt'] * acc
        self.Fgravity = ip['GrossWt'] * ip['gravity'] * slopesin
        self.Frolling[ip['crsPtn'] > 0] = ip['fr']*ip['GrossWt']*ip['gravity']*slopecos
        self.FAero = 0.5 *ip['p']*ip['Af']*ip['Cd'] * ((vx +ip['Vwind']) / 3.6) ** 2
        # Col P - Fx
        self.Fx = InertialL + self.Fgravity + self.Frolling + self.FAero
 
        if ip['VDswitch'] == 1:
            Tw = ip['J'] * alpha + tire['Tirerw'] * (self.Fgravity + self.Frolling + self.FAero)
        else:
            Tw = ip['J'] * alpha
 
        Pe = ww * Tw / 1000 / 3600  # Col S
 
        wr = ww * gear['gdr']  # Col X
        we = wr * pole / 2     # Col Y
        self.werpm = we * 60 / ((pole / 2) * 2 * np.pi)  # Col Z
        self.Tn = Tw/ gear['gdr']
        # Shift `self.Tn` by 1 position and set the first element to 0
        circTn = np.roll(self.Tn, 1)
        circTn[0] = 0
        if ip['zone'] == 1:
            regenDelay[(circTn >= 0) & (self.Tn < 0)] = 1
 
        self.condPe[:self.num] = -Pe
 
        # Apply condition for regeneration limit
        self.condPe[vx > btt['regen_limit']] = -Pe[vx > btt['regen_limit']] * (1 - btt['regen_ratio'])
 
        # Apply condition for alpha >= 0
        self.condPe[alpha >= 0] = Pe[alpha >= 0]
        self.AccPe = np.cumsum(-self.condPe)
        Pn[self.Tn < 0] = -1
        # idx = (ipm.rpm[:-1] < np.roll(ipm.rpm, -1)[:-1]) & (np.roll(ipm.Idc, -1)[:-1] < ipm.Idc[:-1])
        # self.rpmflag[idx] = 0  # OV
 
        tmprpm = ipm.rpm - ipm.increment
        tmprpm[0] = 0
 
        self.rpmflag = np.ones(4100)
        idx = (ipm.rpm < np.roll(ipm.rpm, -1)) & (np.roll(ipm.Idc, -1) < ipm.Idc)
        self.rpmflag[idx] = 0


        nacount = 0
        for idx in range(1, self.num):  
            # Col AZ:FCQ - Find the IPM position of the flag for the ongoing WLTC iteration
            condition = (self.rpmflag == 1) & (np.abs(self.werpm[idx]) >= tmprpm) & (np.abs(self.werpm[idx]) < ipm.rpm) & (np.abs(self.Tn[idx]) >= ipm.Tn)
            indices = np.where(condition)[0]
           
            if indices.size > 0:
                foundAt = indices[-1]  # Find the last occurrence
                index[idx] = foundAt
           
            # When flag found, Use the IPM Modeled values at its location
            if index[idx] != 0:  # This condition will satisfy Col AY
                # Col AK
                if self.Tn[idx] != 0:
                    Tnratio[idx] = (np.abs(self.Tn[idx]) - ipm.Tn[index[idx]]) / (ipm.Tn[index[idx] + 1] - ipm.Tn[index[idx]])
               
                self.Id[idx] = (ipm.Id[index[idx] + 1] - ipm.Id[index[idx]]) * Tnratio[idx] + ipm.Id[index[idx]]  # Col AH
                self.Iq[idx] = Pn[idx] * ((ipm.Iq[index[idx] + 1] - ipm.Iq[index[idx]]) * Tnratio[idx] + ipm.Iq[index[idx]])  # Col AI->AJ
                self.Pekwh[idx] = Pn[idx] * ((ipm.Pe[index[idx] + 1] - ipm.Pe[index[idx]]) * Tnratio[idx] + ipm.Pe[index[idx]])  # Col AL
                self.Pekws[idx] = self.Pekwh[idx] / 3600  # Col AM
                self.Ploss[idx] = Pn[idx] * (((ipm.Ploss[index[idx] + 1] - ipm.Ploss[index[idx]]) * Tnratio[idx] + ipm.Ploss[index[idx]]) / 3600)  # Col AN
                self.Pcu[idx] = (ipm.Pcu[index[idx] + 1] - ipm.Pcu[index[idx]]) * Tnratio[idx] + ipm.Pcu[index[idx]]  # Col A0
                self.Pfe[idx] = (ipm.Pfe[index[idx] + 1] - ipm.Pfe[index[idx]]) * Tnratio[idx] + ipm.Pfe[index[idx]]  # Col AP
                self.Pstr[idx] = (ipm.Pstr[index[idx] + 1] - ipm.Pstr[index[idx]]) * Tnratio[idx] + ipm.Pstr[index[idx]]  # Col AQ
                self.Pf[idx] = (ipm.Pfric[index[idx] + 1] - ipm.Pfric[index[idx]]) * Tnratio[idx] + ipm.Pfric[index[idx]]  # Col AR
                self.Pw[idx] = (ipm.Pwind[index[idx] + 1] - ipm.Pwind[index[idx]]) * Tnratio[idx] + ipm.Pwind[index[idx]]  # Col AS
                self.Pinv[idx] = (ipm.Pinv[index[idx] + 1] - ipm.Pinv[index[idx]]) * Tnratio[idx] + ipm.Pinv[index[idx]]  # Col AT
                self.n[idx] = (ipm.posin[index[idx] + 1] - ipm.posin[index[idx]]) * Tnratio[idx] + ipm.posin[index[idx]]  # Col AX
                self.cdcI[idx] = np.sqrt(self.Id[idx]**2 + self.Iq[idx]**2)  # Col AV
 
                # Col AF
                if Pn[idx] > 0:
                    Pbatt[idx] = self.Pekws[idx] / self.n[idx]
                elif vx[idx] >btt['regen_limit']and regenDelay[idx] != 1:
                    Pbatt[idx] = -(self.Pekws[idx] / self.n[idx] - (self.Pekws[idx] - np.abs(self.Ploss[idx])) * btt['regen_ratio'])
                else:
                    Pbatt[idx] = -self.Pekws[idx] / self.n[idx]
            else:
                # Count the number of rows without flag
                if self.Tn[idx] < 0:
                    nacount += 1  # AY194
            if self.n[idx] > 0:
                self.Temp[idx] = (ipm.Temp[index[idx] + 1] - ipm.Temp[index[idx]]) * Tnratio[idx] + ipm.Temp[index[idx]]
                self.count = self.count + 1
            else:
                self.Temp[idx] = self.Temp[idx - 1]

        self.AccPbatt = np.cumsum(-Pbatt)  # Col AG
 # Logical index of non-NaN elements
        nonNaNIndex = ~np.isnan(self.AccPbatt)

        # Find the last non-NaN index
        lastNonNaNIndex = np.where(nonNaNIndex)[0][-1]

        # Assign the value at the last non-NaN index, and negate it
        # obj.WLTCconpow = -obj.AccPbatt[lastNonNaNIndex]

        self.WLTCconpow = -self.AccPbatt[lastNonNaNIndex]
        self.WLTCdist = np.nansum(dist) / 1000
        self.bttcon = self.WLTCconpow / self.WLTCdist * 10
        self.crusdist = btt['charge'] / self.bttcon * 10
 
 

     def constTrq(self,arr,ipm):
        ctwerpm = list(range(1000, 20000, 1000)) + \
        list(range(1000, 20000, 1000)) + \
        list(range(500, 7001, 500)) + \
        list(range(7100, 7501, 100)) + \
        list(range(500, 4501, 500)) + \
        list(range(4520, 4701, 20))

            
        ctTn = np.zeros(76)
        ctTn[0:19] = arr[0]
        ctTn[19:38] = arr[1]
        ctTn[38:57] = arr[2]
        ctTn[57:76] = arr[3]
        ctindex = [0] * ( len(ctwerpm))
        cTratio = [0] * ( len(ctwerpm))

        self.ctId = [0] * len(ctwerpm)
        self.ctIq  = [0] * len(ctwerpm)

        tmprpm = [0] * 4100
        rpmflag = [1] * 4100
        for idx in range(len(ctwerpm)):
       
            ipm.Tn = np.append(ipm.Tn, 0)  # Creating additional array element  
        #    for iter in range( 1,4100):
        #         tmprpm[0] = 0
        #         tmprpm[iter] = ipm.rpm[iter] - ipm.increment
        #         if (self.rpmflag[iter - 1] == 1 and np.abs(self.werpm[idx]) >= tmprpm[iter-1] and np.abs(self.werpm[idx]) < ipm.rpm[iter-1] and np.abs(self.Tn[idx]) >= ipm.Tn[iter-1] ):
        #             index[idx] = iter     
            for iter in range(1,4100):
                tmprpm[0] = 0
                tmprpm[iter] = ipm.rpm[iter] - ipm.increment
                    
                if self.rpmflag[iter - 1] == 1 and abs(ctwerpm[idx]) >= tmprpm[iter-1] and abs(ctwerpm[idx]) < ipm.rpm[iter-1] and abs(ctTn[idx]) >= ipm.Tn[iter-1] :  
                    ctindex[idx] = iter
                    # break
            ipm.Tn = ipm.Tn[:-1] 

            if ctindex[idx] != 0:  # 
                if ctTn[idx] != 0:
                    cTratio[idx] = np.real((abs(ctTn[idx]) - ipm.Tn[ctindex[idx]-1]) / (
                            ipm.Tn[ctindex[idx] ] -ipm.Tn[ctindex[idx]-1]) ) # Col AK

                self.ctId[idx] = np.real((ipm.Id[ctindex[idx] ] - ipm.Id[ctindex[idx]-1]) * cTratio[idx] + ipm.Id[
                    ctindex[idx]-1] ) # Col AH
                self.ctIq[idx] = np.real((ipm.Iq[ctindex[idx] ] -ipm.Iq[ctindex[idx]-1]) * cTratio[idx] + ipm.Iq[
                    ctindex[idx]-1])  # Col AI
            else:
                self.ctId[idx] = None
                self.ctIq[idx] = None


    