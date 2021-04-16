from .. import __version__


def debug(request):
    """
    Context processor to add the following variables available in our templates.
    - timezone offset of the user
    - debug variables
    - version information
    """
    from django.conf import settings

    return {
        "debug": settings.DEBUG,
        "debug_js": settings.DEBUG_JS,
        "VERSION": __version__,
        "tzoffset": request.COOKIES.get("tzoffset", None),
    }
