from django.shortcuts import render
from django.http import JsonResponse
from .models import Book,Carousel,topCarousel
from BaseView.BaseView import BaseViewClass
from taggit.models import Tag
from django.http import HttpResponse
# Create your views here.


def concatDic(firstDic,SecondDic):
    for item in firstDic.keys():
        SecondDic[item] = firstDic[item]
    return SecondDic

def getBannerImage():
    return topCarousel.objects.all()

def makeCarsDic():
    carList = []
    cars = Carousel.objects.all()
    for item in cars:
        m = {}
        m['car'] = item
        m['books'] = item.books.all()[0:20]
        carList.append(m)
    return carList


class Home(BaseViewClass):
    bannerImages = getBannerImage()
    cars = makeCarsDic()
    context = {}
    templateName = 'mainPage/Main.html'
    def get(self,req):
        if req.session.get('help') == None:
            req.session['help'] = True
        self.context['carList'] = self.cars
        self.context['bannerImages'] = getBannerImage()
        return render(req,self.templateName,context=self.context)
    def post(self,req):
        if req.POST.get('help') != None:
            if req.POST.get('help') == 'false':
                try:
                    req.session['help'] = False
                except:
                    pass
            return JsonResponse({'stat':200})


class Index(BaseViewClass):
    values = {'ACS': 'صعودی', 'DEC': 'نزولی', 'name': 'نام کالا', 'wName': 'نام نویسنده', 'pName': 'نام ناشر',
                  'price': 'قیمت', 'likes': 'محبوبیت', 'date': 'تاریخ چاپ', 'sales': 'تعداد فروش'}
    hasProduct = False
    sortType = 'ACS'
    quanity = 20
    sortMethod = 'name'
    checkPro = False
    page = 1
    context = {}
    templateName = 'books/Index.html'
    def get(self,req,typeId,indexId,name):
        if typeId == 3:
            count = Carousel.objects.getBooksOnCar(indexId, orderMethod=self.sortMethod, orderType=self.sortType, available=self.checkPro).count()
        elif typeId == 4:
            try:
                tag = Tag.objects.get(id=indexId)
                count = Book.objects.getBookByCat(typeId, tag.id, self.sortMethod, self.sortType, self.checkPro).count()
            except:
                count = 0
        elif typeId in [0,1,2]:
            count = Book.objects.getBookByCat(typeId, indexId,self.sortMethod,self.sortType,self.checkPro).count()
        if len(req.GET) > 0:
            try:
                self.sortType = req.GET['sortType']
                self.sortMethod = req.GET['sortMethod']
                self.quanity = int(req.GET['quanity'])
                self.checkPro = req.GET['checkPro']
                try:
                    self.page = int(req.GET['page'])
                except:
                    self.page = 1
                if self.checkPro == 'true':
                    self.checkPro = True
                else:
                    self.checkPro = False
                if typeId == 3:
                    count = Carousel.objects.getBooksOnCar(indexId, orderMethod=self.sortMethod, orderType=self.sortType,
                                                           available=self.checkPro).count()
                else:
                    count = Book.objects.getBookByCat(typeId, indexId, self.sortMethod, self.sortType,self.checkPro).count()
            except:
                pass



        if count%self.quanity == 0:
            pages = int(count/self.quanity)
        else:
            pages = int(count/self.quanity)+1

        if self.page > pages:
            self.page = pages
        if self.page <=0 :
            self.page = 1

        if typeId == 3:
            books = Carousel.objects.getBooksOnCar(indexId,orderMethod=self.sortMethod,orderType=self.sortType,available=self.checkPro)[(self.page-1)*self.quanity:self.quanity*self.page]
        else:
            books = Book.objects.getBookByCat(typeId, indexId,self.sortMethod,self.sortType,self.checkPro)[(self.page-1)*self.quanity:self.quanity*self.page]
        if len(books) > 0:
            self.hasProduct=True
        else:
            name = 'ناشناس'
        start = self.page - 2
        if start <= 0:
            start = 1
        pagesList = range(start,pages+1)[0:5]
        newContext = {
                       'products':books,
                       'hasProduct':self.hasProduct,
                       'name':name,
                       'sortType':self.sortType,
                       'quanity':self.quanity,
                       'sortMethod':self.sortMethod,
                       'sortTypeVal':self.values[self.sortType],
                       'sortMethodVal':self.values[self.sortMethod],
                       'checkPro':self.checkPro,
                       'page':self.page,
                       'pages':pages,
                       'pagesList':pagesList,
                    }
        self.context = concatDic(self.context,newContext)
        return render(req,self.templateName,context=self.context)

class Detail(BaseViewClass):
    context = {}
    templateName = 'books/detail.html'
    def get(self,req,pId,name):
        book = Book.objects.get(id=pId)
        self.context['book'] = book
        return render(req, self.templateName, context=self.context)


