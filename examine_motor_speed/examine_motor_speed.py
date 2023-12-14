from time import sleep
from pathlib import Path
from csv import DictWriter
from buildhat import Motor

#get the absolute path of the parent directory of the file
file_path = Path(__file__)
file_path = file_path.resolve()
directory_path = file_path.parent
csv_path = directory_path.joinpath('examine_motor_speed_results.csv')

#set up the motor
motor_letter = 'A'
motor = Motor(motor_letter)
motor.on()
motor.stop() #stop instantly, because when the motor gets turned on, it will start rotating seemily random
degrees_to_reset = -motor.get_position() + 360 #this resets the motor to 360 degrees
motor.run_for_degrees(degrees_to_reset, 50)
sleep(1.1) #sleep 1.1 seconds to make sure it has stopped turning

with open(csv_path, 'w', newline='') as file:
	fieldnames = ['speed',
	'test 1: position before turning (in degrees)', 'test 1: position after turning (in degrees)', 'test 1: deviation (in degrees)',
	'test 2: position before turning (in degrees)', 'test 2: position after turning (in degrees)', 'test 2: deviation (in degrees)',
	'test 3: position before turning (in degrees)', 'test 3: position after turning (in degrees)', 'test 3: deviation (in degrees)',
	'average deviation (in degrees)']

	writer = DictWriter(file, fieldnames)
	writer.writeheader() #this writes the fieldnames in the first row
	for speed in range(1, 102, 5):
		if speed != 1:
			speed -= 1
		results = {fieldnames[0]: speed}
		print(f'Testing speed: {speed}')

		for test in range(0, 3):
			degrees_to_reset = -motor.get_position() + 360 #this resets the motor to 360 degrees
			motor.run_for_degrees(degrees_to_reset, 50)
			sleep(1.1) #sleep 1.1 seconds to make sure it has stopped turning

			position_before_index = test*3 + 1 #+ 1, since you need to go past the index of 'speed'
			position_before = motor.get_position()
			results[fieldnames[position_before_index]] = position_before #'position before turning (in degrees)'

			motor.run_for_degrees(360, speed=speed)
			sleep(1.1) #sleep 1.1 seconds to make sure it has stopped turning
			motor.run_for_degrees(-360, speed=speed)
			sleep(1.1) #sleep 1.1 seconds to make sure it has stopped turning

			position_after_index = test*3 + 2 #+ 2, since you need to go past the indices of 'speed' and 'position before turning (in degrees)'
			position_after = motor.get_position()
			results[fieldnames[position_after_index]] = position_after #'position after turning (in degrees)'

			deviation_index = test*3 + 3 #+ 3, since you need to go past the indices 'speed', 'position before turning (in degrees)' and 'position after turning (in degrees)'
			deviation = position_before - position_after
			results[fieldnames[deviation_index]] = deviation #'deviation (in degrees)'

		average_deviation = (results[fieldnames[3]]+results[fieldnames[6]]+results[fieldnames[9]]) / 3
		results[fieldnames[10]] = average_deviation #'average deviation (in degrees)'
		writer.writerow(results)
