import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','prjbrji.settings')
import django
import random,json
django.setup()
from books.models import Categori,Publisher,Book

from faker import Faker
fake = Faker()

dt = json.load()

mainCatsCount = Categori.object.filter(catStatus=0).count()
secondCatsCount = Categori.object.filter(catStatus=1).count()
thirdCatsCount = Categori.object.filter(catStatus=2).count()
publishersCount = Publisher.objects.count()

# def PublisherMaker():
#     for i in range(1,10):
#         new = Publisher(name=fake.name())
#         new.save()

def makeBook(number):
    allBook = []
    for i in range(0,number):
        name = fake.name()
        code = fake.isbn13()
        publisher = Publisher.objects.all()[random.randrange(0,publishersCount)]
        mainCat = Categori.object.filter(catStatus=0)[random.randrange(0,mainCatsCount)]
        secondCat = Categori.object.filter(catStatus=1)[random.randrange(0,secondCatsCount)]
        thirdCat = Categori.object.filter(catStatus=2)[random.randrange(0,thirdCatsCount)]
        description = fake.text()
        writer = fake.name()
        translator = fake.name()
        price = random.randrange(10000,30001)
        printNumber = random.randrange(1,11)
        publishYear = fake.past_datetime(start_date="-30d", tzinfo=None)
        pages = random.randrange(100,501)
        weight = random.randrange(100,501)
        available = random.randrange(0,2)
        stock = random.randrange(1,101)
        new = Book(name=name,code=code,publisher=publisher,mainCat=mainCat,secondCat=secondCat,thirdCat=thirdCat,
                   description=description,writer=writer,translator=translator,price=price,printNumber=printNumber,
                   publishYear=publishYear,pages=pages,weight=weight,available=available,stock=stock)
        allBook.append(new)
        print(str(i) + 'saved')
    return allBook

if __name__=='__main__':
    mainCatsCount = Book.object.all().count()
    # print()
    books = makeBook(20000)
    Book.objects.bulk_create(books)

