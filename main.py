import logging
import os

import matplotlib.pyplot as plt
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
output_folder = './output/'

ignore_words = ['also', 'one']
ignore_words = sorted(ignore_words)
logger.debug('words to ignore: %s' % ignore_words)

for file_name in os.listdir(input_folder):
    logger.debug('base input file name: %s' % file_name)
    input_file_name = input_folder + file_name
    logger.debug('relative input file name: %s' % input_file_name)

    input_text = textract.process(input_file_name).lower()
    text = ' '.join(input_text.split('\n'))

    for ignore_word in ignore_words:
        text = text.replace(ignore_word, '')

    result = wordcloud.WordCloud().generate(text)
    figure, axes = plt.subplots(figsize=(16, 9))
    axes.imshow(result, interpolation='bilinear')
    figure.tight_layout()
    plt.axis("off")
    output_file_name = file_name.replace('.pdf', '.jpg')
    full_output_filename = output_folder + output_file_name
    logger.debug('writing result to %s' % full_output_filename)
    plt.savefig(full_output_filename)
