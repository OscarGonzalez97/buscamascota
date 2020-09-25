from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'FONTAWESOME_KIT': settings.FONTAWESOME_KIT
    }