from typing import Generator, Union, Optional
from django.core.paginator import Paginator


def get_page_range(s_page: Optional[str], paginator: Paginator):
    num_pages = paginator.paginator.num_pages
    if num_pages < 10:
        return range(1, num_pages + 1)

    page = None
    try:
        page = int(s_page)
    except Exception:
        print('page conversion error')

    if page is None:
        page = 1
    return truncated_page_range(page, paginator)


def truncated_page_range(page: int, paginator: Paginator):
    num_pages = paginator.paginator.num_pages
    if not paginator.has_previous() or page <= 4:
        for i in range(1, 7):
            yield i
        yield '..'
        yield num_pages
        return

    if not paginator.has_next() or page > num_pages - 4:
        yield 1
        yield '..'
        for i in range(num_pages - 4, num_pages):
            yield i
        return

    yield 1
    yield '..'
    for i in range(page-3, page+4):
        yield i

    yield '..'
    yield num_pages

# https://www.openligadb.de/api/getmatchdata/bl1/2018/30
# https://www.openligadb.de/api/getlastchangedate/bl1/2018/31
