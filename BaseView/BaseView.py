from django.views import View
from books.models import Categori
from methods.getCardCount import getItemsCount


class BaseViewClass(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.context['menu'] = Categori.object.getAllCats()
            self.context['count'] = getItemsCount(request)
            return self.get(request,*args,**kwargs)
        else:
            return self.post(request,*args,**kwargs)