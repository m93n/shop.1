from store.models import Category,Tag

def menu_link(request):
    links = Category.objects.all()
    tags = Tag.objects.all()

    return dict(links=links, tags=tags)