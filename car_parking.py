from tabulate import tabulate

class Vehicle:
    def __init__(self, RegistrationNumber, color):
        self.RegistrationNumber = RegistrationNumber
        self.color = color

class ParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.currentVehiclesCount = 0
        self.parkingSlots = [None]*capacity
        self.ParkedVehicles = {}    # Dictionary for Keeping Track of Parked Vehicles (From Registration Number)
        self.colorTracker = {}      # A Dictionary of colors, [slotIndices] to retrieve all cars of any given color

    # Function to Park a Vehicle
    def ParkVehicle(self, Vehicle):
        """This Function Parks a Vehicle if Slots are present. Worst Case O(n)"""
        if self.currentVehiclesCount == self.capacity:
            print "Sorry, Parking Lot is Full"
            return

        # Check if a Duplicate Vehicle Being Entered
        if Vehicle.RegistrationNumber in self.ParkedVehicles:
            print "This Vehicle is Already Parked at Slot:" + str(self.ParkedVehicles[Vehicle.RegistrationNumber])
            return

        # Empty Space is Present
        emptySlot = 0
        while(self.parkingSlots[emptySlot] != None):
            emptySlot += 1     # Get the Empty Position

        # Add to the Slots
        self.parkingSlots[emptySlot] = Vehicle
        self.ParkedVehicles[Vehicle.RegistrationNumber] = emptySlot
        self.currentVehiclesCount += 1

        # Add to colors array
        if Vehicle.color in self.colorTracker:
            self.colorTracker[Vehicle.color].append(emptySlot)
        else:
            self.colorTracker[Vehicle.color] = [emptySlot]

        print "Allocated Slot Number: " + str(emptySlot+1)

    # Function to Remove a Vehicle From Parking Lot
    def RemoveVehicle(self, slotNumber):
        """This Function Removes a Vehicle From a Given Slot. Worst Case O(1)"""
        if slotNumber > self.capacity or slotNumber < 1:
            print "No Such Slot Present. Please Enter a slot Number Present in the Parking Lot"
            return

        # No Vehicle at the Given Slot
        if(self.parkingSlots[slotNumber-1] is None):
            print "No Vehicle Present at Slot: " + str(slotNumber)
            return

        # Valid Vehicle Present. Remove It
        outGoingVehicle = self.parkingSlots[slotNumber-1]
        self.parkingSlots[slotNumber-1] = None
        self.currentVehiclesCount -= 1
        if outGoingVehicle.RegistrationNumber in self.ParkedVehicles:        # Remove From Dictionary
            del self.ParkedVehicles[outGoingVehicle.RegistrationNumber]
        if outGoingVehicle.color in self.colorTracker:                       # Remove From Color Tracker
            self.colorTracker[outGoingVehicle.color].remove(slotNumber-1)
            if len(self.colorTracker[outGoingVehicle.color]) == 0:
                del self.colorTracker[outGoingVehicle.color]
        print "Slot Number: " + str(slotNumber) + " is free"

    # Get ALl Cars With Given Color
    def RetrieveSlotsWithGivenColor(self, color, printRes = False):
        "Get All Slots which have cars parked with the given color"
        if color in self.colorTracker:
            if printRes == True:
                print ",".join(str(x+1) for x in self.colorTracker[color])
            return self.colorTracker[color]
        else:
            if printRes == True:
                print "No Cars Are Parked with the Given Color"
            return []

    # Get the Registration Number of Cars with the Given Color
    def RegistrationNumbersWithGivenColor(self, color):
        "Get All Registration Number of cars parked with the given color"
        allSlots = self.RetrieveSlotsWithGivenColor(color, False)
        if len(allSlots) == 0:
            print "No Cars Are Parked with the Given Color"
            return
        RegistrationNumbers = []
        for eachSlot in allSlots:
            RegistrationNumbers.append(self.parkingSlots[eachSlot].RegistrationNumber)
        print ",".join(RegistrationNumbers)

    # Get the Slot With this Vehicle Registration Number
    def ParkingSlotWithGivenRegistrationNumber(self, RegNum):
        "Get The Slot with the Given Registration Number"
        if RegNum in self.ParkedVehicles:
            print self.ParkedVehicles[RegNum] + 1
        else:
            print "Not Found"

    # Get the Overall ParkingLot Status
    def ParkingLotStatus(self):
        "Print all the Vehicles Parked"

        if(len(self.ParkedVehicles) == 0):
            print "No Vehicles Present As of Now."
            return

        counter = 0
        pLStatus = []
        for index in range(0, self.capacity):
            if self.parkingSlots[index] is not None:
                counter += 1
                pLStatus.append([counter, self.parkingSlots[index].RegistrationNumber, index+1, self.parkingSlots[index].color])

        print tabulate(pLStatus, headers=['No', 'RegistrationNumber', 'Slot', 'Color'])

def OperateParkingLot():
    print "Hey, Welcome to Parking Lot Creation Wizard"
    size = int(raw_input("Please Enter the Size of Your Parking Lot(int)::"))       # Forcing the User to Create a Parking Lot Before Performing OPerations
    pL = ParkingLot(size)
    print "Created a parking Lot with " + str(size) + " slots"

    permittedOperation = [
        "park <registration_number> <color>",   # Park a Vehicle
        "leave <slotNumber>",                   # Remove a Vehicle
        "Status",                               # All Parked Vehicles
        "registration_numbers_for_cars_with_color <color>",
        "slot_numbers_for_cars_with_color <color>",
        "slot_number_for_registration_number <registration_number>"
    ]

    print "You are permitted the following Operations:"
    print "\n".join(permittedOperation)
    print ""

    while(True):
        input = raw_input().strip().split(" ")
        input[0] = input[0].lower()
        # Handle Incorrect Input Formats
        try:
            if input[0] == "park":
                # Park Cars
                carRegNum = input[1].upper()
                carColor = input[2].upper()
                newVehicle = Vehicle(carRegNum, carColor)
                pL.ParkVehicle(newVehicle)
            elif input[0] == "leave":
                slot = int(input[1])
                pL.RemoveVehicle(slot)
            elif input[0] == "status":
                pL.ParkingLotStatus()
            elif input[0] == "registration_numbers_for_cars_with_color":
                color = input[1].upper()
                pL.RegistrationNumbersWithGivenColor(color)
            elif input[0] == "slot_numbers_for_cars_with_color":
                color = input[1].upper()
                pL.RetrieveSlotsWithGivenColor(color, printRes=True)
            elif input[0] == "slot_number_for_registration_number":
                regNum = input[1].upper()
                pL.ParkingSlotWithGivenRegistrationNumber(regNum)
            else:
                print "Your Command Not Supported by the Parking Lot, as of Now. Please try one of the available operations ?"
        except IndexError:
            print "Incorrect Input Format"


if __name__ == "__main__":
    OperateParkingLot()
