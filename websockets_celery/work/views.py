import logging

from django.shortcuts import render
from django.http import JsonResponse

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from work.tasks import get_picture_average_color


logger = logging.getLogger(__name__)


def work_page(request, name):
    publisher = RedisPublisher(facility='work-page', broadcast=True)
    publisher.publish_message(RedisMessage(
        'JOINED CHAT: {}'.format(name)))

    return render(request, 'work/greeting.html', {})


def average_color(request):
    """Return a response with color codes for each URL received

    Query params:
        - url: a list of URLs as a comma separated value
        - user: the user that is making the request

    # TODO: make this run through celery and post success messages through websocket
    """
    user = request.GET['user']
    urls = request.GET['url'].split(',')
    urls = filter(lambda url: url.strip(), urls)

    response_dict = {}
    try:
        for url in urls:
            color_code = get_picture_average_color(url)
            response_dict[url] = color_code
    except Exception as e:
        logger.exception('Could not get average color.')
        return JsonResponse(
            {'error': 'You got an exception: {}'.format(type(e))},
            status=500
        )

    return JsonResponse(response_dict)
