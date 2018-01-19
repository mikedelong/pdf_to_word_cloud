import collections
import logging
import os

import PyPDF2

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

ignore_words_file = './ignore-words.txt'

if True:
    ignore_words = ['also', 'one', 'and', 'the', 'for', 'to', 'from', 'is', 'or', 'in', 'of', '-', 'a', 'as', 'an',
                    'this',
                    'that', 'will', 'are', 'not', 'be', 'by', 'with', 'on', 'it', 'may', 'only', 'without', 'at',
                    'must',
                    'no', 'who', 'does', 'all', 'their', 'other', 'any', 'e', 's', 'if', 'nor', 'should', 'we', 'our',
                    'use', 'have', 'when', 'they', 'has', 'through', 'while', 'more']
    ignore_words = sorted(ignore_words)
    logger.debug('words to ignore: %s' % ignore_words)
else:
    pass

# todo what if these folders do not exist?
input_folder = './input/'
output_folder = './output/'

for item in os.listdir(input_folder):
    if item.endswith('.pdf') or item.endswith('PDF'):
        logger.debug('base input file name: %s' % item)
        input_file_name = input_folder + item
        logger.debug('relative input file name: %s' % input_file_name)

        text = list()
        with open(input_file_name, 'rb') as pdf_input:
            pdf_file_reader = PyPDF2.PdfFileReader(pdf_input)
            number_of_pages = pdf_file_reader.getNumPages()
            for page in range(0, number_of_pages):
                reader_page = pdf_file_reader.getPage(page)
                page_content = reader_page.extractText()
                text.append(page_content)

        text = ' '.join([item for item in text])

        for key, value in punctuation_outliers.items():
            text = text.replace(key, value)

        for token in ['\n', '.', ',', '(', ')']:
            text = text.replace(token, ' ')
        text = text.split(' ')
        text = [item.strip() for item in text if item.lower() not in ignore_words]
        text = [item for item in text if len(item) > 0]
        text = [item for item in text if not item.isnumeric()]

        # let's use a Counter to get the top N
        most_common_count = 40
        counts = collections.Counter(text)
        tops = [item[0] for item in counts.most_common(most_common_count)]

        text = [item for item in text if item in tops]
        # we know from the if-then structure above we only need to handle two cases here
        output_file = item.replace('.pdf', '.txt') if item.endswith('.pdf') else item.replace('.PDF', '.txt')

        full_output_filename = output_folder + output_file
        logger.debug('writing results to %s' % full_output_filename)
        with open(full_output_filename, 'w', encoding='utf-8') as output_file_pointer:
            for line in text:
                line = line.strip()
                if len(line) > 0:
                    output_file_pointer.write('%s\n' % line)
    else:
        logger.debug('ignoring file %s due to improper suffix' % item)
