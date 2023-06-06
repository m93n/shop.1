from store.models import Category,Tag

def menu_link(request):
    links = Category.objects.all()

    return dict(links=links)

def populer_tags(requeset):
    tags = Tag.objects.all()

    return dict(tags=tags,)

