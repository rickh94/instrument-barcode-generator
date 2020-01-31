import os
import shutil

import treepoem
from pathlib import Path
from multiprocessing import Pool
import click
from datetime import datetime


@click.command()
@click.argument("prefix")
@click.argument("first", type=int)
@click.argument("last", type=int)
@click.option("--rm", is_flag=True)
def generate(prefix, first, last, rm):
    if rm:
        shutil.rmtree("codes")
        os.mkdir("codes")
    numbers = [f"{prefix}-{num}" for num in range(first, last + 1)]
    with Pool(4) as p:
        p.map(generate_single_barcode, numbers)


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
    width = 300
    percent = float(width / image.width)
    height = int(image.height * percent)
    image = image.resize((width, height))
    image.convert("1").save(str(Path("codes", f"{data}.png".replace("/", "-"))))


if __name__ == "__main__":
    generate()
