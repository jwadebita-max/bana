from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import FoodItem


def all(request):
    query = request.GET.get('q')
    if query:
        data = FoodItem.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        data = FoodItem.objects.all()

    context = {'data': data, 'query': query}
    return render(request, 'pages/all.html', context)


def pastries(request):
    query = request.GET.get('q')
    if query:
        data = FoodItem.objects.filter(
            Q(category='Pastries') &
            (Q(name__icontains=query) | Q(description__icontains=query))
        )
    else:
        data = FoodItem.objects.filter(category='Pastries')

    context = {'data': data, 'query': query}
    return render(request, 'pages/pastries.html', context)


def salad(request):
    query = request.GET.get('q')
    if query:
        data = FoodItem.objects.filter(
            Q(category='Salad') &
            (Q(name__icontains=query) | Q(description__icontains=query))
        )
    else:
        data = FoodItem.objects.filter(category='Salad')

    context = {'data': data, 'query': query}
    return render(request, 'pages/salad.html', context)


def FastFood(request):
    query = request.GET.get('q')
    if query:
        data = FoodItem.objects.filter(
            Q(category='Fast Food') &
            (Q(name__icontains=query) | Q(description__icontains=query))
        )
    else:
        data = FoodItem.objects.filter(category='Fast Food')

    context = {'data': data, 'query': query}
    return render(request, 'pages/FastFood.html', context)


def MainCourses(request):
    query = request.GET.get('q')
    if query:
        data = FoodItem.objects.filter(
            Q(category='Main courses') &
            (Q(name__icontains=query) | Q(description__icontains=query))
        )
    else:
        data = FoodItem.objects.filter(category='Main courses')

    context = {'data': data, 'query': query}
    return render(request, 'pages/MainCourses.html', context)


def soups(request):
    query = request.GET.get('q')
    if query:
        data = FoodItem.objects.filter(
            Q(category='Soups') &
            (Q(name__icontains=query) | Q(description__icontains=query))
        )
    else:
        data = FoodItem.objects.filter(category='Soups')

    context = {'data': data, 'query': query}
    return render(request, 'pages/soups.html', context)


def drinks(request):
    query = request.GET.get('q')
    if query:
        data = FoodItem.objects.filter(
            Q(category='Drinks') &
            (Q(name__icontains=query) | Q(description__icontains=query))
        )
    else:
        data = FoodItem.objects.filter(category='Drinks')

    context = {'data': data, 'query': query}
    return render(request, 'pages/drinks.html', context)


def product_detail(request, pk):
    product = get_object_or_404(FoodItem, pk=pk)
    related_products = FoodItem.objects.filter(category=product.category).exclude(pk=pk)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'pages/product_detail.html', context)