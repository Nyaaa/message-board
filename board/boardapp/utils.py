from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import os
import urllib.parse
import uuid


@csrf_exempt  # FIXME
def upload_file(request, **kwargs):
    file_obj = request.FILES['file']
    file_ext = file_obj.name.split('.')[-1]
    filename = f'{uuid.uuid4()}.{file_ext}'
    full_filename = os.path.join(settings.MEDIA_ROOT, filename)
    with open(full_filename, 'wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)
    url = urllib.parse.urljoin(settings.MEDIA_URL, filename)
    return JsonResponse(data={'location': url})
