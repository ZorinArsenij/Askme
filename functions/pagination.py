from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def paginate(objects_list, current_page, elements_per_page = 5):
    paginator = Paginator(objects_list, elements_per_page)
    page = current_page
    try:
        objects_page = paginator.get_page(page)
    except PageNotAnInteger:
        objects_page = paginator.get_page(1)
    except EmptyPage:
        objects_page = paginator.get_page(paginator.num_pages)
    return objects_page, paginator