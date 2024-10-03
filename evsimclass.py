import numpy as np
import math
import cmath
class evsimclass:
    def __init__(self):
        self.rpm = None
        self.T = None
        self.maxT = None
        self.b = None
        self.ptgId = None
        self.ptgIq = None
        self.MTPATe = None
        self.MTPAwe = None  # Variable to store MTPA ωe value
        self.MTPAImax = None
        self.MTPArpm = None
        self.MaxSpdrpm = None  # Max speed rpm value obtained from EVtab
        self.status = None  # EVtab status variable
        self.absearch = None  # EVtab absearch variable
        self.trqTem = None  # Torque array that will store all the 13 variations of Tem
        self.mrpm = None  # Combined array of maxspeed, const torque and mtpv rpm
        self.vLimId = None
        self.vLimIq = None
        self.vLimTn = None
        self.vLim_iq = None
        self.vLim_I = None
        self.MaxPwrId = None
        self.MaxPwrIq = None
        self.MaxPwrTn = None
        self.Maxpwr_iq = None
        self.MaxPwr_I = None
        self.MTPVId = None
        self.MTPVIq = None
        self.MTPVTn = None
        self.MTPV_iq = None
        self.MTPV_I = None
        self.PfId = None
        self.PfIq = None
        
    def init(self, mot, MaxSpdwe):
        deg = np.arange(0, 91)  # Creates an array from 0 to 90
        ind = np.arange(0, 651, 25)
        ind[0] = 5
        ind[-1] = 700
        ptg = ind / ind[-1]
        numi = len(ind)
        numd = len(deg)

        # Calculate torque and find the maximum at each percentage and the corresponding angle(degree)
        self.T = np.zeros((numi, numd))
        self.maxT = np.zeros(numi)
        self.b = np.zeros(numi)
        for idx in range(numi):
            for dind in range(numd):
                self.T[idx, dind]= 3 / 4 * mot['pole'] * (
                (mot['flux'] * (ptg[idx] * mot['DCC']) * np.cos(np.deg2rad(deg[dind]))) +
                (mot['d'] * (ptg[idx] * mot['DCC']) ** 2 * np.sin(np.deg2rad(2 * deg[dind]))) / 2
                )
            self.maxT[idx] = np.max(self.T[idx])
            self.b[idx] = deg[np.argmax(self.T[idx])]
                
        #%Calculate Id,Iq at 25%,50%,75%,100% 
        arr = ((np.arange(25, 101, 25) / 100) * 480* np.sqrt(2))
        self.ptgId = np.zeros((4, len(deg)))
        self.ptgIq = np.zeros((4, len(deg)))
        for ind in range(4):
            for idx in range(len(deg)):
                self.ptgId[ind, idx] = -arr[ind] * np.sin(np.deg2rad(deg[idx]))
                self.ptgIq[ind, idx] = arr[ind] * np.cos(np.deg2rad(deg[idx]))

        self.T=self.T.T
        self.maxT=self.maxT.T
        self.b=self.b.T

        #Calculate ω and ωe - present in Status table
        self.rpm = list(range(100,65000,100))
        self.rpm=np.array(self.rpm)
        self.statw = self.rpm * 2 * np.pi/ 60
        self.statwe = self.statw*(mot['pole']/2)
        nrpm=int(len(self.rpm))

        #%Calculate MTPA (ωea) and constant torque variables
        ct = evsimclass.constTrq(mot, self.statw, self.statwe)#replcae mot with self
        #%Calculate Maxpower variables
        mp = evsimclass.maxPower(mot, self.statw, self.statwe)#replcae mot with self
        #%Calculate Maxpower variables
        mv = evsimclass.mtpv(mot, self.statw, self.statwe,nrpm)#replcae mot with self
        
        
        # #%Basic MTPA (ωea) parameters
        MTPAid = (mot['flux'] - math.sqrt((mot['flux'] ** 2) + 8 * (mot['cur'] ** 2) * (mot['d'] ** 2))) / (4 * mot['d'])
        MTPAiq = math.sqrt(mot['cur'] ** 2 - MTPAid ** 2)
        self.MTPAImax = math.sqrt(MTPAid ** 2 + MTPAiq ** 2)
        MTPAbeta = math.degrees(math.atan(-MTPAid / MTPAiq))
        
        MTPATem = 3 *mot['pole']/4 * (mot['flux']- mot['d']*MTPAid) * MTPAiq   
        self.MTPATe = (3 / 4) * mot['pole'] * (mot['flux'] * self.MTPAImax / math.sqrt(2) * math.cos(math.radians(MTPAbeta)) + mot['d'] * (self.MTPAImax / math.sqrt(2)) ** 2 * math.sin(math.radians(2 * MTPAbeta)) / 2)
        
        self.MTPAwe = mot['vol'] / math.sqrt((mot['lq'] * mot['unit'] * MTPAiq) ** 2 + (mot['ld'] * mot['unit'] * MTPAid + mot['flux']) ** 2)
        self.MTPArpm = self.MTPAwe * 60 / (mot['pole'] / 2 * 2 * math.pi)
      
        #%ωeb search table  
        maxind = np.where(mv['Im']>=mot['cur'])[0]
        if len(maxind) == 0:
            mv['wMax'] = 0
            mv['ImMax'] = 0
        else:
            maxind = maxind[-1]
            mv['ImMax'] = mv['Im'][maxind]
            mv['wMax'] = self.statwe[maxind]
    
        minind = np.where(mv['Im'] <= mot['cur'])[0]
        if len(minind) == 0:
            mv['wMin'] = 0
            mv['ImMin'] = 0
        else:
            minind = minind[0]
            mv['ImMin'] = mv['Im'][minind]
            mv['wMin'] = self.statwe[minind]

        # #%Basic MTPV (ωeb) parameters
        webwe = mv['wMin'] - (mv['ImMin'] - mot['cur']) * (mv['wMin'] - mv['wMax']) / (mv['ImMin'] - mv['ImMax'])
        MTPVrpm =  webwe * 60 / ( (mot['pole']/2) * 2 * np.pi )
        MTPVlambda = (-(mot['lq']*mot['unit']) * mot['flux'] + np.sqrt((mot['lq']*mot['unit']) ** 2 * mot['flux'] ** 2 + 8 * mot['d'] ** 2 * (mot['vol'] / webwe) ** 2)) / (4 * -(mot['d']))
        MTPVid = (MTPVlambda - mot['flux']) / (mot['ld']*mot['unit'])
        MTPViq = np.sqrt((mot['vol'] / webwe) ** 2 - MTPVlambda ** 2) / (mot['lq']*mot['unit'])
        MTPVTem = 3 * mot['pole']/4 * (mot['flux'] - mot['d']*MTPVid) * MTPViq
      
        # #%Basic Max speed parameters
        self.MaxSpdrpm = MaxSpdwe * 60 / ( (mot['pole']/2) * 2 * np.pi)
        ref = self.MaxSpdrpm - (self.MaxSpdrpm % 10000)
        ind = np.where(self.rpm==ref)[0]
        self.rpm[nrpm-1] = 65000
        MSId = mv['id'][ind]
        MSIq = mv['iq'][ind]
        MaxSpdTem = 3/4 * mot['pole'] * (mot['flux']*MSIq - mot['d']*MSId*MSIq)
       
        self.status = np.zeros(nrpm)
        self.status[:] = 3
        self.status[(self.rpm < MTPVrpm) & (self.rpm < self.MaxSpdrpm)] = 2
        self.status[self.MTPArpm>=self.rpm] = 1

        self.absearch = np.zeros(nrpm)
        self.absearch[(MTPVrpm >= self.rpm) & (MTPVrpm < (self.rpm + 100))] = 2  # ωeb
        self.absearch[(self.MTPArpm >= self.rpm) & (self.MTPArpm < (self.rpm + 100))] =1
        self.absearch[(self.MaxSpdrpm >= self.rpm) & (self.MaxSpdrpm < (self.rpm + 100))] = 3

        #%Refine the previously calculated ConstantTorque,Maxpower and MTPV variables based on status and absearch
        ct,mp,mv= evsimclass.flagset(ct,mp,mv,nrpm,self.status,self.absearch)

        # %Voltage limit and torque curve calculations
        # %Both are calculated using a single function (lutpoints) for different sets
        # %and percentages of variable values in constTrq, maxpower and MTPV
        tcId = np.arange(10, 671, 10) * (-1)
        evw = 2 * np.pi * ((np.arange(1, 62)) / 60)
        trqTem = [0] * 13

        self.vLimId = []
        self.vLimIq= []
        self.vLimTn = []
        self.vLim_iq = []
        self.vLim_I= []
    
        self.MaxPwrId= []
        self.MaxPwrIq= []  
        self.MaxPwrTn= []
        self.Maxpwr_iq= []
        self.MaxPwr_I= []
    
        self.MTPVId= []
        self.MTPVIq= []  
        self.MTPVTn= []  
        self.MTPV_iq= []  
        self.MTPV_I= []
        
        self.PfId=[]
        self.PfIq=[]
        temprpm = [self.MTPArpm, MTPVrpm, self.MaxSpdrpm]
        self.trqTem = [0] * 13  
        self.trqTem[0:3] = [MTPATem, MTPVTem, MaxSpdTem]
        self.mrpm=[0]*3
        self.mrpm[:3] = temprpm
        Tidx = 3
        vLimTe =self.trqTem[:3]
       
        for idx in range(3):
            lutwe = temprpm[idx] * (mot['pole'] / 2) * 2 * np.pi / 60
            self.vLimId.append([evsimclass.lutpoints(lutwe, mot, vLimTe[idx], evw, tcId)[0]])#REPLACE MOT
            self.vLimIq.append([evsimclass.lutpoints(lutwe, mot, vLimTe[idx], evw, tcId)[1]])#REPLACE MOT
            self.vLimTn.append([evsimclass.lutpoints(lutwe, mot, vLimTe[idx], evw, tcId)[2]])#REPLACE MOT
            self.vLim_iq.append([evsimclass.lutpoints(lutwe,mot, vLimTe[idx], evw, tcId)[3]])#REPLACE MOT
            self.vLim_I.append([evsimclass.lutpoints(lutwe, mot, vLimTe[idx], evw, tcId)[4]])#REPLACE MOT
      
        pctg = [5, 40, 60, 80, 100]
        for idx in range(0,5):
            temprpm = (pctg[idx]/100) * ( MTPVrpm - self.MTPArpm ) +self. MTPArpm
            
            lutwe = temprpm * (mot['pole']/2) * 2 * np.pi / 60
            if (temprpm < self.MTPArpm):
                MaxPwrTem = self.trqTem(Tidx-3)
            elif ((temprpm >self. MTPArpm) and (temprpm < MTPVrpm)):
                in_ = np.where(self.rpm <= temprpm)[0][-1]
                MaxPwrTem = mp['Tem'][in_]
            else:
                in_ = np.where(self.rpm <= temprpm)[0][-1]
                MaxPwrTem = mv['Tem'][in_]
            Tidx = Tidx+1
            self.trqTem.append(MaxPwrTem)
            self.mrpm.append(temprpm)
            self.MaxPwrId.append([evsimclass.lutpoints(lutwe,mot, MaxPwrTem, evw, tcId)[0]])
            self.MaxPwrIq.append([evsimclass.lutpoints(lutwe, mot, MaxPwrTem, evw, tcId)[1]])
            self.MaxPwrTn.append([evsimclass.lutpoints(lutwe, mot, MaxPwrTem, evw, tcId)[2]])
            self.Maxpwr_iq.append([evsimclass.lutpoints(lutwe,mot, MaxPwrTem, evw, tcId)[3]])
            self.MaxPwr_I.append([evsimclass.lutpoints(lutwe, mot, MaxPwrTem, evw, tcId)[4]])
        
        pctg = [10, 25, 50, 70, 100]
        in_ =0
        for idx in range(0,5):
            temprpm = (pctg[idx] / 100) * (self.MaxSpdrpm - MTPVrpm) + MTPVrpm
            lutwe = temprpm * (mot['pole'] / 2) * 2 * np.pi / 60
            if temprpm <self.MTPArpm:
                MTPV_Tem = trqTem[Tidx - 3]
            elif self.MTPArpm < temprpm < MTPVrpm:
                in_ = np.where(self.rpm <= temprpm)[0][-1]
                MTPV_Tem = mp['Tem'][in_]
            elif idx == 4 :
                ref = temprpm - (temprpm % 10000)
                in_ = np.where(self.rpm == ref)[0][-1]
                MTPV_Tem = mv['Tem'][in_]
            else:
                in_ = np.where(self.rpm <= temprpm)[0][-1]
                MTPV_Tem = mv['Tem'][in_]
        
            Tidx = Tidx + 1
            self.trqTem.append(MTPV_Tem)
            self.mrpm.append(temprpm)
            
            self.MTPVId.append([evsimclass.lutpoints(lutwe,mot , MTPV_Tem, evw, tcId)[0]])
            self.MTPVIq.append([evsimclass.lutpoints(lutwe,mot, MTPV_Tem, evw, tcId)[1]])
            self.MTPVTn.append([evsimclass.lutpoints(lutwe, mot, MTPV_Tem, evw, tcId)[2]])
            self.MTPV_iq.append([evsimclass.lutpoints(lutwe,mot, MTPV_Tem, evw, tcId)[3]])
            self.MTPV_I.append([evsimclass.lutpoints(lutwe,mot, MTPV_Tem, evw, tcId)[4]])
       

        #Unit Power Factor (PF) calculation
        upa = mot['If']/2
        upb = mot['If'] / (2 * np.sqrt(mot['e']))
        p = upa
        q = 0

        self.PfId[0:62] = [0]*61
        self.PfIq[0:62] = [0]*61

        for idx in range(0,61):
            self.PfId[idx] = upa*np.cos(evw[idx])-p
            self.PfIq[idx] = upb*np.sin(evw[idx])-q
        return ct,mp,mv
    @staticmethod
    def constTrq(mot, statw, statwe):
        ct = {}
        throttle = np.zeros(100)
        AI = np.zeros(100)
        ct['Aid'] = np.zeros(100)
        ct['Aiq'] = np.zeros(100)
        Abeta = np.zeros(100)
        ATe = np.zeros(100)
    

        for idx in range(1,101):
            throttle[idx-1] = idx / 100
            AI[idx-1] = mot['cur'] * throttle[idx-1]
            ct['Aid'][idx-1] = (mot['flux'] - np.sqrt(mot['flux']**2 + 8 * AI[idx-1]**2 * mot['d']**2)) / (4 * mot['d'])
            ct['Aiq'][idx-1] = np.sqrt(AI[idx-1]**2 - ct['Aid'][idx-1]**2)
            Abeta[idx-1] = math.degrees(math.atan(-ct['Aid'][idx-1] / ct['Aiq'][idx-1]))
            ATe[idx-1] = (3/4) * mot['pole'] * (mot['flux'] * AI[idx-1] / math.sqrt(2) * math.cos(math.radians(Abeta[idx-1])) + mot['d']*(AI[idx-1]/math.sqrt(2))**2 * math.sin(math.radians(2*Abeta[idx-1]))/2)
        
        MaxATe = max(ATe)
    
        ct['Im'] =np.zeros(90)
        ct['id'] = np.zeros(90)
        ct['iq'] = np.zeros(90)
        ct['Te'] = np.zeros(90)
        ct['beta'] = np.zeros(90)
        ct['Tem'] = np.zeros(90)
        ct['Pe'] = np.zeros(90)
        ct['Vd'] = np.zeros(90)
        ct['Vq'] = np.zeros(90)
        ct['Vm'] = np.zeros(90)
        ct['delta'] = np.zeros(90)
        ct['Pf'] = np.zeros(90)
        ct['Im'] = np.zeros(90)

        for idx in range(90):
            ct['Im'][idx] = mot['cur']
            ct['id'][idx] = (mot['flux'] - np.sqrt(mot['flux']**2 + 8 * (ct['Im'][idx]**2) * (mot['d'])**2)) / (4 * mot['d'])  
            ct['iq'][idx] = np.sqrt(ct['Im'][idx]**2 - ct['id'][idx]**2)

            if ((3/4) * mot['pole'] * (mot['flux'] * ct['iq'][idx] - mot['d'] * ct['id'][idx] * ct['iq'][idx])) > MaxATe:
                ct['Te'][idx] = MaxATe
            else:
                ct['Te'][idx] = (3/4) * mot['pole'] * (mot['flux'] * ct['iq'][idx] - mot['d'] * ct['id'][idx] * ct['iq'][idx])

            ct['beta'][idx] = math.degrees(math.atan(-ct['id'][idx] / ct['iq'][idx]))
            ct['Tem'][idx] = (3/4) * mot['pole'] * (mot['flux'] - (mot['d'] * ct['id'][idx])) * ct['iq'][idx]
            ct['Pe'][idx] = (ct['Te'][idx] * statw[idx]) / 1000
            ct['Vd'][idx] =  mot['res'] * ct['id'][idx] - statwe[idx] *  mot['lq'] *  mot['unit'] * ct['iq'][idx]
            ct['Vq'][idx] = statwe[idx] * ( mot['ld'] *  mot['unit'] * ct['id'][idx] + mot['flux']) +  mot['res'] * ct['iq'][idx]
            ct['Vm'][idx] = np.sqrt(ct['Vd'][idx]**2 + ct['Vq'][idx]**2)
            ct['delta'][idx] = math.degrees(math.atan(-ct['Vd'][idx] / ct['Vq'][idx]))
            ct['Pf'][idx] = math.cos(math.radians(ct['delta'][idx] - ct['beta'][idx]))
        return ct
    
    @staticmethod
    def maxPower(mot, statw, statwe):
        mp = {}
        mp['id'] = []
        mp['iq'] = []
        mp['Im'] = []
        mp['Tem'] = []
        mp['beta'] = []
        mp['Te'] = []
        mp['Pe'] = []
        mp['Vd'] = []
        mp['Vq'] = []
        mp['Vm'] = []
        mp['delta'] = []
        mp['Pf'] = []

        for idx in range(0, 649):
            lutIf = mot['flux'] / (mot['ld'] * mot['unit'])
            mp['id'].extend([(lutIf - cmath.sqrt(lutIf ** 2 - (1 - mot['e'] ** 2) * (
                        lutIf ** 2 + mot['e'] ** 2 * mot['cur'] ** 2 - mot['vol'] ** 2 / ((mot['ld'] * mot['unit']) ** 2 * statwe[idx] ** 2)))) / (
                                        mot['e'] ** 2 - 1)])
            mp['iq'].extend([cmath.sqrt(mot['cur'] ** 2 - (mp['id'][idx])**2)])
            mp['Im'].extend([np.sqrt(mp['id'][idx] ** 2 + (mp['iq'][idx])**2)])
            mp['Tem'].append(3 / 4 * mot['pole'] * (mot['flux'] - (mot['lq'] - mot['ld']) * mot['unit'] * mp['id'][idx]) * mp['iq'][idx])
            angle_rad = cmath.atan(-mp['id'][idx] / mp['iq'][idx])
            angle_deg = angle_rad * (180 / math.pi)

            mp['beta'].extend([angle_deg])
            radians = mp['beta'][idx] * (math.pi / 180)
            radians1 = (2 * mp['beta'][idx]) * (math.pi / 180)
            mp['Te'].append(3/4*mot['pole']*(mot['flux']*mp['Im'][idx]/np.sqrt(2)*np.cos(radians)+(mot['lq']-mot['ld'])*mot['unit']*(mp['Im'][idx]/np.sqrt(2)) ** 2 * np.sin(radians1) / 2))                                                                                                                  #[idx]np.sqrt(2)) ** 2 * np.sin(radians1) / 2))                                
            mp['Pe'].extend([mp['Te'][idx] * statw[idx] / 1000])
        
            mp['Vd'].append(mot['res'] * mp['id'][idx] - statwe[idx] * mot['lq'] * mot['unit'] * mp['iq'][idx ])
            mp['Vq'].append(statwe[idx] * (mot['ld'] * mot['unit'] * mp['id'][idx] + mot['flux']) + mot['res'] * mp['iq'][idx])
            mp['Vm'].extend([np.sqrt(mp['Vd'][idx] ** 2 + mp['Vq'][idx] ** 2)])
            angle_rad1 = cmath.atan(-mp['Vd'][idx] / mp['Vq'][idx])
            angle_deg1 = angle_rad1 * (180 / math.pi)
            mp['delta'].append(angle_deg1)
            radians3 = (mp['delta'][idx] - mp['beta'][idx]) * (np.pi / 180)
            mp['Pf'].append(np.cos(radians3))
        return mp
    
    @staticmethod
    def mtpv(mot, statw, statwe,nrpm):
        mv = {}

        mv["id"] = np.zeros(nrpm)
        mv["iq"] = np.zeros(nrpm)
        mv["Im"] = np.zeros(nrpm)
        mv["beta"] = np.zeros(nrpm)
        mv["Vd"] = np.zeros(nrpm)
        mv["Vq"] = np.zeros(nrpm)
        mv["Vm"] = np.zeros(nrpm)
        mv["delta"] = np.zeros(nrpm)
        mv["Tem"] = np.zeros(nrpm)
        mv["Te"] = np.zeros(nrpm)
        mv["Pe"] = np.zeros(nrpm)
        mv["Pf"] = np.zeros(nrpm)

        for idx in range(nrpm):
            _lambda = (-mot['lq'] * mot['unit']*mot['flux'] + np.sqrt((mot['lq'] * mot['unit'])**2 * mot['flux']**2 + 8 * (mot['d']**2) * (mot['vol']/statwe[idx])**2)) / (4 * (-mot['d']))
            mv["id"][idx] = (_lambda - mot['flux']) / (mot['ld'] * mot['unit'])
            mv["iq"][idx] = np.sqrt((mot['vol']/statwe[idx])**2 - _lambda**2) / (mot['lq'] * mot['unit'])
            mv["Im"][idx] = np.sqrt(mv["id"][idx]**2 + mv["iq"][idx]**2)
            mv["beta"][idx] = np.rad2deg(np.arctan(-mv["id"][idx] / mv["iq"][idx]))
            mv['Vd'][idx] = mot['res'] * mv['id'][idx] - statwe[idx] * mot['lq'] * mot['unit'] * mv['iq'][idx]
        
            mv['Vq'][idx ] = statwe[idx] * (mot['ld'] * mot['unit'] * mv['id'][idx ] + mot['flux']) + mot['res'] * mv['iq'][idx ]
            mv["Vm"][idx] = np.sqrt(mv["Vd"][idx]**2 + mv["Vq"][idx]**2)
        
            mv['delta'][idx] = np.rad2deg(np.arctan(-mv['Vd'][idx] / mv['Vq'][idx]))
        
        
            mv["Tem"][idx] = (3/4) * mot['pole'] * (mot['flux'] * mv["iq"][idx] - mot['d']* mv["id"][idx] * mv["iq"][idx])
            mv["Te"][idx] = 3/4 * mot['pole'] * (mot['flux'] * mv["Im"][idx] / np.sqrt(2) * np.cos(np.deg2rad(mv["beta"][idx])) + mot['d'] * (mv["Im"][idx] / np.sqrt(2))**2 * np.sin(np.deg2rad(2 * mv["beta"][idx])) / 2)
            mv["Pe"][idx] = mv["Te"][idx] * statw[idx] / 1000
            mv["Pf"][idx] = np.cos(np.deg2rad(mv["delta"][idx] - mv["beta"][idx]))

        return mv
    
    @staticmethod
    def flagset(ct, mp, mv, nrpm, status, absearch):
        ct['Pfflag'] = np.full(nrpm, np.nan)
        ct['Pfflag'] =np.full(nrpm, np.nan)
        ct['delflag'] = np.full(nrpm, np.nan)
        ct['betaflag'] =np.full(nrpm, np.nan)
        ct['Imflag'] =np.full(nrpm, np.nan)
        ct['Vmflag'] = np.full(nrpm, np.nan)
        ct['Teflag'] = np.full(nrpm, np.nan)
        ct['Peflag'] = np.full(nrpm, np.nan)
    
        mp['Pfflag'] =np.full(nrpm, np.nan)
        mp['delflag'] =np.full(nrpm, np.nan)
        mp['betaflag'] =np.full(nrpm, np.nan)
        mp['Imflag'] =np.full(nrpm, np.nan)
        mp['Vmflag'] =np.full(nrpm, np.nan)
        mp['Teflag'] =np.full(nrpm, np.nan)
        mp['Peflag'] =np.full(nrpm, np.nan)
        mp['idflag'] =np.full(nrpm, np.nan)
        mp['iqflag'] =np.full(nrpm, np.nan)
    
        mv['Pfflag'] =np.full(nrpm, np.nan)
        mv['delflag'] =np.full(nrpm, np.nan)
        mv['betaflag'] =np.full(nrpm, np.nan)
        mv['Imflag'] =np.full(nrpm, np.nan)
        mv['Vmflag'] =np.full(nrpm, np.nan)
        mv['Teflag'] =np.full(nrpm, np.nan)
        mv['Peflag'] =np.full(nrpm, np.nan)
        mv['idflag'] =np.full(nrpm, np.nan)
        mv['iqflag'] =np.full(nrpm, np.nan)
        sts11 = ((status[0:90] == 1) | (absearch[0:90] == 1)).astype(int)
        for idx in range(len(sts11)):
            if sts11[idx] == 1:
                ct['Pfflag'][idx] = ct['Pf'][idx]
                ct['delflag'][idx] = ct['delta'][idx]
                ct['betaflag'][idx] = ct['beta'][idx]
                ct['Imflag'][idx] = ct['Im'][idx]
                ct['Vmflag'][idx] = ct['Vm'][idx]
                ct['Teflag'][idx] = ct['Te'][idx]
                ct['Peflag'][idx] = ct['Pe'][idx]
                
        sts21 = np.array(((status == 2) | (absearch == 1)).astype(int))
        for idx in range(len(sts21)):
            if sts21[idx] == 1:
                mp['Pfflag'][idx] = np.real(mp['Pf'][idx])
                mp['delflag'][idx] = np.real(mp['delta'][idx])
                mp['betaflag'][idx] =np.real( mp['beta'][idx])
                mp['Vmflag'][idx] = np.real(mp['Vm'][idx])
                mp['Teflag'][idx] =np.real( mp['Te'][idx])
                mp['Peflag'][idx] = np.real(mp['Pe'][idx])
                mp['idflag'][idx] = np.real(mp['id'][idx])
                mp['iqflag'][idx] = np.real(mp['iq'][idx])
                mp['Imflag'][idx]= np.sqrt(mp['idflag'][idx]**2 + mp['iqflag'][idx]**2)
    
        sts32 = np.array(((status == 3) | (absearch == 2)).astype(int))
        for idx in range(len(sts32)):
            if sts32[idx] == 1:
                mv['Pfflag'][idx] = np.real(mv['Pf'][idx])
                mv['delflag'][idx] = np.real(mv['delta'][idx])
                mv['betaflag'][idx] =np.real( mv['beta'][idx])
                mv['Vmflag'][idx] = np.real(mv['Vm'][idx])
                mv['Teflag'][idx] = np.real(mv['Te'][idx])
                mv['Peflag'][idx] = np.real(mv['Pe'][idx])
                mv['idflag'][idx] =np.real(mv['id'][idx])
                mv['iqflag'][idx] =np.real( mv['iq'][idx])
                mv['Imflag'][idx]= np.sqrt(mv['idflag'][idx]**2 + mv['iqflag'][idx]**2)
        return ct,mp,mv    
        
    @staticmethod
    def lutpoints(we, mot, Tem, w, curI):
        a =  mot['vol'] / (we * mot['ld']*mot['unit'])
        lutb = mot['vol'] / (we *  mot['lq']*mot['unit'])
        p =  mot['flux'] /  (mot['ld']*mot['unit'])
        q = 0

        Id = np.zeros(61)
        Iq = np.zeros(61)
        Tn = np.zeros(61)

        for idx in range(61):
            Id[idx] = a * np.cos(w[idx]) - p
            Iq[idx] = lutb * np.sin(w[idx]) - q
            Tn[idx] = 3 *  mot['pole'] / 4 * ( mot['flux'] + ( mot['ld'] -  mot['lq'])*mot['unit'] * Id[idx]) * Iq[idx]

        # Torque curve calculations
        iq = np.zeros(len(curI))
        I = np.zeros(len(curI))

        for idx in range(len(curI)):
            iq[idx] = 4 * np.real(Tem) / (3 *  mot['pole'] * ( mot['flux'] - ( mot['lq'] -  mot['ld'])*mot['unit'] * curI[idx]))
            I[idx] = np.sqrt(curI[idx]**2 + iq[idx]**2)

        return Id, Iq, Tn, iq, I
# ev=evsimclass()
# ev.init("8",10000)
