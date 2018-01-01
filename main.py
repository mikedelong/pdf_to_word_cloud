import logging
import os

import textract
import wordcloud

# set up logging
formatter = logging.Formatter('%(asctime)s : %(name)s :: %(levelname)s : %(message)s')
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
console_handler.setLevel(logging.DEBUG)
logger.debug('started')

input_folder = './input/'

for file_name in os.listdir(input_folder):
    logger.debug('base input file name: %s' % file_name)
    input_file_name = input_folder + file_name
    logger.debug('relative input file name: %s' % input_file_name)

    input_text = textract.process(input_file_name).lower()

    logger.debug('input text length: %d' % len(input_text))
    tokens = ' '.join(input_text.split('\n'))
    tokens = tokens.split(' ')
    logger.debug(len(tokens))
