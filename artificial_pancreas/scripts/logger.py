import logging
from sys import stdout

class SerinterfaceFilter(logging.Filter):
	def filter(self, record):
		return record.module != 'serinterface' #otherwise the buildhat library logs every read and write on the serial interface

def initialise_logger(debug_mode, directory_path):
	level = logging.DEBUG if debug_mode else logging.INFO
	log_path = directory_path.joinpath('artificial_pancreas.log')
	file_handler = logging.FileHandler(log_path)
	stream_handler = logging.StreamHandler(stdout)
	logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=level, handlers=(file_handler, stream_handler))
	logging.root.addFilter(SerinterfaceFilter())