# TODO: Refactor class values to store library of congress values in a dictionary
class CallNumber:
    def __init__(self, call_number_dict, sec_callnum_dict, description_dict, details_dict):
        self.callnum_dict = call_number_dict
        self.callnum_letter = call_number_dict["classification_letter"]
        self.callnum_number = call_number_dict["classification_number"]
        self.callnum_cutlet = call_number_dict["cutter_letter"]
        self.callnum_cutnum = call_number_dict["cutter_num"]
        self.sec_callnum_dict = sec_callnum_dict
        self.desc_dict = description_dict
        self.details = details_dict
        # Testing Second Part of the Call Number
        self.callnum_seccutter = False
        self.callnum_index = False
        self.callnum_supp = False
        self.callnum_year = None
        # Testing the Values in the Description
        # Volume Details
        self.has_volume = False
        self.vol_part = False
        self.vol_index = False
        self.vol_supp = False
        # Part Details
        self.has_part = False
        self.part_hasvol = False
        self.part_supp = False
        # Number Details
        self.has_number = False
        self.number_part = False
        self.number_volume = False
        self.number_index = False
        self.number_supp = False
        # Series Details
        self.has_series = False
        self.series_vol = False
        self.ser_index = False
        self.ser_supp = False
        # Index Details
        self.desc_index = False
        # Supplement Details
        self.desc_supp = False
        # Copy Number
        self.copy_num = None


        for key, value in sec_callnum_dict.items():
            if key == 'second cutletter':
                self.callnum_seccutter = True
            if key == 'Call Index':
                self.callnum_index = True
            elif key == 'supplement':
                self.callnum_supp = True
            elif key == 'Publication Year':
                self.callnum_year = sec_callnum_dict['Publication Year']
        for key, value in description_dict.items():
            if key == 'Volume Number':
                self.has_volume = True
            elif key == 'Volume Part':
                self.vol_part = True
            elif key == 'Part Number':
                self.has_part = True
            elif key == 'Part Volume':
                self.part_hasvol = True
            elif key == 'Number':
                self.has_number = True
            elif key == 'Number Part':
                self.number_part = True
            elif key == 'Number Volume':
                self.number_volume = True
            elif key == 'Number Index':
                self.number_index = True
            elif key == 'Number Supplement':
                self.number_supp = True
            elif key == 'Series':
                self.has_series = True
            elif key == 'Series Volume':
                self.series_vol = True
            elif key == 'Index Bool':
                self.desc_index = True
            elif key == 'Volume Index':
                self.vol_index = True
            elif key == 'Series Index':
                self.ser_index = True
            elif key == 'Supplement Bool':
                self.desc_supp = True
            elif key == 'Volume Supplement':
                self.vol_supp = True
            elif key == 'Part Supplement':
                self.part_supp = True
            elif key == 'Series Supplement':
                self.ser_supp = True
            elif key == 'Copy Number':
                self.copy_num = description_dict['Copy Number']

    # Getters for the dictionary values
    def getCallNumDict(self):
        return self.callnum_dict

    def getSecCallNumDict(self):
        return self.sec_callnum_dict

    def getDetails(self):
        return self.details

    def getDescriptionDict(self):
        return self.desc_dict

    # Getters for CallNumberValues
    def getCallNumLetter(self):
        return self.callnum_letter

    def getCallNumNumber(self):
        return self.callnum_number

    def getCallNumCutLet(self):
        return self.callnum_cutlet

    def getCallNumCutNum(self):
        return self.callnum_cutnum

    # Testing Second Part of the Call Number
    def testCallNumSecCutter(self):
        return self.callnum_seccutter

    def testCallNumIndex(self):
        return self.callnum_index

    def testCallNumSupp(self):
        return self.callnum_supp

    def testCallNumYear(self):
        return self.callnum_year

    # Testing the Values in the Description
    # Getter of Volume Details
    def testVolVolume(self):
        return self.has_volume

    def testVolPart(self):
        return self.vol_part

    def testVolIndex(self):
        return self.vol_index

    def testVolSupp(self):
        return self.vol_supp

    # Part Details
    def testPrtPart(self):
        return self.has_part

    def testPrtVol(self):
        return self.part_hasvol

    def testPrtSupp(self):
        return self.part_supp

    # Number Details
    def testNumNumber(self):
        return self.has_number

    def testNumPart(self):
        return self.number_part

    def testNumVol(self):
        return self.number_volume

    def testNumIndex(self):
        return self.number_index

    def testNumSupp(self):
        return self.number_supp

    # Series Details
    def testSerSeries(self):
        return self.has_series

    def testSerVol(self):
        return self.series_vol

    def testSerIndex(self):
        return self.ser_index

    def testSerSupp(self):
        return self.ser_supp

    # Index Details
    def testDescIndex(self):
        return self.desc_index
    # Supplement Details
    def testDescSupp(self):
        return self.desc_supp
    # Copy Number
    def testCopyNum(self):
        return self.copy_num
