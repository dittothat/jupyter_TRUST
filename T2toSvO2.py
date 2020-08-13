#!/usr/bin/env python
# coding: utf-8

# Function to convert from T2 to SO2
# input: T2 (s), Hct (fraction), tCPMG (ms), models (adult, neonate_bush, neonate_liu, SCD)
# output: SvO2 (note this is 1-OEF)
# can vectorize this as T2toYv_vec = np.vectorize(T2toYv) 

from scipy.optimize import fsolve

def T2toSvO2(T2, Hct, tCPMG = 10, model = 'adult' ):
    
    model_dict = {'adult':1, 'neonate_bush':2, 'neonate_liu':3, 'SCD':4}
    global f
    
    if model_dict[model] == 1: # adult
        # Parameters from Lu et al., Table 1
        if tCPMG == 10:
            a1 = -13.5
            a2 = 80.2
            a3 = -75.9
            b1 = -.5
            b2 = 3.4
            c1 = 247.4
        elif tCPMG==15:
            a1 = -12
            a2 = 77.7
            a3 = -75.5;
            b1 = -6.6
            b2 = 31.4
            c1 = 249.4;
        elif tCPMG==20:
            a1 = 7
            a2 = -9.2
            a3 = 23.2
            b1 = -4.5
            b2 = 5.3
            c1 = 310.8
        else:
            raise Exception("tCPMG invalid")
        
        A = a1 + a2*Hct + a3*Hct**2
        B = b1*Hct + b2*Hct**2
        C = c1*Hct*(1-Hct)
        def f(OEF):
            return A + B*OEF + C*OEF**2 - 1/T2
            
    elif model_dict[model] == 2: # neonate_bush
        # Paramters from Bush et al., 2016, MRM
        assert tCPMG == 10, 'tCPMG must be 10 ms for neonate_bush model'
        
        A1 = 77.5
        A2 = 27.8
        A3 = 6.95
        A4 = 2.34
        
        def f(OEF):
            return A1*Hct*OEF**2 + A2*OEF**2 + A3*Hct + A4 - 1/T2
            
    elif model_dict[model] == 3: # neonate_liu
        #Parameters from Liu et al., 2015, MRM, CORRECTED
        assert tCPMG == 10, 'tCPMG must be 10 ms for neonate_liu model'
        
        a1 = -1.1
        a2 = 24
        a3 = -21.4
        b1 = -5.1
        b2 = 29.4
        c1 = 242.9
        
        A = a1 + a2*Hct + a3*Hct**2
        B = b1*Hct + b2*Hct**2
        C = c1*Hct*(1-Hct)
        def f(OEF):
            return A + B*OEF + C*OEF**2 - 1/T2
        
    elif model_dict[model] == 4: #SCD
        # Parameters from Bush, et al., 2018, MRM
        assert Hct > 0.2 and Hct < 0.4, 'Hct out of bounds for SCD model'
        if tCPMG == 10:
            A = 70.0
            B = 5.75
        elif tCPMG == 20:
            A = 93.1
            B = 7.16
        else:
            raise Exception("tCPMG invalid")
        
        def f(OEF):
            return B + A*OEF**2 - 1/T2

    OEF = fsolve(f, 0.5)
    SvO2 = 1 - OEF
    
    return SvO2
