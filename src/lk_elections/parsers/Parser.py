import os
import re

from utils import Log

from lk_elections.core import ElectionFPTP

log = Log('Parser')


class Parser:
    def __init__(self, id):
        self.id = id

    @property
    def pdf_path(self):
        return os.path.join(
            'data',
            'original_pdfs',
            f'general-election-{self.id}.pdf',
        )
    
    @property
    def pdf_path_linux(self):
        return self.pdf_path.replace('\\', '/')

    def parse(self):
        log.info(f'Parsing {self.id}...')
        election = ElectionFPTP(
            date_str=self.id,
            results=self.results,
        )
        election.save()

    def clean(s):
        s = re.sub(r'\s+', ' ', s).strip()
        s = re.sub(r'[^a-zA-Z ]', '', s)
        s = s.lower().title()
        for before, after in [
            ['Cart Wheet', 'Cart Wheel'],
            ['Cartwheel', 'Cart Wheel'],
            ['Chai', 'Chair'],
            ['Chairr', 'Chair'],
            ['Coclerel', 'Cockerel'],
            ['Elepaht', 'Elephant'],
            ['Elepant', 'Elephant'],
            ['Elephnt', 'Elephant'],
            ['Elepnant', 'Elephant'],
            ['Housse', 'House'],
            ['Lader', 'Ladder'],
            ['Omni Bus', 'Bus'],
            ['Pair If Scakes', 'Pair Of Scales'],
            ['Pair Of Scacles', 'Pair Of Scales'],
            ['Pair Of Scaless', 'Pair Of Scales'],
            ['Pine Apple', 'Pineapple'],
            ['Pine-Apple', 'Pineapple'],
            ['Radio Set', 'Radio'],
            ['Sweing Machine', 'Sewing Machine'],
            ['Winnow', 'Window'],
        ]:
            s = s.replace(before, after)
        return s
