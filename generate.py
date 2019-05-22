import os

import treepoem
from airtable import Airtable
from pathlib import Path
from multiprocessing import Pool


def generate_single_barcode(data):
    if Path("codes", f"{data}.png".replace("/", "-")).exists():
        return
    print(data)
    image = treepoem.generate_barcode(
        barcode_type="code128",
        data=data,
        options={
            "height": "0.3",
            "includetext": True,
            "showborder": False,
            "textyoffset": "2",
            "textfont": "Arial",
            "inkspread": "0.2",
        },
    )
    image.convert("1").save(str(Path("codes", f"{data}.png".replace("/", "-"))))


def get_all_instrument_numbers():
    at = Airtable(
        base_key=os.environ.get("AIRTABLE_BASE_KEY"), table_name="Instruments"
    )
    numbers = [
        item["fields"]["Number"]
        for item in at.get_all()
        if item["fields"].get("Number", False)
    ]
    with Pool(16) as p:
        p.map(generate_single_barcode, numbers)


if __name__ == "__main__":
    get_all_instrument_numbers()
