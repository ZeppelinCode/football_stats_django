from django.shortcuts import render
from matches.services import match_service as ms
from matches.services.util import get_page_range
from django.http import HttpRequest


def get_all_season_matches(request: HttpRequest):
    page = request.GET.get('page')
    matches, paginator = ms.get_all_matches_paginated(page)
    return render(
        request,
        'matches/season.html',
        {
            'matches': matches,
            'paginator': paginator,
            'page_range': get_page_range(page, paginator)
        }
    )


def get_upcomming_matches(request: HttpRequest):
    upcomming_matches = ms.get_upcomming_matches()
    return render(
        request,
        'matches/upcomming.html',
        {'matches': upcomming_matches}
    )
