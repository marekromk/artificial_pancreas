import logging
from sys import exit
from time import sleep
from buildhat import Motor
from math import floor, modf, ceil
from buildhat.exc import DeviceError

def accurate_round(number):
    fractional = modf(number)[0]
    if fractional >= 0.5:
        rounded_up = ceil(number)
        return rounded_up
    if fractional <= -0.5:
        rounded_up = floor(number)
        return rounded_up
    rounded_down = int(number)
    return rounded_down

class Pump:
    motor_turn = 135 #in degrees
    motor_speed = 35

    cutoff_level = 30 #in mmol/L
    lower_limit_level = 4 #in mmol/L
    upper_limit_level = 12 #in mmol/L
    turning_level = 20 #in mmol/L

    flow_time = 0.1 #in seconds
    ten_minutes = 600 #in seconds
    buffer_time = 0.5 #in seconds

    total_units = 555
    unit_effect = 2.5 #in mmol/L
    units_warning = 444
    add_unit_threshold = 6.5
    millilitres_per_unit = 0.9 #in mL
    minimum_units_under_turning_level = 2
    minimum_units_above_turning_level = 1


    def __init__(self, main, motor_port):
        self.units_counter = 0
        self.main = main #inherit the main ArtificialPancreas class to be able to close the camera if the motor is no longer connected
        try:
            self.motor = Motor(motor_port)
        except DeviceError as e:
            logging.error(e)
            exit()
        self.motor.on()
        self.motor.stop() #stop instantly, because when the motor gets turned on, it will start rotating seemily random
        self.motor.set_default_speed(self.motor_speed)

    @property
    def is_connected(self):
        if not self.motor.connected:
            self.main.camera.close()
            logging.error('The motor is no longer connected')
            exit()
        return True

    def calculate_units(self, glucose_level): #'glucose_level' is in mmol/L
        if glucose_level is None:
            return
        if glucose_level >= self.cutoff_level: #this is done as a precaution, because the blood glucose level should not be higher than 30 mmol/L, as that would mean the OCR has read a number incorrectly
            logging.warning(f'The OCR read that the glucose level is {glucose_level} mmol/L, wich is probably a mistake')
            return
        if glucose_level < self.lower_limit_level:
            logging.warning(f'The glucose level is {glucose_level} mmol/l, which is too low')
            return
        if self.lower_limit_level <= glucose_level <= self.upper_limit_level:
            logging.info(f'The glucose level is {glucose_level} mmol/l, which is in the normal range')
            return

        if glucose_level >= self.turning_level:
            units = self.minimum_units_above_turning_level + accurate_round(glucose_level*0.5 - self.add_unit_threshold) #use 'accurate_round', because since Python version 3.0, Python uses "Banker's Rounding" for its default rounding function, which tends to be inaccurate
            return units
        #this is if the glucose_level < 20
        units = self.minimum_units_under_turning_level + accurate_round(glucose_level*0.5 - self.add_unit_threshold) #use 'accurate_round', because since Python version 3.0, Python uses "Banker's Rounding" for its default rounding function, which tends to be inaccurate
        return units

    def flow(self, glucose_level, units):
        if units is None:
            return
        logging.debug(f'The position of the motor in degrees before turning is: {self.motor.get_aposition()}')
        for unit in range(units):
            self.motor.run_for_degrees(self.motor_turn) #this opens the insulin tap
            sleep(self.flow_time) #this means the insulin tap should be opened for 0.1 seconds
            self.motor.run_for_degrees(-self.motor_turn) #this closes the insulin tap
            sleep(self.buffer_time) #this works as a buffer to be sure that the motor has fully stopped turning
        self.units_counter += units
        logging.debug(f'The position of the motor in degrees after turning is: {self.motor.get_aposition()}')
        logging.debug(f'After having pumped {units} units, there are about {self.total_units - self.units_counter} units left in the reservoir')
        logging.info(f'The pump has pumped {self.millilitres_per_unit * units} mL of insulin solution into the blood, which means the blood glucose level will change from {glucose_level} mmol/L to {glucose_level - self.unit_effect*units} mmol/L')
        if self.units_counter >= self.units_warning:
            logging.warning(f'There are about {self.total_units - self.units_counter} units left, so the reservoir should be refilled')
        sleep(self.ten_minutes)