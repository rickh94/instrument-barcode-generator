import os

import treepoem
from airtable import Airtable
from pathlib import Path


def generate_single_barcode(data):
    print(data)
    image = treepoem.generate_barcode(
        barcode_type="code128",
        data=data,
        options={
            "height": "0.3",
            "includetext": True,
            "showborder": False,
            "textyoffset": "2",
            "textfont": "Arial"
        },
    )
    image.convert("1").save(str(Path("codes", f"{data}.png")))


def get_all_instrument_numbers():
    at = Airtable(
        base_key=os.environ.get("AIRTABLE_BASE_KEY"), table_name="Instruments"
    )
    for page in at.get_iter():
        for record in page:
            if not record["fields"].get("Number", False):
                continue
            generate_single_barcode(record["fields"]["Number"].strip())


if __name__ == "__main__":
    get_all_instrument_numbers()
