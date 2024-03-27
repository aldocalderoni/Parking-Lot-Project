from enum import Enum
import datetime

class VehicleType(Enum):
    CAR = 1
    TRUCK = 2
    VAN = 3
    MOTORCYCLE = 4

class AccountStatus(Enum):
    ACTIVE = 1
    BLOCKED = 2

class PaymentStatus(Enum):
    UNPAID = 1
    COMPLETED = 2
    CANCELLED = 3
    REFUNDED = 4

class ParkingLot:
    def __init__(self, loc: str, admin: str, password: str):
        self.totalSpots = 200
        self.freeSpotsCars = 50
        self.freeSpotsTrucks = 50
        self.freeSpotsVans = 50
        self.freeSpotsMotorcycles = 50
        self.numEntrancePanels = 10
        self.numExitPanels = 10
        self.location = loc #Add location when initialized
        self.admin = Admin(self, admin, password)
        self.parkingAttendant = ParkingAttendant(self, "", "")

        self.entrancePanels = []
        self.exitPanels = []
        for i in range(1, 11):
            self.entrancePanels.append(EntrancePanel(i, self))
            self.exitPanels.append(ExitPanel(i, self))

        self.floors = []
        for i in range(1, 6):
            self.floors.append(ParkingFloor(i))

        self.numParkingDisplayBoards = len(self.floors)
        self.parkingDisplayBoards = []
        for i in range(self.numParkingDisplayBoards):
            self.parkingDisplayBoards.append(ParkingDisplayBoard(self))
        
        self.tickets = []
            
    def addEntrancePanel(self):
        self.numEntrancePanels += 1
        self.entrancePanels.append(EntrancePanel(self.numEntrancePanels))

    def addExitPanel(self):
        self.numExitPanels += 1
        self.exitPanels.append(ExitPanel(self.numExitPanels))
        

class ParkingTicket():
    ticketNumber = 0
    def __init__(self, parkingLot: ParkingLot, vehType: int, pet: bool, spot: str):
        ParkingTicket.ticketNumber += 1
        self.ticketNumber = ParkingTicket.ticketNumber
        self.vehicleType = VehicleType(vehType)
        self.spot = spot
        self.pet = pet
        self.issuedAtDate = datetime.datetime.now()
        self.paidAtDate = ""
        self.payAmount = 0
        self.payStatus = PaymentStatus(1).name
        self.additionalFee = False
        if(vehType == 1):
            parkingLot.freeSpotsCars -= 1
        if(vehType == 2):
            parkingLot.freeSpotsTrucks -= 1
        if(vehType == 3):
            parkingLot.freeSpotsVans -= 1
        if(vehType == 4):
            parkingLot.freeSpotsMotorcycles -= 1

