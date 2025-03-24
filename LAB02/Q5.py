import time
from typing import Dict, List, Tuple

class HospitalEnvironment:
    def __init__(self):
        self.corridors = ["Corridor1", "Corridor2", "Corridor3"]
        self.patient_rooms = {
            "Room101": "Patient1",
            "Room102": "Patient2",
            "Room103": "Patient3"
        }
        self.nurse_stations = ["NurseStation1", "NurseStation2"]
        self.medicine_storage = {"MedicineA": 5, "MedicineB": 3, "MedicineC": 7}

class DeliveryRobot:
    def __init__(self, environment: HospitalEnvironment):
        self.environment = environment
        self.current_location = "Corridor1"
        self.medicine_inventory: Dict[str, int] = {}

    def move_to(self, location: str):
        print(f" Moving from {self.current_location} to {location}...")
        time.sleep(1)  
        self.current_location = location
        print(f" Arrived at {location}.")

    def pick_up_medicine(self, medicine: str, quantity: int):
        if medicine not in self.environment.medicine_storage:
            print(f" Error: {medicine} is not available in storage.")
            return

        if self.environment.medicine_storage[medicine] < quantity:
            print(f"Error: Not enough {medicine} in storage (available: {self.environment.medicine_storage[medicine]}).")
            return

        self.environment.medicine_storage[medicine] -= quantity
        self.medicine_inventory[medicine] = self.medicine_inventory.get(medicine, 0) + quantity
        print(f" Picked up {quantity} units of {medicine}.")

    def deliver_medicine(self, room: str, patient: str, medicine: str, quantity: int):
        if medicine not in self.medicine_inventory or self.medicine_inventory[medicine] < quantity:
            print(f"Error: Not enough {medicine} in inventory to deliver to {patient}.")
            return

        self.medicine_inventory[medicine] -= quantity
        print(f" Delivered {quantity} units of {medicine} to {patient} in {room}.")
        self.scan_patient_id(room, patient)

        if medicine == "MedicineC":  # Critical medicine alert
            self.alert_staff(f"Critical medicine delivered to {patient} in {room}.")

    def scan_patient_id(self, room: str, patient: str):
        print(f" Scanning patient ID for {patient} in {room}...")
        time.sleep(1)  
        print(f"Patient ID verified for {patient}.")

    def alert_staff(self, message: str):
        print(f" Alerting staff at {self.environment.nurse_stations[0]}: {message}")

def execute_delivery_plan(robot: DeliveryRobot, delivery_schedule: List[Tuple[str, str, str, int]]):
    print("\n Starting Delivery Plan...")
    for room, patient, medicine, quantity in delivery_schedule:
        print(f"\n Processing delivery for {patient} in {room}...")

        robot.move_to("MedicineStorage")
        robot.pick_up_medicine(medicine, quantity)

        robot.move_to(room)
        robot.deliver_medicine(room, patient, medicine, quantity)

def main():
    hospital = HospitalEnvironment()
    robot = DeliveryRobot(hospital)

    delivery_schedule = [
        ("Room101", "Patient1", "MedicineA", 2),
        ("Room102", "Patient2", "MedicineB", 1),
        ("Room103", "Patient3", "MedicineC", 1),
    ]

    execute_delivery_plan(robot, delivery_schedule)

    print("\n Final Medicine Storage:", hospital.medicine_storage)
    print(" Robot's Medicine Inventory:", robot.medicine_inventory)

if __name__ == "__main__":
    main()
