from django.db import models
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from taggit.managers import TaggableManager
from django.utils import timezone

taminKondandeOlaviat = {'Dakheli': 12, 'Gostaresh': 11, 'Ghoghuns': 10, 'Asar': 9, 'Bidgol': 7, 'GotenBerg': 6,
                        'Elias': 5, 'Kharazmi': 4,
                        'Jungle': 8, 'PaiamNur': 3, 'PezeshkiPasargad': 2, 'SimaieDanesh': 1}

# Create your models here.
fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'Statics'))
staticDir = os.path.join(settings.BASE_DIR,'Static')
defaultImagePathBook = '/Book/default.png'
defaultImagePathAuthor = '/Author/default.png'
defaultImagePathTranslator = '/Translator/default.png'
defaultImagePathPublisher = '/Publisher/default.png'

langs = {0:'فارسی',1:'انگلیسی',2:'غیره'}
ghats = {0:'رقعی',1:'وزیری',2:'وزیری جدید',3:'پالتویی',4:'رحلی',5:'خشتی',6:'جیبی'}
jelds = {0:'شومیز',1:'گالینگور',2:'سلفونی'}
status = {0:'دسته اصلی',1:'زیر دسته 1',2:'زیر دسته 2'}

class CategoriManager(models.Manager):
    def getAllCats(self):
        def reorderCats(lst):
            p = []
            for item in lst:
                if item['secondSubS'] == True:
                    p.append(item)
            for item in lst:
                if item not in p:
                    p.append(item)
            return p

        allMenus = []
        index = 0
        firstSub = self.filter(catStatus=0)
        for obj in firstSub:
            firstSubS = True
            secondSubS = True
            menu = []
            secondSub = obj.subCat.filter(catStatus=1)
            if len(secondSub) == 0:
                firstSubS = False
            else:
                firstSubS = True
            for obj2 in secondSub:
                thirdSub = obj2.subCat.filter(catStatus=2)
                if len(thirdSub) == 0:
                    secondSubS = False
                else:
                    secondSubS = True
                menu.append({'obj': obj2, 'thirdSubS': secondSubS, 'thirdSub': thirdSub})
            allMenus.append({'obj': obj, 'secondSubS': firstSubS, 'secondSub': menu})
        return reorderCats(allMenus)

class BookManager(models.Manager):
    def getBookByCat(self,catType,indexId,orderMethod=None,orderType=None,available=False):
        if catType == 0:
            books = self.filter(mainCat=indexId)
        elif catType == 1:
            books = self.filter(secondCat=indexId)
        elif catType == 2:
            books = self.filter(thirdCat=indexId)
        elif catType == 4:
            books = self.filter(tags__id__in=[indexId])

        if orderType and orderMethod :
            if available:
                return self.sortBy(orderMethod, orderType, books).filter(available = True)
            else:
                return self.sortBy(orderMethod, orderType, books)
        return books

    def sortBy(self,by,type,query):
        enum = {'name':'name','wName':'writer','pName':'publisher__name','price':'price','likes':'likes','date':'publishYear','sales':'sales'}
        if type == 'ACS':
            order = enum[by]
        elif type == 'DEC':
            order = '-' + enum[by]
        return query.order_by(order)



class Publisher(models.Model):
    name = models.CharField(null=False,verbose_name='نام',max_length=30)
    decs = models.CharField(max_length=200,verbose_name='توضیحات')
    publisherPic = models.ImageField(storage=fs, upload_to='Publisher', verbose_name='تصویر',default=defaultImagePathPublisher)
    def __str__(self):
        return self.name

class Author(models.Model):
    name =  models.CharField(primary_key=True,max_length=50,verbose_name='نام نوینده')
    decs = models.CharField(max_length=200,verbose_name='توضیحات')
    authorPic = models.ImageField(storage=fs, upload_to='Authors', verbose_name='تصویر',default=defaultImagePathAuthor)
    def __str__(self):
        return self.name

class Translator(models.Model):
    name = models.CharField(primary_key=True,max_length=50, verbose_name='نام مترجم')
    decs = models.CharField(max_length=200, verbose_name='توضیحات')
    translatorPic = models.ImageField(storage=fs, upload_to='Translator', verbose_name='تصویر', default=defaultImagePathTranslator)
    def __str__(self):
        return self.name


