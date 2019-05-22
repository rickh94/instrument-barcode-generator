import os
from pathlib import Path

from PIL import Image

PAGE_WIDTH = 1125
PAGE_HEIGHT = 1500
ROWS_PER_PAGE = 20
PADDING_X = 20
PADDING_Y = 11
ROW_HEIGHT = 64


def get_next_image():
    for image in os.listdir("codes"):
        yield image


def image_width(image_path):
    im = Image.open(Path("codes", image_path))
    width, _ = im.size
    im.close()
    return width


def make_image_rows():
    total_width = 0
    row = []
    all_rows = []

    for image in get_next_image():
        if "png" not in image:
            continue
        im = Image.open(Path("codes", image))
        add_width = im.size[0] + PADDING_X
        if total_width + add_width >= PAGE_WIDTH:
            all_rows.append(make_row(row))
            total_width = 0
            row = []
        row.append(im)
        total_width += add_width
    if row:
        all_rows.append(make_row(row))
    return all_rows


def make_row(images):
    x_offset = 0
    new_im = Image.new("1", (PAGE_WIDTH, ROW_HEIGHT), color=1)
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0] + PADDING_X
        im.close()

    return new_im


def write_page(rows_in_page, page_number):
    page = Image.new("1", (PAGE_WIDTH, PAGE_HEIGHT), color=1)
    y_offset = 0
    for im in rows_in_page:
        page.paste(im, (0, y_offset))
        y_offset += ROW_HEIGHT + PADDING_Y
        im.close()
    page.save(Path('pages', f'page-{page_number}.png'))
    page.close()


def make_pages(rows):
    rows_in_page = []
    current_page = 0
    for row in rows:
        print(current_page)
        print(len(rows_in_page))
        if len(rows_in_page) + 1 > ROWS_PER_PAGE:
            write_page(rows_in_page, current_page)
            rows_in_page = []
            current_page += 1
        rows_in_page.append(row)

    if rows_in_page:
        write_page(rows_in_page, current_page)


# def make_lines():
#     this_line, start_next_line = make_image_row()
#     new_im = Image.new("1", (2400, 64), color=1)
#     x_offset = 0
#     for image_path in this_line:
#         im = Image.open(Path("codes", image_path))
#         new_im.paste(im, (x_offset, 0))
#         x_offset += im.size[0] + 20
#         im.close()
#     new_im.save(Path("lines", "test.png"))


if __name__ == "__main__":
    make_pages(make_image_rows())
