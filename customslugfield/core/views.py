from django.shortcuts import render, get_object_or_404

from .models import TestModel

# Create your views here.

def index_view(request):
    test_data = TestModel.objects.all()

    context = {
        "test_data": test_data
    }
    return render(request, "core/index.html", context)


def detail_view(request, slug):
    test_data = get_object_or_404(TestModel, slug=slug)

    context = {
        "test_data": test_data
    }
    return render(request, "core/detail.html", context)
