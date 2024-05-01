import os

from utils import Log

log = Log('Parser')



class Parser:
    def __init__(self, id):
        self.id = id

    @property
    def pdf_path(self):
        return os.path.join(
            'original_pdfs',
            f'general-election-{self.id}.pdf',
        )
