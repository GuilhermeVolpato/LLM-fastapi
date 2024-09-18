import logging

logging.basicConfig(
    filename='servico.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)
logger = logging.getLogger(__name__)
