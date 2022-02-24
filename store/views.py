from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery, Like
from category.models import Category
from carts.models import CartItem
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")
        paginator = Paginator(products, 3)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        "products": paged_products,
        "product_count": product_count,
    }
    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product
        ).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(
                user=request.user, product_id=single_product.id
            ).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(
        product_id=single_product.id, status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(
        product_id=single_product.id)

    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "orderproduct": orderproduct,
        "reviews": reviews,
        "product_gallery": product_gallery,
    }
    return render(request, "store/product_detail.html", context)


def search(request):
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            products = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(
                    product_name__icontains=keyword)
            )
            product_count = products.count()
    context = {
        "products": products,
        "product_count": product_count,
    }
    return render(request, "store/store.html", context)


def submit_review(request, product_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id
            )
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(
                request, "Thank you! Your review has been updated.")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(
                    request, "Thank you! Your review has been submitted.")
                return redirect(url)


## TESTING LIKE / UNLIKE FUNCTIONALITY ##
@login_required
def liked_product(request, id):
    print(request.user)
    user = request.user

    if request.method == "POST":
        product_id = request.POST['product_id']
        get_product = get_object_or_404(Product, id=product_id)
        if get_product:
            like = Like.objects.filter(product=get_product)
            # likes exist for this product
            if like:
                print('like exist: ', like)
                print('checking if user is in this list of likes...')
                if user.userprofile in like[0].likes.all():
                    print('USER HAS ALREADY LIKED PRODUCT')
                    data = {
                        # "liked": like[0],
                        "likes_count": like[0].likes.all().count()
                    }
                    return JsonResponse(data, safe=False)
                else:
                    print('user has not liked product. will like now')
                    like[0].likes.add(user.userprofile)
                    like[0].save()
                    print(f'new likes like: {like[0].likes.all()}')
                    data = {
                        # "liked": like[0],
                        "likes_count": like[0].likes.all().count()
                    }
                    return JsonResponse(data, safe=False)
                    ''' return redirect(reverse("product_detail", args=[str(id)])) '''
            else:  # first like
                print('like does not exist for this item')
                new_like = Like.objects.create(product=get_product)
                new_like.likes.add(user.userprofile)
                new_like.save()
                print(new_like.likes.all())
                data = {
                    # "liked": new_like,
                    "likes_count": get_product.likes.all().count()
                }
                return JsonResponse(data, safe=False)
        # if user in get_product.likes.all():
        #     get_product.likes.remove(user)
        #     Likes = False
        # else:
        #     get_product.likes.add(user)
        #     Likes = True
        data = {
            "msg": "product does not exist"
            # "liked": Likes,
            # "likes_count": get_product.likes.all().count()
        }
        ''' return JsonResponse(data, safe=False) '''
        return redirect(reverse("product_detail", args=[str(id)]))


@login_required
def disliked_product(request, id):
    user = request.user

    if request.method == "POST":
        product_id = request.POST['product_id']
        get_product = get_object_or_404(Product, id=product_id)
        if get_product:
            dislike = Like.objects.filter(product=get_product)
        # dislikes exist for this product
        if dislike:
            print('dislike exist: ', dislike)
            print('checking if user is in this list of dislikes...')
            if user.userprofile in dislike[0].likes.all():
                print('USER HAS ALREADY DISLIKED PRODUCT')
                data = {
                    # "disliked": dislike[0],
                    "dislikes_count": dislike[0].dislikes.all().count()
                }
                return JsonResponse(data, safe=False)
            else:
                print('user has not disliked product. will dislike now')
                dislike[0].dislikes.add(user.userprofile)
                dislike[0].save()
                print(f'new dislikes like: {dislike[0].likes.all()}')
                data = {
                    # "disliked": dislike[0],
                    "dislikes_count": dislike[0].dislikes.all().count()
                }
                return JsonResponse(data, safe=False)
                ''' return redirect(reverse("product_detail", args=[str(id)])) '''
        else:  # first dislike
            print('dislike does not exist for this item')
            new_dislike = Like.objects.create(product=get_product)
            new_dislike.dislikes.add(user.userprofile)
            new_dislike.save()
            print(new_dislike.likes.all())
            data = {
                # "disliked": new_dislike,
                "dislikes_count": get_product.dislikes.all().count()
            }
            return JsonResponse(data, safe=False)

    return redirect(reverse("product_detail", args=[str(id)]))
## -------------------------------------------------------------------------------------------- ##
