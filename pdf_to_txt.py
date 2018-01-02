import logging
import os

import textract

# set up logging
formatter = logging.Formatter('%(asctime)s : %(name)s :: %(levelname)s : %(message)s')
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
console_handler.setLevel(logging.DEBUG)
logger.debug('started')

punctuation_outliers = {'i.e.': 'ie', 'U.S.': 'US'}
ignore_words = ['also', 'one']
ignore_words = sorted(ignore_words)
logger.debug('words to ignore: %s' % ignore_words)

input_folder = './input/'
output_folder = './output/'
for item in os.listdir(input_folder):
    logger.debug('base input file name: %s' % item)
    input_file_name = input_folder + item
    logger.debug('relative input file name: %s' % input_file_name)

    text = textract.process(input_file_name)

    for key, value in punctuation_outliers.iteritems():
        text = text.replace(key, value)
    for ignore_word in ignore_words:
        text = text.replace(ignore_word, '')

    for token in ['\n', '.', ',', '(', ')']:
        text = text.replace(token, ' ')
    text = text.split(' ')

    output_file = item.replace('.pdf', '.txt')
    full_output_filename = output_folder + output_file

    for token in text:
        logger.debug(token)
