import os

import barcode
from airtable import Airtable
from barcode.writer import ImageWriter
from pathlib import Path


def generate_single_barcode(data):
    print(data)
    CODE128 = barcode.get_barcode_class("code128")
    code = CODE128(data, writer=ImageWriter())
    with Path("codes", f"{data}.png".replace('/', '-')).open("wb") as f:
        code.write(f)

def get_all_instrument_numbers():
    at = Airtable(base_key=os.environ.get('AIRTABLE_BASE_KEY'), table_name='Instruments')
    for page in at.get_iter():
        for record in page:
            if not record['fields'].get('Number', False):
                continue
            generate_single_barcode(record['fields']['Number'].strip())


if __name__ == '__main__':
    get_all_instrument_numbers()