class EntrancePanel():
    def __init__(self, ident, parkingLot: ParkingLot):
        self.id = ident
        self.pl = parkingLot

    def inputInfoForTicket(self, pl: ParkingLot):
        vehicleType = 0
        while vehicleType != 1 and vehicleType != 2 and vehicleType != 3 and vehicleType != 4:
            vehicleType = input("What type of vehicle do you have? Press the number: 1. Car, 2. Truck, 3. Van, 4. Motorcycle ")
            if vehicleType.isnumeric():
                vehicleType = int(vehicleType)
            else:
                print("Incorrect option")
        if vehicleType == 1 and pl.freeSpotsCars == 0:
            return False
        elif vehicleType == 2 and pl.freeSpotsTrucks == 0:
            return False
        elif vehicleType == 3 and pl.freeSpotsVans == 0:
            return False
        elif vehicleType == 4 and pl.freeSpotsMotorcycles == 0:
            return False
        
        pd = ParkingDisplayBoard(self.pl)
        pd.printParkingLot()

        spot = "000"
        while not(self.correctSpotCode(spot, vehicleType)):
            spot = input("Choose where you want to park your vehicle: ")
                #The first character should be the floor number (up to five); 
                #the second character should be 'A', 'B', 'C', or 'D'; 
                # and the third character should be the spot number (up to 10). 
                # Section 'A' is for cars, 'B' for trucks, 'C' for vans, and 'D' for motorcycles. 
                # Examples: 1A9 or 2D10 or 5B2.
        pet = 0
        while pet != 1 and pet != 2:
            pet = input("Do you have a pet inside? Press the number: 1. Yes, 2. No ")
            if pet == '1' or pet == '2':
                pet = int(pet)
            else:
                print("Incorrect option")
        if(pet == 1): pet = True
        else: pet = False
        return ParkingTicket(pl, vehicleType, pet, spot)
    
    def correctSpotCode(self, spot: str, vehType: int):
        if len(spot) != 3 and len(spot) != 4:
            return False
        if int(spot[0]) < 0 or int(spot[0]) > len(self.pl.floors):
            return False
        if spot[1] != 'A' and spot[1] != 'B' and spot[1] != 'C' and spot[1] != 'D':
            return False
        if spot[2] != '1' and spot[2] != '2' and spot[2] != '3' and spot[2] != '4' and spot[2] != '5' and spot[2] != '6' and spot[2] != '7' and spot[2] != '8' and spot[2] != '9' and spot[2:] != "10":
            return False
        if not(spot[1] == 'A' and vehType == 1) and not(spot[1] == 'B' and vehType == 2) and not(spot[1] == 'C' and vehType == 3) and not(spot[1] == 'D' and vehType == 4):
            print("Incorrect section. Type it again.")
            print()
            return False
        
        temp = ord(spot[1]) - 65
        if self.pl.floors[int(spot[0])-1].sections[temp].spots[int(spot[2:])-1].isFree == False:
            print("Invalid spot. It is already occupied.")
            print()
            return False
        return True
    
    def spotCodeConverter(self, pt: ParkingTicket):
        #Change from human readable code to machine language code. Ex. 1B3 = floors[0], sections[1], spots[2] 
        fl = int(pt.spot[0])-1
        se = ord(pt.spot[1]) - 65
        sp = int(pt.spot[2:])-1
        return fl, se, sp
        
    def printTicket(self):
        ticket = self.inputInfoForTicket(self.pl)
        if ticket == False:
            print("Sorry, no more space. Follow the exit signs.")
            return 0
        self.pl.tickets.append(ticket) #Add the new ticket to the parking lot system
        fl, se, sp = self.spotCodeConverter(ticket)
        self.pl.floors[fl].sections[se].spots[sp].isFree = False
        print()
        print("-----------------------------")
        print(f"Ticket number: {ticket.ticketNumber}")
        print("Issued at date: ", end="")
        print (ticket.issuedAtDate.strftime("%Y-%m-%d %H:%M:%S"))
        print(f"Vehicle type: {ticket.vehicleType.name}")
        print(f"Spot selected: {ticket.spot}")
        print(f"Pet inside: {ticket.pet}")
        print(ticket.payStatus)
        print("-----------------------------")
        print()
        self.openEntranceDoor()
        print()

    def openEntranceDoor(self):
        print("Come in!")
    
