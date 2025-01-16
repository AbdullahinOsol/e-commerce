from .models import Category

def store(request):
    categories = Category.objects.all()

    return {'categories': categories}