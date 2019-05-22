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
            "inkspread": "0.4",
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


def get_new_instrument_numbers():
    numbers = []
    for prefix in [
        1,
        2,
        3,
        4,
        8,
        "C1",
        "C2",
        "C3",
        "C4",
        "V13",
        "V14",
        "V15",
        "V16",
        "V17",
    ]:
        numbers.extend(generate_twenty_more(prefix))
    with Pool(16) as p:
        p.map(generate_single_barcode, numbers)


def generate_twenty_more(prefix):
    return [f"{prefix}-{i}" for i in range(501, 521)]


if __name__ == "__main__":
    get_new_instrument_numbers()
    # get_all_instrument_numbers()
