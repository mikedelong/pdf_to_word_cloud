import logging
import os

import textract
import wordcloud
import collections
import matplotlib.pyplot as plt

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
output_folder = './output/'

for file_name in os.listdir(input_folder):
    logger.debug('base input file name: %s' % file_name)
    input_file_name = input_folder + file_name
    logger.debug('relative input file name: %s' % input_file_name)

    input_text = textract.process(input_file_name).lower()
    text = ' '.join(input_text.split('\n'))
    text = text.replace('also', '')

    result = wordcloud.WordCloud().generate(text)
    plt.imshow(result, interpolation='bilinear')
    plt.axis("off")
    output_file_name = file_name.replace('.pdf', '.jpg')
    plt.savefig(output_folder + output_file_name)
