from dashboard.settings import DEBUG_MODE
import inspect, pprint
from django.shortcuts import render
from django.http import HttpResponse
from .init_db_app import init_db_sql
from django.views import View
#####################################################################################
#               Debug utils
#####################################################################################

def debug_info(self,*args,**kargs):
    if DEBUG_MODE:
        print(self.__class__.__name__)
        print(inspect.stack()[1].function)
        if args:
            for arg in args:
                print(arg)
        if kargs:
            pprint.pprint(kargs)
                


def page_not_found_fbv_view(request, exception=None):
    """
    View per gestire la pagina 404 (pagina non trovata).
    """
    return render(request, '404.html', status=404)



class InitDBView(View):
    def get(self, request=None):
        debug_info(self)
        print("******esecuzione script DB******")
        init_db_sql()
        message = """<p>Script lanciato ed eseguito con successo</p>"""
        return HttpResponse(message, status=200)