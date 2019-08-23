import numpy as np
# Class variables follow variable naming conventions established in "Analysis of Plant..."


class EquipmentUnit():

    def __init__(self, A=None, K=None, Fm=None, C=None, B=None, P=None):
        self.A = A if A is not None else 1
        self.K = K if K is not None else [1, 1, 1]
        self.Fm = Fm if Fm is not None else 1
        self.C = C if C is not None else [1, 1, 1]
        self.B = B if B is not None else [1, 1]
        self.P = P if P is not None else 1

    # Base Unit Cost
    def Cp0(self):
        K1 = self.K[0]
        K2 = self.K[1]
        K3 = self.K[2]
        # Equation from page ...
        Cp0 = 10**(K1+K2*np.log10(self.A)+K3*(np.log10(self.A))**2)
        return Cp0

    # Pressure Factor
    def Fp(self, P):
        C1 = self.C[0]
        C2 = self.C[1]
        C3 = self.C[2]
        # Equation from page ...
        Fp = 10**(C1+C2*np.log10(self.P)+C3*(np.log10(self.P))**2)
        return Fp

    # Bare Module Cost
    def CBM(self):
        B1 = self.B[0]
        B2 = self.B[1]
        # Equation from page ...
        CBM = self.Cp0()*(B1+B2*self.Fm*self.Fp())
        return CBM

    def CBM0(self):
        B1 = self.B[0]
        B2 = self.B[1]
        # Equation from page ...
        CBM0 = self.Cp0()*(B1+B2)
        return CBM0


class Material():
    def __init__(self, flowRate, cost):
        self.flowRate = flowRate
        self.cost = cost


class PlantDesign():

    def __init__(self, equipmentList=None, materialList=None, SF=None):
        self.equipmentList = equipmentList if equipmentList is not None else []
        self.materialList = materialList if materialList is not None else []
        self.SF = SF if SF is not None else 1

    def AddEquipment(self, unit):
        self.equipmentList.append(unit)

    def RemoveEquipment(self, unit):
        self.equipmentList.remove(unit)

    # Grass Roots Plant Cost
    def CGR(self):
        # Use combined CBM,CBM0 for every unit to be purchased
        CGR = 0
        for unit in self.equipmentList:
            # Equation from page ...
            CGR += 1.18*unit.CBM()+0.5*unit.CBM0()
        return CGR

    # Number of operators required per shift
    def NOL(self):
        # Depends on total number of equipment units(compressors,reactors,exchangers,etc)
        # Equation from page ...
        NOL = (6.29+0.23*len(self.equipmentList))**0.5
        return NOL

    # Cost of Labor
    def COL(self):
        TOTAL_SHIFTS = 1095  # per year assuming 3 per day 24/7
        OP_SHIPTS = 245  # shifts per operator per year
        OP_SALARY = 66910  # cost of employing op for year
        opsRequired = TOTAL_SHIFTS/OP_SHIPTS*self.NOL()

        # round up
        numOps = int(opsRequired)
        if opsRequired == numOps:
            numOps = numOps
        else:
            numOps = numOps+1

        COL = numOps*OP_SALARY

        return COL

    # Cost of Raw Materials
    def CRM(self):
        CRM = 0
        for mat in self.materialList:
            # Equation from page ...
            CRM += 365*24*self.SF*mat.flowRate*mat.cost
        return CRM

    # Cost of Manufacturing
    def COM(self):
        # with depreciation
        # Equation from page ...
        COM = 0.180*self.CGR()+2.73*self.COL()+1.23*(self.CRM())  # +self.CUT())
        return COM
