 #  Copyright (c) 2019. Lim Ji Xiong. All Rights Reserved.
#  Contact: limjix@gmail.com


# title           :IO.py
# description     :Interface Layer between Control Algorithm and PLC
# author          :Lim Ji Xiong
# date            :20180625
# version         :0.1
# notes           :
# python_version  : 3.6
# ==============================================================================

'''
# ==========THE BIG IDEA=================================================================
This Library Models the TBM

#========================================================================================
'''#Test

# -------------------- Import Libraries ----------------------------------------------
import snap7
import time
import json
# -------------------- Define Class --------------------------------------------------

class TBM():

    #=========================================================================
    #               Encapsulates all the info within TBM
    #=========================================================================

    def __init__(self):

        #Create PLC CLient
        result = False
        while result == False:
            result = self.create_client()
            if result == False:
                print("Can't connect to client")
                time.sleep(2)
            else:
                print("Connection Success")

        #==========================Define Addresses=======================
        with open('./SensorAddress.json', 'r') as f:
            sensorlist = json.load(f)

        sensorlist = [tuple(l) for l in sensorlist]
        self.SensorAddress = tuple(sensorlist)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    #--------------------- Connection Functions ---------------------------------------------
    def create_client(self):
        # Creates the connection between PLC and Computer

        self.plc = snap7.client.Client()
        PLC_IP = "192.168.0.22"
        try:
            self.plc.connect(PLC_IP, 0, 2)
            result = True
        except:
            print("PLC Connection Not Available")
            result = False

        return result

    #--------------------- Read Functions [High Level] --------------------------------

    #USE THIS!!! THIS IS USEFUL
    def readSpecificValue(self, varName):

        #================================================================
        #   Function to read specific addresses and ouput real number   #
        #================================================================
        [DBnumber,AddressBlock] = self.findDBAddress(varName)

        area = snap7.snap7types.S7AreaDB
        ByteSize = 4 #I am only working with READ

        #Read
        readData = self.plc.read_area(area, DBnumber, AddressBlock, ByteSize)

        #Convert from ByteArray to Real
        Data = snap7.util.get_real(readData, 0)
        return Data



    #--------------------- Write Functions [High Level]--------------------------------

    #USE THIS!! THIS IS USEFUL ---- TURN THIS OFF TO PREVENT WRITING
    def changeSpecificValue(self, varName, NewValue):

        #================================================================
        #       Function to enable data in PLC to be changed easily     #
        #================================================================
        [DBnumber, AddressBlock] = self.findDBAddress(varName)

        #Define
        area = snap7.snap7types.S7AreaDB
        ByteSize = 4 #I am only working with READ

        #Read
        readData = self.plc.read_area(area, DBnumber, AddressBlock, ByteSize)

        #Change
        snap7.util.set_real(readData, 0, NewValue)

        #Write
        self.plc.write_area(area, DBnumber, AddressBlock, readData)

        return


    #--------------------- Utility Functions [Low Level]-------------------------------------------
    def findDBAddress(self,varName):
        # ================================================================
        #    Input what sensor you want, out comes dbnumber and address  #
        # ================================================================
        for item in self.SensorAddress:
            if item[0] == varName:
                dbnumber = item[1]
                address = item[2]
                try:
                    byte = item[3]
                    return dbnumber, address , byte
                except:
                    return dbnumber, address

        return