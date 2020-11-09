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
    
