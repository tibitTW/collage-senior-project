import logging
logging.basicConfig(filename='worklog.log',
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    level=logging.DEBUG)

logging.debug('debug test', exc_info=True)
logging.error('Error test')