class Payment():
    def __init__(self, ticketCreationDate: str, additionalFee: bool):
        self.ticketCreationDate = ticketCreationDate
        self.additionalFee = additionalFee
        self.amount = self.calculateAmountToPay()

    def calculateAmountToPay(self):
        currentTime = datetime.datetime.now()
        timeDifference = currentTime - self.ticketCreationDate
        seconds = timeDifference.seconds
        if seconds < 3600:
            amount = 0
        elif seconds >= 3600 and seconds < (3600 * 2):
            amount = 4
        elif seconds >= (3600 * 2) and seconds < (3600 * 4):
            amount = (((seconds - 3600) // 3600) * 3.5) + 4
        else:
            amount = (((seconds - (3600 * 3)) // 3600) * 2.5) + 11

        if amount == 0 and self.additionalFee == True:
            amount = 4
        elif amount > 0 and self.additionalFee == True:
            amount = amount * 2
        return amount
    
    def initiateTransaction(self):
        print(f"It is ${self.amount:.2f} dollars.")
        if self.amount > 0:
            paymentMethod = ''
            while paymentMethod != '1' and paymentMethod != '2':
                paymentMethod = input("Type '1' for card payment and '2' for cash payment: ")
            if paymentMethod == '1':
                cardName = input("Insert card: ")
            else:
                cash = 0
                while cash < self.amount:
                    cash += float(input("Insert bills or coins: "))

                if cash > self.amount:
                    change = cash - self.amount
                    print(f"Here is your change: ${change:.2f}")

class ExitPanel():
    def __init__(self, ident, parkingLot: ParkingLot):
        self.id = ident
        self.pl = parkingLot

    def scanTicket(self):
        valid = False
        while not valid:
            ticketNum = int(input("Enter the ticket number: "))
            for i in self.pl.tickets:
                if i.ticketNumber == ticketNum and i.payStatus == PaymentStatus(1).name:
                    valid = True
                    payment = Payment(i.issuedAtDate, i.additionalFee)
                    result = self.processPayment(payment)
                    if result:
                        i.payAmount = payment.amount
                        i.payStatus = PaymentStatus(2).name
                        i.paidAtDate = datetime.datetime.now()
                        temp = ord(i.spot[1]) - 65
                        self.pl.floors[int(i.spot[0])-1].sections[temp].spots[int(i.spot[2:])-1].isFree = True
                        if temp == 0: self.pl.freeSpotsCars += 1
                        elif temp == 1: self.pl.freeSpotsTrucks += 1
                        elif temp == 2: self.pl.freeSpotsVans += 1
                        else: self.pl.freeSpotsMotorcycles += 1
                        self.openExitDoor()
                    else: 
                        print("We are sorry, but there was a problem during the transaction.")
                    
            if valid == False:
                print("There is no unpaid ticket with that number.")

    def processPayment(self, payment: Payment):
        payment.initiateTransaction()
        return True
    
    def openExitDoor(self):
        print("You can leave. Thanks for coming!")
        print()

class ParkingFloor():
    def __init__(self, ident):
        self.id = ident
        self.sections = []
        for i in "ABCD":
            self.sections.append(ParkingSection(i, self.id))

class ParkingSection():
    def __init__(self, ident, floor):
        self.id = ident
        self.floor = floor
        self.spots = []
        for i in range(1, 11):
            if self.id == "A":
                self.spots.append(ParkingSpot(i, self.id, self.floor, "CAR"))
            elif self.id == "B":
                self.spots.append(ParkingSpot(i, self.id, self.floor, "TRUCK"))
            elif self.id == "C":
                self.spots.append(ParkingSpot(i, self.id, self.floor, "VAN"))
            else:
                self.spots.append(ParkingSpot(i, self.id, self.floor, "MOTORCYCLE"))

class ParkingSpot():
    def __init__(self, ident, section, floor, vehType):
        self.id = ident
        self.section = section
        self.floor = floor
        self.isFree = True
        self.vehicleType = vehType

class Account():
    def __init__(self, parkingLot: ParkingLot, username: str, password: str):
        self.pl = parkingLot
        self.username = username
        self.password = password
        self.status = AccountStatus(1).name
    
    def checkMapOfParkingLot(self):
        self.pl.parkingDisplayBoards[0].printParkingLot()

class ParkingAttendant(Account):
    def checkTickets(self):
        for i in self.pl.tickets:
            print("-----------------------------")
            print(f"Ticket number: {i.ticketNumber}")
            print(f"Vehicle type: {i.vehicleType.name}")
            print(f"Spot: {i.spot}")
            print(f"Pet: {i.pet}")
            print(f"Issued at date: {i.issuedAtDate}")
            print(f"Paid at date: {i.paidAtDate}")
            print(f"Fee: ${i.payAmount:.02f}")
            print(f"Payment status: {i.payStatus}")
            print(f"Additional fee: {i.additionalFee}")
            print("-----------------------------")

    def addAdditionalFee(self, ticket: ParkingTicket):
        ticket.additionalFee = True
    
    def removeAdditionalFee(self, ticket: ParkingTicket):
        ticket.additionalFee = False

    def checkNumOfFreeSpots(self):
        print(f"A: {self.pl.freeSpotsCars}, B: {self.pl.freeSpotsTrucks}, C: {self.pl.freeSpotsVans}, D: {self.pl.freeSpotsMotorcycles}")

class Admin(Account):
    def addParkingFloor(self):
        if len(self.pl.floors) < 9:
            temp = self.pl.floors[-1].id + 1
            self.pl.floors.append(ParkingFloor(temp))
            self.pl.numEntrancePanels += 2
            self.pl.numExitPanels += 2
            for i in range(1, 3):
                temp = self.pl.entrancePanels[-1].id + 1
                self.pl.entrancePanels.append(EntrancePanel(temp, self.pl))
                temp = self.pl.exitPanels[-1].id + 1
                self.pl.entrancePanels.append(ExitPanel(temp, self.pl))
            self.pl.totalSpots += 40
            self.pl.freeSpotsCars += 10
            self.pl.freeSpotsTrucks += 10
            self.pl.freeSpotsVans += 10
            self.pl.freeSpotsMotorcycles += 10
            self.pl.numParkingDisplayBoards += 1
            self.pl.parkingDisplayBoards.append(ParkingDisplayBoard(self.pl))
            print("The new floor has been added.")
        else:
            print("No more floors can be added.")

    def blockParkingAttendant(self):
        self.pl.parkingAttendant.status = AccountStatus(2).name

    def unblockParkingAttendant(self):
        self.pl.parkingAttendant.status = AccountStatus(1).name

    def replaceParkingAttendant(self, username: str, password: str):
        self.pl.parkingAttendant.username = username
        self.pl.parkingAttendant.password = password

class ParkingDisplayBoard():
    def __init__(self, parkingLot: ParkingLot):
        self.pl = parkingLot

    def printLabels(self):
        for i in range(0, 4):
            for j in range(0, 5):
                if j != 0:
                    print("\t", end="")
                else:
                    if i == 0:
                        print("A", end="")
                    elif i == 1:
                        print("B", end="")
                    elif i == 2:
                        print("C", end="")
                    else:
                        print("D", end="")
        print()

    def printSectionSpotNumbers(self, floor: int, section: int):
        print("{", end=" ")
        for i in range(0, 10):
            if self.pl.floors[floor].sections[section].spots[i].isFree == True:
                print(i + 1, end=" ")
            else:
                if i == 9:
                    print(" X", end=" ")
                else:
                    print("X", end=" ")
        print("}", end="\t")

    def printFloor(self, floor: ParkingFloor):
        print(f"Floor {floor.id}")
        self.printLabels()
        for i in range(0, 4):
            self.printSectionSpotNumbers((floor.id - 1), i)
            if i == 3:
                print()

    def printParkingLot(self):
        print()
        for i in reversed(range(0, len(self.pl.floors))):
            self.printFloor(self.pl.floors[i])
            print()

class AdminPortal():
    def __init__(self, pl: ParkingLot):
        self.pl = pl
        self.admin = self.pl.admin

    def menu(self):
        pw = input("Admin: Type your password: ")
        if pw == self.admin.password:
            while(True):
                while(True):
                    option = input("Choose one of the following options: '1' to add a new parking floor, '2' to see the map of the parking lot, '3' to block a parking attendant, '4' to unblock a parking attendant, '5' to replace the parking attendant, and '6' to exit: ")
                    if option == '1' or option == '2' or option == '3' or option == '4' or option == '5' or option == '6':
                        break
                if option == '1':
                    self.admin.addParkingFloor()
                elif option == '2':
                    self.admin.checkMapOfParkingLot()
                elif option == '3':
                    name = input("Type the name of the parking attendant: ")
                    if name == self.pl.parkingAttendant.username:
                        self.admin.blockParkingAttendant()
                        print("The parking attendant account has been blocked.")
                    else:
                        print("That name does not exist.")
                elif option == '4':
                    name = input("Type the name of the parking attendant: ")
                    if name == self.pl.parkingAttendant.username:
                        self.admin.unblockParkingAttendant()
                        print("The parking attendant account has been unblocked.")
                    else:
                        print("That name does not exist.")
                elif option == '5':
                    newName = input("Type the name of the new parking attendant: ")
                    password = input("Type the password of the new parking attendant: ")
                    self.admin.replaceParkingAttendant(newName, password)
                    print("The parking attendant has been replaced.")
                else:
                    break
        else:
            print("Failed")

class ParkingAttendantPortal():
    def __init__(self, pl: ParkingLot):
        self.pl = pl
        self.parkingAttendant = self.pl.parkingAttendant

    def menu(self):
        pw = input("Parking attendant: Type your password: ")
        if pw == self.parkingAttendant.password:
            if self.parkingAttendant.status == AccountStatus(1).name:
                while(True):
                    while(True):
                        option = input("Choose one of the following options: '1' to check the tickets, '2' to see the map of the parking lot, '3' to check the number of free spots, '4' to add an additional fee, '5' to remove an additional fee, and '6' to exit: ")
                        if option == '1' or option == '2' or option == '3' or option == '4' or option == '5' or option == '6':
                            break
                    if option == '1':
                        self.parkingAttendant.checkTickets()
                    elif option == '2':
                        self.parkingAttendant.checkMapOfParkingLot()
                    elif option == '3':
                        self.parkingAttendant.checkNumOfFreeSpots()
                    elif option == '4':
                        ticketNum = input("What is the ticket number: ")
                        if ticketNum.isnumeric():
                            ticketNum = int(ticketNum)
                            for i in self.pl.tickets:
                                if i.ticketNumber == ticketNum and i.additionalFee == False and i.payStatus == PaymentStatus(1).name:
                                    self.parkingAttendant.addAdditionalFee(i)
                                    print("The additional fee has been added.")
                    elif option == '5':
                        ticketNum = input("What is the ticket number: ")
                        if ticketNum.isnumeric():
                            ticketNum = int(ticketNum)
                            for i in self.pl.tickets:
                                if i.ticketNumber == ticketNum and i.additionalFee == True and i.payStatus == PaymentStatus(1).name:
                                    self.parkingAttendant.removeAdditionalFee(i)
                                    print("The additional fee has been removed.")
                    else:
                        break
            else: print("You are not allowed to log in.")
        else:
            print("Failed")

#Examples:
PL = ParkingLot("Ensenada, Baja California", "Pepe", "flymetothemoon")
adm = Admin(PL, "Pepe", "flymetothemoon")
adm.replaceParkingAttendant("Juan", "Iusedtoruletheworld")
PL.parkingAttendant.checkMapOfParkingLot()
adm.addParkingFloor()
print(f"Number of floors: {len(PL.floors)}")
for i in range(0, 2):
    PL.entrancePanels[0].printTicket()
PL.parkingAttendant.checkNumOfFreeSpots()
PL.parkingAttendant.addAdditionalFee(PL.tickets[0])
PL.parkingAttendant.checkTickets()
PL.exitPanels[0].scanTicket()
PL.parkingAttendant.checkNumOfFreeSpots()
PL.entrancePanels[0].printTicket()
PL.parkingAttendant.checkNumOfFreeSpots()
PL.admin.checkMapOfParkingLot()

adminPortal = AdminPortal(PL)
adminPortal.menu()

parkingAttendantPortal = ParkingAttendantPortal(PL)
parkingAttendantPortal.menu()
