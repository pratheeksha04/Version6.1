import cmath
import numpy as np
import math
import pandas as pd
from math import atan, sqrt, cos, sin, radians, degrees

class ipmclass:
    def __init__(self):
        self.initial = None
        self.increment = None
        self.rpm = None
        self.we = None
        self.ppsi1 = None
        self.ppsi2 = None
        self.oLd = None
        self.oLq = None
        self.MtpvId = None
        self.MtpvIq = None
        self.webwe = None
        self.IPMstatus = None
        self.Id = None
        self.Iq = None
        self.Idc = None
        self.Irms = None
        self.Vd = None
        self.Vq = None
        self.Vdc = None
        self.Tn = None
        self.Pe = None
        self.PF = None
        self.P = None
        self.reltrq = None
        self.Pbtt = None
        self.Ploss = None
        self.Pcu = None
        self.Pfe = None
        self.Pstr = None
        self.Pfric = None
        self.Pwind = None
        self.Pinv = None
        self.posin = None
        self.negan = None
        self.n = None
        self.Temp = None
        self.psipm = None
        self.beta = None
        self.Im = None
        self.tmpId = None
        self.tmpIq = None
        self.plaId = None
        self.plaIq = None
        self.Ld = None
        self.Lq = None
        self.e = None
        self.PsiArr = None
        self.psi = None
        self.Hdmat = None
        self.Hqmat = None


    def complex_radians_to_degrees(z):
        """
        Converts the real and imaginary parts of a numpy array of complex numbers from radians to degrees.
        """
        # Initialize an empty list to hold the results
        result = []

        # Loop through the numpy array
        for i in range(len(z)):
            real_part = z[i].real
            imaginary_part = z[i].imag
            degrees_real = math.degrees(real_part)
            degrees_imaginary = math.degrees(imaginary_part)
            res = complex(degrees_real, degrees_imaginary)
            result.append(res)
        
        # Convert the result list back to a numpy array
        result_array = np.array(result)
        return result_array


    def complex_degrees_to_radians(z):
        result = []

        # Loop through the numpy array
        for i in range(len(z)):
            real_part_degrees = z[i].real
            imaginary_part_degrees = z[i].imag
            real_part_radians = math.radians(real_part_degrees)
            imaginary_part_radians = math.radians(imaginary_part_degrees)
            res = complex(real_part_radians, imaginary_part_radians)
            result.append(res)
        
        # Convert the result list back to a numpy array
        result_array = np.array(result)
        return result_array

    def init(self, mot, DTtab, DTnum, PLmat, tnflag, peflag, const):
        
        temp = np.arange(self.initial, 19900, self.increment).tolist()
        # temp = self.initial + np.arange(100) * self.increment
        # temp = self.initial + 0.99 * self.increment

        nrpm = len(temp)
        prctg = [i * 2.5 for i in range(int(100 / 2.5) + 1)]  # col B\
        prctg[0] = 0.000001
        nprctg = len(prctg)
        num = nrpm * nprctg

        # idc = [0] * nprctg
        # for idx in range(nprctg):
        #     idc[idx] = prctg[idx] * mot['cur'] / 100

        # Initialization as lists
        ipm_status = [1] * num  # Col AQ
        Lambda = [0] * num  # Col AL
        check = [1] * num

        cI = np.concatenate(([700], np.arange(650, -1, -25)))

        
        idx = 0  

        wr = np.zeros(num)  # Col D
        self.we = np.zeros(num)  # Col E
        self.rpm = np.zeros(num)  # Col C
        idc = np.zeros(nprctg)
        self.Idc = np.zeros_like(num, dtype=complex)   # Col AU
        tXIdc = np.zeros(num)  # Col AU*Col AW




        self.ppsi1 = np.zeros(num)
        self.ppsi2 = np.zeros(num)
        self.oLd = np.zeros(num)
        self.oLq = np.zeros(num)
        dif = np.zeros(num)
        E = np.zeros(num)
        MTPAid = np.zeros(num)
        MTPAiq = np.zeros(num)
        MTPAbeta = np.zeros(num)
        MTPAIrms = np.zeros(num)
        MTPAtn = np.zeros(num)
        
        wea = np.zeros(num)
        CPSRid = np.zeros_like(num, dtype=complex)
        CPSRiq = np.zeros_like(num, dtype=complex)
        CPSRIrms = np.zeros_like(num, dtype=complex)
        CPSRbeta = np.zeros(num)
        CPSRTn = np.zeros(num)
        XTn = np.zeros(num)
        self.MtpvId = np.zeros(num)
        self.MtpvIq = np.zeros(num)
        MtpvIm = np.zeros(num)
        MtpvIrms = np.zeros(num)
        mtpvbeta = np.zeros(num)
        MtpvTn = np.zeros(num)
        Lambda = np.zeros(num)
        Hd = np.zeros(num)
        Hq = np.zeros(num)
        H2 = np.zeros(num)
        Tlin = np.zeros(num)
        kofM123 = np.zeros(num)
        kofM45 = np.zeros(num)
        kK0 = np.zeros(num)
        self.Tn = np.zeros(num)
        Hwea = np.zeros(num)
        Hwearpm = np.zeros(num)
        self.IPMstatus = np.zeros(num)
        self.Id = np.zeros(num)
        self.Iq = np.zeros(num)
        self.Vd = np.zeros(num)
        self.Vq = np.zeros(num)
        self.Vdc = np.zeros(num)
        self.PF = np.zeros(num)
        self.Irms = np.zeros(num)
        self.P = np.zeros(num)
        self.reltrq = np.zeros(num)
        self.Pe = np.zeros(num)
        self.Temp = np.zeros(num)


        XVd = np.zeros(num)
        XVq = np.zeros(num)
        Vdc = np.zeros(num)
        iIm = np.zeros(num)
        ibeta = np.zeros(num)
        delta = np.zeros(num)
        Pe = np.zeros(num)
        Rs = np.zeros(num)
        self.Pcu = np.zeros(num)
        self.Pfe = np.zeros(num)
        self.Pstr = np.zeros(num)
        self.Pfric = np.zeros(num)
        self.Pwind = np.zeros(num)
        self.Pinv = np.zeros(num)
        self.Ploss = np.zeros(num)
        self.Pbtt = np.zeros(num)
        self.n = np.zeros(num)
        self.posin = np.zeros(num)
        self.Pe = np.zeros(num)
        self.negan = np.zeros(num)
        Psat = np.zeros(num)
        Pon = np.zeros(num)
        Poff = np.zeros(num)
        Pfmj = np.zeros(num)
        Prr = np.zeros(num)

        #Calculate the final comprehensive RPM array, ωr and ωe
        self.rpm[:num] = np.repeat(temp, nprctg)
        wr = self.rpm / 60 * 2 * np.pi
        self.we = (self.rpm / 60 * 2 * np.pi) * (mot['pole'] / 2)
     
        #Calculate raw and tuned XIdc arrays
        idc = np.array(prctg) * mot['cur'] / 100
        self.Idc = np.tile(idc, nrpm)
        tXIdc = self.Idc * np.array(PLmat['tuning'])

        #Initialization
        self.psipm = PLmat['copy']
        piq1 = np.zeros(nprctg)
        piq2 = np.zeros(nprctg)
        psi1 = np.zeros(nprctg)
        psi2 = np.zeros(nprctg)
        Ld1 = np.full(nprctg, mot['ld'] * mot['unit'])
        Ld2 = np.full(nprctg, mot['ld'] * mot['unit'])
        Lq1 = np.full(nprctg, mot['lq'] * mot['unit'])
        Lq2 = np.full(nprctg, mot['lq'] * mot['unit'])

        #The current(I) array for ld, lq, ψ
        cI = np.concatenate(([700], np.arange(650, -1, -25)))

        for idx in range(nprctg):
            #Calculate the combinations of ψ, ld and lq arrays
            #pid,pidq,ppsi->id,iq,ψ obtained from Psi_PM

            #XLOOKUP(tXIdc(idx),cI,cI/PsiArr,flux,-1,-1)
            maxind = np.where(cI <= tXIdc[idx])[0][0] if np.any(cI <= tXIdc[idx]) else None
            if (maxind>=0):
                piq1[idx] = cI[maxind]  
                psi1[idx] =PLmat['PsiArr'][maxind]
            else:
                piq1[idx] = mot['flux']
                psi1[idx] = mot['flux'] 

            #XLOOKUP(tXIdc(idx),cI,cI/PLmat.PsiArr,flux,1,-1)
            minind = np.where(cI >= tXIdc[idx])[0][-1] if np.any(cI >= tXIdc[idx]) else None
            if (minind>=0):
                piq2[idx] = cI[minind]  # Col J
                psi2[idx] = PLmat['PsiArr'][minind]
            else:
                piq2[idx] = mot['flux']
                psi2[idx] = mot['flux'] 


            if const != 1:
                #XLOOKUP(tXIdc(idx),cI,PLmat.LdArr/PLmat.LqArr,0,-1,1)            
                if maxind>=0:
                    Ld1[idx] = PLmat['LdArr'][maxind]
                    Lq1[idx] = PLmat['LqArr'][maxind]
                else:
                    Ld1[idx] = 0
                    Lq1[idx] = 0
            
                if minind>=0:
                    Ld2[idx] = PLmat['LdArr'][minind]
                    Lq2[idx] = PLmat['LqArr'][minind]
                else:
                    Ld2[idx] = 0
                    Lq2[idx] = 0

        piq1 = np.tile(piq1, nrpm)
        piq2 = np.tile(piq2, nrpm)
        self.ppsi1 = np.tile(psi1, nrpm)
        self.ppsi2 = np.tile(psi2, nrpm)


        if const != 1:
            self.psipm = (tXIdc - piq1) / (piq2-piq1) * (self.ppsi2 - self.ppsi1) + self.ppsi1

        Ld1 = np.tile(Ld1, nrpm)
        Ld2 = np.tile(Ld2, nrpm)
        Lq1 = np.tile(Lq1, nrpm)
        Lq2 = np.tile(Lq2, nrpm)


        self.oLd = (self.Idc - piq1) / (piq2 - piq1) * (Ld2 - Ld1) + Ld1  # Optimized Ld (Col Q)
        self.oLq = (self.Idc - piq1) / (piq2 - piq1) * (Lq2 - Lq1) + Lq1  # Optimized Lq (Col R)
        dif = self.oLq - self.oLd  # Difference: Col T
        E = self.oLq / self.oLd # ξ: Col S

        # MTPA variables
        MTPAid = (self.psipm - np.sqrt(self.psipm**2 + (8 * self.Idc**2 * dif**2))) / (4 * dif)
        MTPAiq = np.sqrt(self.Idc**2 - MTPAid**2)  # Col X
        

        MTPAbeta = np.degrees(np.arctan(-MTPAid/ MTPAiq))
        MTPAIrms = np.sqrt( MTPAid**2 + MTPAiq**2 ) / np.sqrt(2)
        MTPAtn = 3/4 * mot['pole'] * ( self.psipm * MTPAIrms * np.cos(np.radians(MTPAbeta)) + dif * ( MTPAIrms ** 2 ) * np.sin(np.radians(2 * MTPAbeta))/2 )
        wea = mot['vol'] / np.sqrt((self.oLq * MTPAiq)**2 + (self.oLd * MTPAid + self.psipm)**2)  # Col AA
        
        # CPSR 
        CPSRid = (self.psipm / self.oLd - np.sqrt((self.psipm*self.psipm) / (self.oLd**2) + (E**2 - 1) * (self.psipm*self.psipm/(self.oLd**2) + E**2 * self.Idc**2 - mot['vol']**2 / (self.we**2 * self.oLd**2) ) + 0j)) / (E**2 - 1)  # Col AE
        
        # Col AF
        CPSRiq = np.full(num, np.sqrt(0.001+0j))
        ind = (self.Idc ** 2 - CPSRid ** 2) > 0
        CPSRiq[ind] = np.sqrt(self.Idc[ind] ** 2 - CPSRid[ind] ** 2)
        CPSRIrms = np.sqrt( CPSRid**2 + CPSRiq**2 +0j) / np.sqrt(2)
        CPSRbeta = ipmclass.complex_radians_to_degrees(np.arctan(-CPSRid / CPSRiq ))
        
        CPSRTn = (3/4 * mot['pole'] * (self.psipm * CPSRIrms * np.cos(ipmclass.complex_degrees_to_radians(CPSRbeta)) +
                dif * CPSRIrms**2 * np.sin(ipmclass.complex_degrees_to_radians(2 * CPSRbeta)) / 2))
        # print("CPSRTn",CPSRTn)
        

        
        #MTPV variables
        #ipmif = -psipm./oLd; %Col AI       
        Lambda = (-self.oLq * self.psipm + np.sqrt((self.oLq**2) * (self.psipm**2) + (8 * (dif**2) * ((mot['vol'] / self.we)**2)))) / (4 * (-dif))
        self.MtpvId = (Lambda - self.psipm) / self.oLd
        self.MtpvIq = np.sqrt((mot['vol'] / self.we)**2 - Lambda**2) / self.oLq
        MtpvIm = np.sqrt(self.MtpvId**2 + self.MtpvIq**2)
        MtpvIrms = MtpvIm / np.sqrt(2)
        mtpvbeta = np.rad2deg(np.arctan(-self.MtpvId / self.MtpvIq))
        MtpvTn = (3/4 * mot['pole'] * (self.psipm * MtpvIrms * np.cos(np.deg2rad(mtpvbeta)) + dif * MtpvIrms**2 * np.sin(np.deg2rad(2 * mtpvbeta)) / 2))

        # MTPV checker
        check = np.zeros(num)
        check[MtpvIm < self.Idc] = 1

        # Initialize IPMstatus array
        self.IPMstatus = np.full(num, 2)

        # Perform the status calculation
        for idx in range(1, num):  # Note: Python is zero-indexed, so range starts at 1
            if check[idx] == 1:
                if (self.IPMstatus[idx - 1] != 0) and (self.IPMstatus[idx - 1] != 1):
                    self.IPMstatus[idx] = 1  # MTPV
                else:
                    self.IPMstatus[idx] = 0  # Skip
            else:
                if self.we[idx] < wea[idx]:
                    self.IPMstatus[idx] = 2  # MTPA
                else:
                    self.IPMstatus[idx] = 3  # CPSR

        self.Id = self.MtpvId
        self.Iq = self.MtpvIq


        # Update Id and Iq based on IPMstatus
        self.Id[self.IPMstatus == 2] = MTPAid[self.IPMstatus == 2]
        self.Iq[self.IPMstatus == 2] = MTPAiq[self.IPMstatus == 2]
        self.Id[self.IPMstatus == 3] = np.real(CPSRid[self.IPMstatus == 3])
        self.Iq[self.IPMstatus == 3] = np.real(CPSRiq[self.IPMstatus == 3])

        
        
        #Compute Voltage, Torque and Power components corresponding to comprehensive Id and Iq
        XVd = mot['res'] * self.Id - self.we * self.oLq * self.Iq
        XVq = mot['res'] * self.Iq + self.we * (self.oLd * self.Id + self.psipm)
        XVdc = np.sqrt(XVd**2 + XVq**2)


        # Col BA
        XTn = CPSRTn
        XTn[self.IPMstatus == 1] = MtpvTn[self.IPMstatus == 1]
        XTn[self.we < wea] = MTPAtn[self.we < wea]

   
        # Calculate Hd, Hq and H² variables using DigitalTwin table
        Hd = DTtab[DTnum, 4] + DTtab[DTnum, 2] * self.Id * 0.000001
        Hq = DTtab[DTnum, 3] * self.Iq * 0.000001 + DTtab[DTnum, 5]
        H2 = (Hd / DTtab[DTnum, 0])**2 + (Hq / DTtab[DTnum, 1])**2

        # Calculate linear torque
        Tlin = 3/2 * (mot['pole'] / 2) * (Hd * self.Iq - Hq * self.Id)
        
        if DTnum == 0 or DTnum == 2:
            kofM123 = DTtab[DTnum, 6] * np.sqrt(H2) / np.sqrt(1 + (np.sqrt(H2) * DTtab[DTnum, 6])**2)
        elif DTnum == 1:
            kofM123 = np.tanh(DTtab[DTnum, 6] * np.sqrt(H2))
        else:
            kofM123 = 0

        # Calculate k of Methods 4 or 5
        if DTnum == 3:
            kofM45 = np.arctan(DTtab[DTnum, 6] * np.sqrt(H2))
        elif DTnum == 4:
            kofM45 = 1 - np.exp(-DTtab[DTnum, 6] * np.sqrt(H2))
        else:
            kofM45 = DTtab[DTnum, 6] * np.sqrt(H2) / np.sqrt(1 + (np.sqrt(H2) * DTtab[DTnum, 6])**2)

        # Calculate kK0
        if 0 <= DTnum <= 2:
            kK0 = kofM123 / np.sqrt(H2)
        else:
            kK0 = kofM45 / np.sqrt(H2)

        
        Tcal = Tlin * kK0
        # print("kK0",kK0)

        # Calculate corresponding ωea and ωea(rpm)
        Hwea = np.zeros(num)
        sts2 = self.IPMstatus == 2
        Hwea[sts2] = XVdc[sts2] / np.sqrt(Hd[sts2]**2 + Hq[sts2]**2)

        # Proceed to compute other values
        iIm = np.sqrt(self.Id**2 + self.Iq**2)
        ibeta = np.rad2deg(np.arctan(-self.Id / self.Iq))
        self.Vd = mot['res'] * self.Id - self.oLq * self.we * self.Iq
        self.Vq = mot['res'] * self.Iq + self.we * (self.oLd * self.Id + self.psipm)
        self.Vdc = np.sqrt(self.Vd**2 + self.Vq**2)
        delta = np.rad2deg(np.arctan(-self.Vd / self.Vq))
        self.PF = np.cos(np.deg2rad(delta - ibeta))
        self.Irms = iIm / np.sqrt(2)
        self.P = (self.Irms * self.Vdc) / 1000
        if tnflag == 1:
            self.Tn = XTn
        else:
            self.Tn = Tcal
        # print("Tcal",Tcal)
        self.reltrq = (3/4 * mot['pole'] * (dif * (self.Irms / np.sqrt(2))**2 * np.sin(np.deg2rad(2 * ibeta)) / 2)) / self.Tn
        # print("self.reltrq",self.reltrq)

        if peflag == 1:
            self.Pe = wr * self.Tn / 1000
        else:
            self.Pe = Hwea * self.Tn / 1000

        self.beta = ibeta[nprctg:nprctg*2]
        self.Im = iIm[nprctg:nprctg*2] / (2 ** 0.5)

        # Find the first index where check is 1
        idx = next((i for i, val in enumerate(check) if val == 1), None)
        self.webwe = self.we[idx] if idx is not None else None

        self.Hdmat = PLmat['Hdmat']
        self.Hqmat = PLmat['Hqmat']
        self.Ld = PLmat['Ld']
        self.Lq = PLmat['Lq']
        self.psi = PLmat['Psi']
        self.PsiArr = PLmat['PsiArr']
        self.e = PLmat['LqArr'] / PLmat['LdArr']




    def losscalc(self, mot, inv, igbt, Temp, Flag, num):
        # Implement the losscalc method
        self.Temp = Temp['A'] * self.rpm + (Temp['B'] * (self.Tn)**2 - Temp['C'] * self.Tn + Temp['iniTemp'])  # Col CP
        Rs = mot['res'] * (1 + (self.Temp - Temp['RoomT']) / (234.5 + Temp['RoomT']))  # Col CQ

        # IGBT/FRD Modeling for inverter loss calculation
        # current and modulation variables
        iIrms = self.Irms / np.sqrt(2)  # Col DB
        Mod = self.Vdc / mot['DCV']  # Col DC

        # Initialize different kinds of losses
        self.Pcu = np.zeros(num)  # Col CI - Copper loss
        if Flag['Pcu'] == 1:
            if Flag['temp'] == 1:
                self.Pcu = (3/2 * Rs * ((self.Id)**2 + (self.Iq)**2)) / 1000
            else:
                self.Pcu = (3/2 * mot['res'] * ((self.Id)**2 + (self.Iq)**2)) / 1000

        self.Pfe = np.zeros(num)  # Col CJ - Iron loss
        if Flag['Pfe'] == 1:
            self.Pfe = (mot['cfe'] * (self.we**1.6) * ((self.oLd * self.Id + self.psipm)**2 + (self.oLq * self.Iq)**2)) / 1000  # 1.6 from CJ28
        elif Flag['Pfe'] == 2:
            self.Pfe = (3/(2*200) * (self.we**2 * (self.oLd * self.Id + self.psipm)**2 + (self.we * self.oLq * self.Iq)**2)) / 1000  # 200 from: WLTC E36
        self.Pfe = np.roll(self.Pfe, -1)

        self.Pstr = np.zeros(num)  # Col CK - Stray loss
        if Flag['Pstr'] == 1:
            self.Pstr = mot['cstr'] * mot['Cstrunit'] * (self.we)**2 * ((self.Id)**2 + (self.Iq)**2) / 1000

        self.Pfric = np.zeros(num)  # Col CL - Friction loss
        if Flag['Pf'] == 1:
            self.Pfric = (0.000001 * mot['cPfric'] * (self.rpm)**2 - 0.0003 * self.rpm + 1.4471) / 1000 * (max(self.Pe) / 80)

        self.Pwind = np.zeros(num)  # Col CM - Windage loss
        if Flag['Pw'] == 1:
            self.Pwind = (mot['cPwind'] / 10000000) * ((self.we) / (mot['pole'] / 2))**3 / 1000

        self.Pinv = np.zeros(num)  # Col CN - Inverter loss
        if Flag['Pinv'] == 1:
            self.Pinv = 3 * ((2 * mot['vol'] * self.Idc * (inv['tr'] + inv['tf']) * 10**-6) +
                             (inv['von'] * (2/np.pi) * self.Idc * inv['ton'] * 10**-6) +
                             ((self.Vdc) / 2 * self.Idc / 3 * inv['trr'] * 10**-6)) * mot['freq'] / 1000  # Col CS - Mode1Pinv
        elif Flag['Pinv'] == 2:
            Psat = 2 * iIrms**2 * igbt['A1'] * (1/8 + igbt['modulation'] * self.PF / (3 * np.pi)) + \
                   np.sqrt(2) * iIrms * igbt['A0'] * (1 / (2 * np.pi) + igbt['modulation'] * self.PF / 8)  # Col CV
            Pfmj = 2 * iIrms**2 * igbt['B1'] * (1/8 - igbt['modulation'] * self.reltrq / (3 * np.pi)) + \
                   np.sqrt(2) * iIrms * igbt['B0'] * (1 / (2 * np.pi) - igbt['modulation'] * self.reltrq / 8)  # Col CY
            Pon = (igbt['C3'] * (self.Irms)**3 + igbt['C2'] * (self.Irms)**2 + (igbt['C1'] * self.Irms) + igbt['C0']) / \
                  np.pi * mot['freq'] * Mod  # Col CW
            Poff = (igbt['D3'] * (self.Irms)**3 + igbt['D2'] * (self.Irms)**2 + igbt['D1'] * self.Irms + igbt['D0']) / \
                   np.pi * mot['freq'] * Mod  # Col CX
            Prr = (igbt['E3'] * (self.Irms)**3 + igbt['E2'] * (self.Irms)**2 + igbt['E1'] * self.Irms + igbt['E0']) / \
                  np.pi * mot['freq'] * Mod  # Col CZ
            self.Pinv = (Psat + Pon + Poff + Pfmj + Prr) * 6 / 1000000  # Col CU - Mode2Pinv

        # Calculate other cumulative losses and efficiencies
        # n: η=Efficiency, posin=positive efficiency, negan=negative efficiency
        self.Ploss = self.Pcu + self.Pfe + self.Pstr + self.Pfric + self.Pwind + self.Pinv  # Col CH
        self.Pbtt = self.Pe + self.Ploss  # Col CG
        iPe = 3/2 * (self.Id * self.Vd + self.Iq * self.Vq) / 1000  # Col BN
        self.n = (self.Pe) / iPe  # Col CC
        self.posin = (self.Pe) / (self.Pbtt)  # Col CD
        # Col CE
        self.negan = (self.Pe - self.Ploss) / self.Pe
        idx = (self.Pe - self.Ploss) / self.Pe <= 0
        self.negan[idx] = 0


    @staticmethod
    def graphtool(IPMstatus, Id, Iq, Tn, Pe):
        gt = {}
        num = len(IPMstatus)
        gt['MaId'] = np.zeros(num)
        gt['MaIq'] = np.zeros(num)
        gt['MaTn'] = np.zeros(num)
        gt['MaPe'] = np.zeros(num)
        gt['CId'] = np.zeros(num)
        gt['CIq'] = np.zeros(num)
        gt['CTn'] = np.zeros(num)
        gt['CPe'] = np.zeros(num)
        gt['MvId'] = np.zeros(num)
        gt['MvIq'] = np.zeros(num)
        gt['MvTn'] = np.zeros(num)
        gt['MvPe'] = np.zeros(num)

        gt['MaId'][IPMstatus == 2] = Id[IPMstatus == 2]
        gt['MaIq'][IPMstatus == 2] = Iq[IPMstatus == 2]
        gt['MaTn'][IPMstatus == 2] = Tn[IPMstatus == 2]
        gt['MaPe'][IPMstatus == 2] = Pe[IPMstatus == 2]

        gt['CId'][IPMstatus == 3] = Id[IPMstatus == 3]
        gt['CIq'][IPMstatus == 3] = Iq[IPMstatus == 3]
        gt['CTn'][IPMstatus == 3] = Tn[IPMstatus == 3]
        gt['CPe'][IPMstatus == 3] = Pe[IPMstatus == 3]

        gt['MvId'][IPMstatus == 1] = Id[IPMstatus == 1]
        gt['MvIq'][IPMstatus == 1] = Iq[IPMstatus == 1]
        gt['MvTn'][IPMstatus == 1] = Tn[IPMstatus == 1]
        gt['MvPe'][IPMstatus == 1] = Pe[IPMstatus == 1]

        return gt

    @staticmethod
    def efficiency(nrpm, ptg, IPMstatus, posin, negan, Tn, Pe):
        effposiTn = np.full((len(ptg) - 1, nrpm), np.nan)
        effposiPwr = np.full((len(ptg) - 1, nrpm), np.nan)
        effnegaTn = np.full((len(ptg) - 1, nrpm), np.nan)
        effnegaPwr = np.full((len(ptg) - 1, nrpm), np.nan)

        for ind in range(len(ptg) - 1):
            for idx in range(nrpm):
                # Positive efficiency
                if (posin[idx] >= ptg[ind]) and (posin[idx] < ptg[ind + 1]) and (IPMstatus[idx] != 0):
                    effposiTn[ind, idx] = Tn[idx]
                    effposiPwr[ind, idx] = Pe[idx]

                # Negative efficiency
                if (negan[idx] >= ptg[ind]) and (negan[idx] < ptg[ind + 1]):
                    effnegaTn[ind, idx] = -Tn[idx]
                    if IPMstatus[idx] != 0:
                        effnegaPwr[ind, idx] = -Pe[idx]

        return effposiTn, effposiPwr, effnegaTn, effnegaPwr

    @staticmethod
    def torquemap(ptg, nrpm, Tn, Id, Iq):
        trqId = np.zeros((len(ptg) - 1, nrpm))
        trqIq = np.zeros((len(ptg) - 1, nrpm))

        for ind in range(len(ptg) - 1):
            idx = (Tn >= ptg[ind]) & (Tn < ptg[ind + 1])
            trqId[ind, idx] = Id[idx]
            trqIq[ind, idx] = Iq[idx]

        return trqId, trqIq

    @staticmethod
    def temperaturemap(arr, nrpm, Temp, IPMstatus, Tn, Pe, Id, Iq):
        tmpTn = np.full((13, nrpm), np.nan)
        tmpPwr = np.full((13, nrpm), np.nan)
        tmpId = np.zeros((13, nrpm))
        tmpIq = np.zeros((13, nrpm))

        for ind in range(13):
            for idx in range(nrpm):
                if (Temp[idx] >= arr[ind]) and (Temp[idx] < arr[ind + 1]):
                    if IPMstatus[idx] != 0:
                        tmpTn[ind, idx] = Tn[idx]
                        tmpPwr[ind, idx] = Pe[idx]
                    tmpId[ind, idx] = Id[idx]
                    tmpIq[ind, idx] = Iq[idx]

        return tmpTn, tmpPwr, tmpId, tmpIq

    @staticmethod
    def filter(crr, rpm, Id, Iq):
        plaId = np.full((len(crr), len(rpm)), np.nan)
        plaIq = np.full((len(crr), len(rpm)), np.nan)

        for ind in range(len(crr)):
            idx = np.round(rpm) == np.round(crr[ind])
            plaId[ind, idx] = Id[idx]
            plaIq[ind, idx] = Iq[idx]

        return plaId, plaIq
