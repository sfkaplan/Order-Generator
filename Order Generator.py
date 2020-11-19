import numpy as np
import pandas as pd

class Instruments:
    
# In this class, we define the species and do a random pick of the instrument that is being traded.

    species = []
    Species1 = "1BOC90"
    Species2 = "1BPLD"
    Species3 = "1BPLE"
    Species4 = "1BP21D"
    Species5 = "1BP28D"
    Species6 = "1BRN20"
    Species7 = "1BUS20"
    Species8 = "1CH24D"
    mat = [Species1, Species2, Species3, Species4, Species5, Species6, Species7, Species8]
    
    def random_pick(self): 
        aux = int(np.random.uniform(0,7,1))
        self.species.append(self.mat[aux])
        return self.species

class Order:
    Amount = 0
    Price = 0
    ID = ""
    Side = 0
    Type = 0
    Duration = 0
    
# For Side: 0 = Buy Order, 1 = Sell Order
# For Type: 0 = Market Order, 1 = Limit Order, 2 = Cancel Order, 3 = Fill or Kill
# For Duration: 0 = GTC, 1 = FOK, 2 = IOC, 3 = GFD

    def __init__(self, amount, price, id, side, type, duration):
        self.Amount = amount
        self.Price = price
        self.ID = id
        self.Side = side
        self.Type = type
        self.Duration = duration

    def printOrder(self):
        print("Price:"  + str(self.Price) + " Amount: " + str(self.Amount) + " ID: " + str(self.ID) + " Side: " + str(self.Side) + " Type: " + str(self.Type) + " Duration: " + str(self.Duration) )
        

    BuyOrders = []
    SellOrders = []

    def BuyOrder(self, newOrder):
        index = 0
        if newOrder.Type == 0:
            self.BuyOrders.insert(index, newOrder)
        else:
            for o in self.BuyOrders:
                if o.Price > newOrder.Price:
                    break
                index += 1
            self.BuyOrders.insert(index, newOrder)

    def SellOrder(self, newOrder):
        if newOrder.Type == 0:
            index = len(newOrder)
            self.SellOrders.insert(index, newOrder)
        else:
            index = 0
            for o in self.SellOrders:
                if o.Price < newOrder.Price:
                    break
                index += 1
            self.SellOrders.insert(index, newOrder)
            
class Generator:
    
    BuyOrders = []
    SellOrders = []

    def generator(self, i):
        for j in range(i):
            Amount = int(np.random.uniform(1,101,1))
            Price = round(float(np.random.uniform(25,25.5,1)),2)
            if j < 10:
                ID = "00" + str(j)
            elif j < 100:
                ID = "0" + str(j)
            else:
                ID = str(j)
            Side = int(np.rint(np.random.uniform(0,1,1)))
            Type = 1
            Duration = 0
            if Side == 0:
                self.BuyOrders.append(Order(Amount, Price, ID, Side, Type, Duration))
            else:
                self.SellOrders.append(Order(Amount, Price, ID, Side, Type, Duration))
        
generate = Generator()
generate.generator(50)

print("BuyOrders:" + str(len(generate.BuyOrders)))
for o in generate.BuyOrders:
    o.printOrder()

print("####################")

print("SellOrders:" + str(len(generate.SellOrders)))
for o in generate.SellOrders:
    o.printOrder()
    
fg = generate.BuyOrders[0:9]
len(fg)

class dbistorage:
    import sys         # Provides Information About Python Interpreter Constants And Functions
    import ibm_db      # Contains The APIs Needed To Work With Db2 Databases
    import ibm_db_dbi
    conn = ibm_db.connect("DATABASE=testdb;HOSTNAME=localhost;PORT=50000;PROTOCOL=TCPIP;UID=db2inst1;PWD=arquant;", "", "")
    connection = ibm_db_dbi.Connection(conn)
    tab = "CREATE TABLE Ordering6 (Price float, Amount int, ID VARCHAR(60), Side int, Type int)"
    #return1 = ibm_db.exec_immediate(conn, tab)
    def dbistore(self, order):
        params = ()
        insert = "insert into ordering6 values(?,?,?,?,?)"
        stmt_insert = self.ibm_db.prepare(self.conn, insert)
        for i in range(len(order)):
            if i == 0:
                aux1 = [(order[i].Price, order[i].Amount, order[i].ID, order[i].Side, order[i].Type)]
            else:
                aux2 = (order[i].Price, order[i].Amount, order[i].ID, order[i].Side, order[i].Type)
                aux1.append(aux2)
            #print(aux1)
            #params=(params, (order[i].Price, order[i].Amount, order[i].ID, order[i].Side, order[i].Type))
        params = tuple(aux1)
        #print(params)
        self.ibm_db.execute_many(stmt_insert,params)
        select="select price, amount, id, side, type from ordering6"
        cur = self.connection.cursor()
        cur.execute(select)
        row=cur.fetchall()
        for j in range(len(order)):
            print("{} \t  ".format(row[j]),end="\n")
     
