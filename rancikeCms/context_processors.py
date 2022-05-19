from QuestionPaper.models import Paper


def total_items_in_cart(request):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Paper.objects.filter(user=request.user))
    return {'total_items' : total_items}