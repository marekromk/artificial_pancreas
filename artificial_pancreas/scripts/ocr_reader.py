from logging import debug
from easyocr import Reader

class OCRReader:
    characters = '0123456789,.' #the characters to search for
    min_confidence_level = 0.95 #the minimum confidence level a found number should have to be returned by 'read_frame'

    def __init__(self):
        self.model = Reader(['en'], gpu=False)

    def read_frame(self, frame):
        found_numbers = self.model.readtext(frame, allowlist=self.characters)
        if not found_numbers:
            return
        debug(f'The OCR returned: {found_numbers}')

        #find the index of the found number with the highest confidence level
        confidence_levels = [found_number[2] for found_number in found_numbers] #index 2 is the confidence level
        max_confidence = max(confidence_levels)
        debug(f'The OCR\'s highest returned confidence level is: {max_confidence}')
        if max_confidence < self.min_confidence_level:
            return
        max_confidence_index = confidence_levels.index(max_confidence) #find the index of the highest confidence level

        max_confidence_number_str = found_numbers[max_confidence_index][1] #index 1 is the found number as a string
        max_confidence_number_str = max_confidence_number_str.replace(',', '.')
        if max_confidence_number_str.count('.') > 1:
            return
        max_confidence_number = float(max_confidence_number_str)
        debug(f'The OCR read the number: {max_confidence_number}')
        return max_confidence_number