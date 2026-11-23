import random
from collections import Counter

from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

RECIPES = [
    {"id": 1, "slug": "khinkali", "name": "ხინკალი", "category": "main",
     "minutes": 90, "vegetarian": False,
     "ingredients": ["ფქვილი", "საქონლის ხორცი", "ღორის ხორცი",
                     "ხახვი", "კვლიავი"]},
    {"id": 2, "slug": "khachapuri", "name": "ხაჭაპური", "category": "bakery",
     "minutes": 60, "vegetarian": True,
     "ingredients": ["ფქვილი", "იმერული ყველი", "კვერცხი", "კარაქი"]},
    {"id": 3, "slug": "lobiani", "name": "ლობიანი", "category": "bakery",
     "minutes": 75, "vegetarian": True,
     "ingredients": ["ფქვილი", "ლობიო", "ხახვი", "კარაქი"]},
    {"id": 4, "slug": "pkhali", "name": "ფხალი", "category": "snack",
     "minutes": 30, "vegetarian": True,
     "ingredients": ["ისპანახი", "ნიგოზი", "ნიორი", "ქინძი"]},
    {"id": 5, "slug": "churchkhela", "name": "ჩურჩხელა", "category": "dessert",
     "minutes": 240, "vegetarian": True,
     "ingredients": ["ნიგოზი", "ყურძნის წვენი", "ფქვილი"]},
    {"id": 6, "slug": "chakapuli", "name": "ჩაქაფული", "category": "main",
     "minutes": 120, "vegetarian": False,
     "ingredients": ["ცხვრის ხორცი", "ტყემალი", "ტარხუნა", "თეთრი ღვინო"]},
]


def page(title, body):
    return HttpResponse(
        f"<h1>{title}</h1>{body}<hr><a href='/recipes/'>← ყველა რეცეპტი</a>"
    )


def find_recipe(pk):
    for r in RECIPES:
        if r["id"] == pk:
            return r
    return None


def recipe_list_html(recipes):
    items = "".join(
        f"<li><a href='{reverse('recipes:detail', args=[r['id']])}'>{r['name']}</a>"
        f" · {r['minutes']} წთ</li>"
        for r in recipes
    )
    return f"<ul>{items}</ul>"


def recipe_page(recipe):
    ingredients = "".join(f"<li>{i}</li>" for i in recipe["ingredients"])
    veg = "დიახ" if recipe["vegetarian"] else "არა"
    body = (
        f"<p>მომზადების დრო: {recipe['minutes']} წთ</p>"
        f"<p>კატეგორია: {recipe['category']}</p>"
        f"<p>ვეგეტარიანული: {veg}</p>"
        f"<h3>ინგრედიენტები</h3><ul>{ingredients}</ul>"
    )
    return page(recipe["name"], body)


def recipe_list(request):
    recipes = RECIPES

    category = request.GET.get("category")
    max_time = request.GET.get("max_time")
    vegetarian = request.GET.get("vegetarian")

    if category:
        recipes = [r for r in recipes if r["category"] == category]

    if max_time:
        try:
            limit = int(max_time)
            recipes = [r for r in recipes if r["minutes"] <= limit]
        except ValueError:
            pass

    if vegetarian == "yes":
        recipes = [r for r in recipes if r["vegetarian"]]

    if not recipes:
        return page("რეცეპტები", "<p>ვერაფერი მოიძებნა</p>")
    return page("რეცეპტები", recipe_list_html(recipes))


def recipe_detail(request, pk):
    recipe = find_recipe(pk)
    if recipe is None:
        raise Http404("რეცეპტი ვერ მოიძებნა")
    return recipe_page(recipe)


def category_detail(request, name):
    recipes = [r for r in RECIPES if r["category"] == name]
    if not recipes:
        raise Http404("კატეგორია ვერ მოიძებნა")
    return page(f"კატეგორია: {name}", recipe_list_html(recipes))


def search(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return page("ძებნა", "<p>ჩაწერე საძიებო სიტყვა</p>")
    found = [r for r in RECIPES if any(q in ing for ing in r["ingredients"])]
    if not found:
        return page(f"ძებნა: {q}", "<p>ვერაფერი მოიძებნა</p>")
    return page(f"ძებნა: {q}", recipe_list_html(found))


def recipe_by_slug(request, slug):
    for r in RECIPES:
        if r["slug"] == slug:
            return recipe_page(r)
    raise Http404("რეცეპტი ვერ მოიძებნა")


def random_recipe(request):
    recipe = random.choice(RECIPES)
    return redirect("recipes:detail", pk=recipe["id"])


def stats(request):
    data = {
        "count": len(RECIPES),
        "categories": dict(Counter(r["category"] for r in RECIPES)),
        "avg_minutes": sum(r["minutes"] for r in RECIPES) / len(RECIPES),
    }
    return JsonResponse(data, json_dumps_params={"ensure_ascii": False})
