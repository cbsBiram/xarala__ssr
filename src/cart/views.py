from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from course.models import Course

# from course.recommender import Recommender
from coupons.forms import CouponApplyForm
from .cart import Cart
from .forms import CartAddCourseForm


def add_course_to_cart(request, course_slug):
    cart = Cart(request)
    course = get_object_or_404(Course, slug=course_slug)
    cart.add(course=course, quantity=1, override_quantity=False)
    return redirect("cart:cart_detail")


@require_POST
def cart_add(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    form = CartAddCourseForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            course=course, quantity=cd["quantity"], override_quantity=cd["override"]
        )
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    cart.remove(course)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item["update_quantity_form"] = CartAddCourseForm(
            initial={"quantity": item["quantity"], "override": True}
        )
    coupon_apply_form = CouponApplyForm()

    # r = Recommender()
    # cart_courses = [item["course"] for item in cart]
    # recommended_courses = r.suggest_courses_for(cart_courses, max_results=4)

    return render(
        request,
        "cart_detail.html",
        {
            "cart": cart,
            "coupon_apply_form": coupon_apply_form,
            # "recommended_courses": recommended_courses,
        },
    )
