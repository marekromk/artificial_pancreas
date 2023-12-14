from scripts import *

class ArtificialPancreas:
	def __init__(self, camera_index, motor_port):
		debug_mode = get_debug_mode()
		directory_path = get_directory_path(__file__)
		initialise_logger(debug_mode, directory_path)

		self.camera = Camera(debug_mode, camera_index)
		self.ocr_reader = OCRReader()
		self.pump = Pump(self, motor_port)

		keyboardinterrupt_handler(self.camera)

	def run(self):
		while self.camera.is_open and self.pump.is_connected:
			frame = self.camera.get_frame()
			self.camera.show_frame(frame)
			glucose_level = self.ocr_reader.read_frame(frame)
			units = self.pump.calculate_units(glucose_level)
			self.pump.flow(glucose_level, units)

if __name__ == '__main__':
	camera_index = 0
	motor_port = 'A'
	ArtificialPancreas(camera_index, motor_port).run()