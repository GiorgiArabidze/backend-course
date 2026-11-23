from django.http import HttpResponse, Http404
from django.urls import reverse

PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 1800},
    {"id": 2, "name": "Headphones", "price": 150},
    {"id": 3, "name": "Mouse", "price": 40},
]


def home(request):
    link = reverse("product_list")
    return HttpResponse(f'<h1>myshop</h1><a href="{link}">პროდუქტები</a>')


def about(request):
    return HttpResponse(
        "<p>გამარჯობა! მე ვარ გიორგი. ვსწავლობ backend დეველოპმენტს "
        "და ეს ჩემი პირველი Django პროექტია.</p>"
    )


def product_list(request):
    items = "".join(
        f'<li><a href="{reverse("product_detail", args=[p["id"]])}">'
        f'{p["name"]}: {p["price"]} ₾</a></li>'
        for p in PRODUCTS
    )
    return HttpResponse(f"<ul>{items}</ul>")


def product_detail(request, pk):
    for p in PRODUCTS:
        if p["id"] == pk:
            return HttpResponse(f'<h1>{p["name"]}</h1><p>{p["price"]} ₾</p>')
    raise Http404("Product not found")
