from contextlib import contextmanager
import csv
import datetime
from decimal import Decimal, InvalidOperation
import logging
import os
import sys

log = logging.getLogger(__name__)

csv.field_size_limit(sys.maxsize)


def _wrap_row(r, headers):
    return dict(zip(headers, r))


@contextmanager
def _context_reader(source, skip=0, quotechar=None, quoting=csv.QUOTE_NONE):
    if not os.path.exists(source):
        raise ValueError("File not found: {}".format(source))

    with open(source, encoding='cp1252') as f:
        rows = csv.reader(
            f, delimiter='|', quotechar=quotechar, quoting=quoting)
        for i in range(skip):
            next(rows)

        headers = [h.lower() for h in next(rows)]

        yield (_wrap_row(r, headers) for r in rows)


def process_csv(source, process_row_callback):
    with _context_reader(
            source, quotechar='"', quoting=csv.QUOTE_MINIMAL) as rows:
        return [
            result for result in (
                process_row_callback(r) for r in rows) if result]


def parse_decimal(d):
    d = '0' if d == '' else d

    try:
        return Decimal(d.replace(',', '.'))
    except InvalidOperation:
        return Decimal()


def parse_datum(s):
    if not s or s == '0':
        return None

    return datetime.datetime.strptime(s, "%Y%m%d").date()


def parse_nummer(s):
    if not s:
        return None

    return int(s, 10)
