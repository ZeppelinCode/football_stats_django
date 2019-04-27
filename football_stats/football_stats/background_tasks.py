from background_task.models import Task
from matches.services.background_match_service import (
    update_matches_if_necessary)


def poll_for_mach_data():
    if not Task.objects.filter(verbose_name='poll_for_mach_data').exists():
        update_matches_if_necessary(repeat=Task.HOURLY, repeat_until=None,
                                    verbose_name='poll_for_mach_data')
