from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from .... import __version__


class Command(BaseCommand):

    help = """
       This command exports data in a spreadsheet. It is only available only
       from the user interface.

       TODO implement a command line version of this command. Also unify that
       command with the view function that is serving the spreadsheet from the
       user interface.
       """

    def get_version(self):
        return __version__

    requires_system_checks = False
    title = _("Export a spreadsheet")
    index = 1000
    help_url = "command-reference.html#exportworkbook"

    @staticmethod
    def getHTML(request):
        return render_to_string("commands/exportworkbook.html", request=request)
