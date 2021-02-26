from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from blog.forms import CreatePostForm, UpdatePostForm
from blog.models import Post
from django.views.generic import ListView
from django.shortcuts import redirect, render
from userlogs.models import UserLog


@login_required
def dashboard_view(request):
    user = request.user
    if user.is_student:
        return redirect("dashboard:student")
    if user.is_teacher and user.is_staff:
        return redirect("dashboard:staff")
    if user.is_teacher and not user.is_staff:
        return redirect("dashboard:instructor")
    else:
        return redirect("oauth-new-password")


@method_decorator([login_required], name="dispatch")
class TutorialListView(ListView):
    template_name = "tutorials.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        user = self.request.user
        tutorials = Post.objects.filter(author=user).order_by("-publish_date")
        context = {"tutorials": tutorials, "user": user}
        return render(request, self.template_name, context)


@method_decorator([login_required], name="dispatch")
class TutorialCreateView(CreateView):
    form_class = CreatePostForm
    template_name = "instructor/create-tutorial.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        user = self.request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()
            UserLog.objects.create(
                action=f"Created {post.title} post", user_type="Writer", user=user
            )
            return redirect("dashboard:tutorials")

        return render(request, self.template_name, {"form": form})


@method_decorator([login_required], name="dispatch")
class TutorialDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("dashboard:tutorials")


@method_decorator([login_required], name="dispatch")
class TutorialUpdateView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = "instructor/edit-tutorial.html"


@login_required
def publish_tutorial(request):
    user = request.user
    values = {"error": "", "has_error": 0}
    tutorial_id = int(request.POST.get("id"))
    try:
        tutorial = Post.objects.get(pk=tutorial_id, author=user)
        if not tutorial.submitted and not tutorial.published:
            tutorial.submitted = True
        elif tutorial.submitted:
            tutorial.published = True
        tutorial.save()
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
        print(e)
    return JsonResponse(values)