class Categori(models.Model):
    categoriName = models.CharField(verbose_name='نام',max_length=30)
    subCat = models.ManyToManyField(to='self',symmetrical=True,blank=True,verbose_name='زیر دسته ها')
    catStatus = models.SmallIntegerField(default=0,choices=((a,b) for a,b in status.items()),verbose_name='نوع دسته')
    object = CategoriManager()
    def __str__(self):
        return self.categoriName


class Book(models.Model):
    name = models.CharField(max_length=50,verbose_name='عنوان')
    subject = models.CharField(max_length=100,verbose_name='موضوع')
    code = models.CharField(max_length=13,blank=False,unique=True,null=False,verbose_name='شابک')
    publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE,verbose_name='ناشر')
    mainCat = models.ForeignKey(Categori,on_delete=models.SET_DEFAULT,default=1,related_name='main',verbose_name='نوع محصول')
    secondCat = models.ForeignKey(Categori,on_delete=models.SET_NULL,blank=True,null=True,related_name='second',verbose_name='دسته فرعی')
    thirdCat= models.ForeignKey(Categori,on_delete=models.SET_NULL,blank=True,null=True,related_name='third',verbose_name='دسته فرعی دوم')
    description = models.CharField(max_length=200,verbose_name='توضیحات',blank=True,null=True)
    writer = models.ForeignKey(Author,on_delete=models.CASCADE,verbose_name='نویسنده',blank=True,null=True)
    translator = models.ForeignKey(Translator,on_delete=models.CASCADE,verbose_name='مترجم',blank=True,null=True)
    image = models.ImageField(storage=fs, upload_to='Books', verbose_name='تصویر',default=defaultImagePathBook)
    #tamin konande ha
    Dakheli = models.CharField(max_length=20,verbose_name='داخلی',default='NULL',blank=True)
    Gostaresh = models.CharField(max_length=20,verbose_name='گسترش',default='NULL',blank=True)
    Ghoghnus = models.CharField(max_length=20,verbose_name='ققنوس',default='NULL',blank=True)
    Asar = models.CharField(max_length=20,verbose_name='اثار',default='NULL',blank=True)
    GitaMehr = models.CharField(max_length=20,verbose_name='گیتا مهر',default='NULL',blank=True)
    Elias = models.CharField(max_length=20,verbose_name='الیاس',default='NULL',blank=True)
    PezeshkiPasargad = models.CharField(max_length=20,verbose_name='پاسارگاد',default='NULL',blank=True)
    PaiamNur = models.CharField(max_length=20,verbose_name='پیام نور',default='NULL',blank=True)
    Jungle = models.CharField(max_length=20,verbose_name='جنگل',default='NULL',blank=True)
    Bidgol = models.CharField(max_length=20,verbose_name='بیدگل',default='NULL',blank=True)
    GotenBerg = models.CharField(max_length=20,verbose_name='گتنبرگ',default='NULL',blank=True)
    Kharazmi = models.CharField(max_length=20,verbose_name='خوارزمی',default='NULL',blank=True)
    SimaieDanesh = models.CharField(max_length=20,verbose_name='سیمای دانش',default='NULL',blank=True)
    #---------------------------
    inventory = models.BooleanField(default=False,verbose_name='موجودی')
    price = models.DecimalField(decimal_places=0,max_digits=6,verbose_name='قیمت')
    printNumber = models.IntegerField(blank=True,null=True,verbose_name='نوبت چاپ')
    publishYear = models.CharField(max_length=4,blank=True,null=True,verbose_name='سال چاپ')
    created_time = models.DateField(editable=False)
    updated_time = models.DateField(editable=False)
    language = models.SmallIntegerField(default=0,choices=((a,b) for a,b in langs.items()),verbose_name='زبان کتاب')
    ghat = models.SmallIntegerField(default=0,choices=((a,b) for a,b in ghats.items()),verbose_name='قطع')
    jeld = models.SmallIntegerField(default=0,choices=((a,b) for a,b in jelds.items()),verbose_name='نوع جلد')
    pages = models.DecimalField(max_digits=4,decimal_places=0,verbose_name='تعداد صفحه',blank=True,null=True)
    weight = models.DecimalField(max_digits=5,decimal_places=0,verbose_name='وزن',null=True,blank=True)
    likes = models.IntegerField(default=0,verbose_name='پسندیدم ها')
    dilikes = models.IntegerField(default=0, verbose_name='نپسندیدم ها')
    views = models.DecimalField(default=0,max_digits=4,decimal_places=0,verbose_name='بازدید')
    discount = models.DecimalField(default=0,max_digits=3,decimal_places=0,verbose_name='تخفیف')
    sales = models.DecimalField(default=0,max_digits=4,decimal_places=0,verbose_name='تعداد فروش',editable=False)
    available = models.BooleanField(default=True,verbose_name='قابل خرید')
    visiblity = models.BooleanField(default=True,verbose_name='نمایش')
    stock = models.DecimalField(default=4,max_digits=2,decimal_places=0,verbose_name='قابل خرید')
    tags = TaggableManager()
    objects = BookManager()

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        if not self.id:
            self.created_time = timezone.now()
        self.updated_time = timezone.now()
        return super(Book, self).save(*args, **kwargs)

    def getTaminKonande(self):
        all = {'Dakheli': self.Dakheli, 'Gostaresh': self.Gostaresh, 'Ghoghuns': self.Ghoghnus, 'Asar': self.Asar,
               'Bidgol': self.Bidgol, 'GotenBerg': self.GotenBerg,
                        'Elias': self.Elias, 'Kharazmi': self.Kharazmi,
                        'Jungle': self.Jungle, 'PaiamNur': self.PaiamNur, 'PezeshkiPasargad': self.PezeshkiPasargad,
               'SimaieDanesh': self.SimaieDanesh}
        taminkonande = ''
        max = -1
        if self.inventory == True:
            for key in all.keys():
                if all[key] != 'NULL':
                    newMax = taminKondandeOlaviat[key]
                    if max < newMax:
                        max = newMax
                        taminkonande = key
            if max != -1:
                return self.__dict__[taminkonande]
        else:
            return 'NULL'

    def getRealPrice(self):
        return int(self.price)

    def calculatePriceWithDiscount(self): #book price with discount
        if self.discount > 0:
            dis = (int(self.discount)/100)*int(self.price)
            return {'stat':True,'price':int(int(self.price)-dis)}
        return {'stat':False,'price':self.price}

    def getBookDiscount(self): #discount of a book
        if self.discount > 0:
            return (int(self.discount)/100)*int(self.price)
        return 0


