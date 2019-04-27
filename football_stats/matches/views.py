from django.shortcuts import render
from matches.services import match_service as ms
from matches.services.util import get_page_range
from django.http import HttpRequest

# Create your views here.


def get_all_season_matches(request: HttpRequest):
    page = request.GET.get('page')
    matches, paginator = ms.get_all_matches(page)
    return render(
        request,
        'matches/season.html',
        {
            'matches': matches,
            'paginator': paginator,
            'page_range': get_page_range(page, paginator)
        }
    )
