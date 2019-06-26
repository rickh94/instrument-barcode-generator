import os
import glob
from pathlib import Path

from PIL import Image

PIXELS_PER_IN = 300


def in_to_px(inches):
    return int(inches * PIXELS_PER_IN)


PAGE_WIDTH_IN = 8.5
PAGE_HEIGHT_IN = 11
PAGE_WIDTH_PX = in_to_px(PAGE_WIDTH_IN)
PAGE_HEIGHT_PX = in_to_px(PAGE_HEIGHT_IN)

# PADDING_X = 20
# PADDING_Y = 11
# ROW_HEIGHT = 64
LABEL_WIDTH_IN = 2
LABEL_HEIGHT_IN = 3
LABEL_WIDTH_PX = in_to_px(LABEL_WIDTH_IN)
LABEL_HEIGHT_PX = in_to_px(LABEL_HEIGHT_IN)

LABELS_PER_ROW = int(PAGE_WIDTH_IN / LABEL_WIDTH_IN)
ROWS_PER_PAGE = int(PAGE_HEIGHT_IN / LABEL_HEIGHT_IN)


def get_next_image():
    for image in sorted(glob.glob("codes/*.png")):
        yield make_label(image)


def image_width(image_path):
    im = Image.open(Path("codes", image_path))
    width, _ = im.size
    im.close()
    return width


def make_image_rows():
    total_width = 0
    row = []
    all_rows = []

    for im in get_next_image():
        im.save("test.png")
        if len(row) == LABELS_PER_ROW:
            all_rows.append(make_row(row))
            row = []
        row.append(im)
    if row:
        all_rows.append(make_row(row))

    return all_rows


def make_row(images):
    x_offset = in_to_px(0.12)
    new_im = Image.new("RGB", (PAGE_WIDTH_PX, LABEL_HEIGHT_PX), color="#ffffff")
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.width + in_to_px(0.12)
        # im.close()

    # new_im.save('test.png')
    return new_im


def write_page(rows_in_page, page_number):
    page = Image.new("RGB", (PAGE_WIDTH_PX, PAGE_HEIGHT_PX), color="#ffffff")
    y_offset = in_to_px(0.5)
    for im in rows_in_page:
        page.paste(im, (0, y_offset))
        y_offset += LABEL_HEIGHT_PX + in_to_px(0.4)
        im.close()
    page.save(Path("pages", f"page-{page_number}.png"))
    page.close()


def make_pages(rows):
    rows_in_page = []
    current_page = 0
    for row in rows:
        if len(rows_in_page) == ROWS_PER_PAGE:
            write_page(rows_in_page, current_page)
            rows_in_page = []
            current_page += 1
        rows_in_page.append(row)

    if rows_in_page:
        write_page(rows_in_page, current_page)


def make_label(filename):
    new_im = Image.new("RGB", (LABEL_WIDTH_PX, LABEL_HEIGHT_PX), color="#ffffff")
    property_of_tmm = Image.open("./property-of-tmm-image.png")
    file_path = Path(filename)
    basename = file_path.name
    # percent = LABEL_WIDTH * 0.8 / property_of_tmm.width
    # new_height = int(property_of_tmm.height * percent)
    # property_of_tmm = property_of_tmm.resize((LABEL_WIDTH, new_height))
    # property_x_offset = (LABEL_WIDTH - property_of_tmm.width) // 2
    code = Image.open(file_path)
    y_offset = property_of_tmm.height + 15
    x_offset = int((new_im.width - code.width) / 2)
    new_im.paste(property_of_tmm, (0, 0))
    new_im.paste(code, (x_offset, y_offset))
    return new_im


if __name__ == "__main__":
    # for image in get_next_image():
    #     make_label(image)
    make_pages(make_image_rows())
