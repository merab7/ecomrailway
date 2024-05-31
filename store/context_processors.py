from .models import Category
from .quantity import Quantity


#creating context processor.py and here i am creating function that will get all the categories from the model category and this
#data will be available for every template file in project by registering this function in setting.
def category_names(request):
    return {'categories':Category.objects.all()}

def quantity_proc(request):
    return{'quantities': Quantity(request)}