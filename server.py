import random, sched, time
import pandas as pd

hospitals = pd.DataFrame({})
min_time = 1 # min time between arrial of two patients in sec
max_time = 3 # max time between arrival of two patients in sec
max_duration = 5400 # max time of patient duration in sec
max_patients = 30 # max number of patients/beds
min_nurses = 0
max_nurses = 30
min_drs = 0
max_drs = 30
min_techs = 0
max_techs = 30

class Hospital():
    def __init__(self, index):
        self.hospitals_index = index
        self.patients = 0
        self.nurses = 0
        self.drs = 0
        self.techs = 0
        self.timer = sched.scheduler(time.time, time.sleep)
        self.timer.enter(2, 1, self.update, ())
        self.timer.run()

    def update(self):
        # TO DO:
            # randomly add patients
            # new covid test shipment arrived
            # add dr, nurse, tech
            # calculate num vents being used
        
        # add/remove some number of patients
        self.patients = self.update_count(self.patients, 0, max_patients)
        
        # add/remove some number of nurses
        self.nurses = self.update_count(self.nurses, min_nurses, max_nurses)

        # add/remove some number of doctors
        self.drs = self.update_count(self.drs, min_drs, max_drs)
        
        # add/remove some number of techs
        self.techs = self.update_count(self.techs, min_techs, max_techs)

        print([self.patients, self.nurses, self.drs, self.techs])
        
        self.timer.enter(random.randint(min_time, max_time), 1, self.update, ())
        self.timer.run()
    
    def update_count(self, count, min, max):
        count += random.randint(-1, 1)
        if count < min:
            count = min
        elif count > max:
            count = max
        return count
    
    def add_PCI(self):
        pass
    
    def add_rapid(self):
        pass

h = Hospital(0)