import logging
import os

if False:
    import textract
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
ignore_words = ['also', 'one']
ignore_words = sorted(ignore_words)
logger.debug('words to ignore: %s' % ignore_words)

# todo what if these folders do not exist?
input_folder = './input/'
output_folder = './output/'

for item in os.listdir(input_folder):
    if item.endswith('.pdf') or item.endswith('PDF'):
        logger.debug('base input file name: %s' % item)
        input_file_name = input_folder + item
        logger.debug('relative input file name: %s' % input_file_name)

        if False:
            text = textract.process(input_file_name)
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
        for ignore_word in ignore_words:
            text = text.replace(ignore_word, '')

        for token in ['\n', '.', ',', '(', ')']:
            text = text.replace(token, ' ')
        text = text.split(' ')

        # we know from the if-then structure above we only need to handle two cases here
        output_file = item.replace('.pdf', '.txt') if item.endswith('.pdf') else item.replace('.PDF', '.txt')

        full_output_filename = output_folder + output_file
        logger.debug('writing results to %s' % full_output_filename)
        with open(full_output_filename, 'w') as output_file_pointer:
            for line in text:
                line = line.strip()
                if len(line) > 0:
                    output_file_pointer.write('%s\n' % line)
    else:
        logger.debug('ignoring file %s due to improper suffix' % item)