class CarouselManager(models.Manager):
    def getBooksOnCar(self,indexId,quanity=None,orderMethod=None,orderType=None,available=False):
        try:
            car = self.get(id=indexId)
        except:
            return self.none()
        if quanity != None:
            books = car.books.all()[0:quanity]
        else:
            books =  car.books.all()
        if orderType and orderMethod :
            if available:
                return self.sortBy(orderMethod, orderType, books).filter(available = True)
            else:
                return self.sortBy(orderMethod, orderType, books)
        return books


    def sortBy(self,by,type,query):
        enum = {'name':'name','wName':'writer','pName':'publisher__name','price':'price','likes':'likes','date':'publishYear','sales':'sales'}
        if type == 'ACS':
            order = enum[by]
        elif type == 'DEC':
            order = '-' + enum[by]
        return query.order_by(order)


class Carousel(models.Model):
    books = models.ManyToManyField(Book,verbose_name='کتاب ها')
    name = models.CharField(max_length=20,verbose_name='نام')
    objects = CarouselManager()
    def __str__(self):
        return self.name

class Banner(models.Model):
    image = models.ImageField(storage=fs,upload_to='Banner',verbose_name='تصویر')
    description = models.CharField(blank=True,null=True,verbose_name='توضیحات',max_length=100)
    link = models.GenericIPAddressField(verbose_name='لینک')

    def __str__(self):
        return str(self.link)

class topCarousel(models.Model):
    image = models.ImageField(storage=fs,upload_to='Banner',verbose_name='تصویر')
    active = models.BooleanField(default=False)