testing = dbistorage()
testing.dbistore(fg)

class Message:

    import xml.etree.ElementTree as ET
    import time, datetime
    import sys         # Provides Information About Python Interpreter Constants And Functions
    import ibm_db      # Contains The APIs Needed To Work With Db2 Databases
    import ibm_db_dbi
    conn2 = ibm_db.connect("DATABASE=testdb;HOSTNAME=localhost;PORT=50000;PROTOCOL=TCPIP;UID=db2inst1;PWD=arquant;", "", "")
    connection2 = ibm_db_dbi.Connection(conn2)
    tab2 = "CREATE TABLE Message3 (ID VARCHAR(60), Message XML)"
    #return2 = ibm_db.exec_immediate(conn2, tab2)

    def Orders(self, order):
        import xml.etree.ElementTree as ET
        import xml.dom.minidom
        from lxml import etree
        import time, datetime
        checksum = []
        ExecutionReportMessage = ET.Element('NewOrderSingle')
        BeginString = ET.SubElement(ExecutionReportMessage, 'BeginString')
        BeginString.text = 'FIX Latest'
        BodyLength = ET.SubElement(ExecutionReportMessage, 'BodyLength')
        BodyLength.text = " "
        MsgType = ET.SubElement(ExecutionReportMessage, 'MsgType')
        MsgType.text = 'D'
        MsgSeqNum = ET.SubElement(ExecutionReportMessage, 'MsgSeqNum')
        MsgSeqNum.text = ' '
        SenderCompID = ET.SubElement(ExecutionReportMessage, 'SenderCompID')
        SenderCompID.text = 'SERVER'
        SendingTime = ET.SubElement(ExecutionReportMessage, 'SendingTime')
        current_time = datetime.datetime.utcnow()
        SendingTime.text = str(current_time)
        TargetCompID = ET.SubElement(ExecutionReportMessage, 'TargetCompID')
        TargetCompID.text = 'CLIENT'
        OrderID = ET.SubElement(ExecutionReportMessage, 'OrderID')
        OrderID.text = str(order.ID)
        Instrument = ET.SubElement(ExecutionReportMessage, 'Instrument' )
        Instrument.text = "1BOC90"
        if order.Side == 0:
            Side = ET.SubElement(ExecutionReportMessage, 'Side' )
            Side.text = 'Buy'
            checksum.append('Buy')
        else:
            Side = ET.SubElement(ExecutionReportMessage, 'Side' )
            Side.text = 'Sell'
            checksum.append('Sell')
        TransactTime = ET.SubElement(ExecutionReportMessage, 'TransactTime')
        current_time2 = datetime.datetime.utcnow()
        TransactTime.text = str(current_time2)
        OrderQtyData = ET.SubElement(ExecutionReportMessage, 'OrderQtyData')
        OrderQtyData.text = str(order.Amount)
        checksum = ['FIX Latest', " ", "D", 'SERVER', 'CLIENT', ' ', str(current_time), str(order.ID), str(current_time2), str(order.Amount)]
        if order.Type == 0:
            OrdType = ET.SubElement(ExecutionReportMessage, 'OrdType')
            OrdType.text = 'Market'
            checksum.append('Market')
        elif order.Type == 1:
            OrdType = ET.SubElement(ExecutionReportMessage, 'OrdType')
            OrdType.text = 'Limit'
            checksum.append('Limit')
        else:
            OrdType = ET.SubElement(ExecutionReportMessage, 'OrdType')
            OrdType.text = 'Cancel'
            checksum.append('Cancel')
        #aux1 = bytearray(ET.tostring(ExecutionReportMessage))
        #aux2 = len(aux1)
        #aux3 = bytearray(checksum)
        aux4 = len(str(checksum))
        CheckSum = ET.SubElement(ExecutionReportMessage, 'CheckSum')
        CheckSum.text = str(aux4)
        mydata = ET.tostring(ExecutionReportMessage)
        
        tup = [(order.ID, mydata)]
        params2 = tuple(tup)
        insert2 = "insert into Message3 values(?,?)"
        stmt_insert2 = self.ibm_db.prepare(self.conn2, insert2)
        self.ibm_db.execute_many(stmt_insert2,params2)
        select2="select id, message from message3"
        cur2 = self.connection2.cursor()
        cur2.execute(select2)
        row2=cur2.fetchall()
        #print(len(row2))
        #for j in range(len(order)):
        #print("{} \t ".format(row2[22]),end="\n")
        #element = etree.element(row2[0][1])
        #print(etree.tostring(element, pretty_print=True))
        xml = xml.dom.minidom.parseString(row2[len(row2)-1][1])
        xml_pretty_str = xml.toprettyxml()
        print(xml_pretty_str)
        myfile = open("NewOrderSingle_" + str(order.ID) + ".xml", "wb")
        aux3 = ET.Element(row2[5])
        #mydata2 = ET.tostring(aux3)
        myfile.write(mydata)
        
message = Message()
message.Orders(generate.SellOrders[3])
