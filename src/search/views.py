from itertools import chain
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from blog.models import Post
from course.models import Course


class SearchView(TemplateView):
    template_name = "search.html"


class SearchResultsView(ListView):
    template_name = "results.html"
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["count"] = self.count or 0
        context["query"] = self.request.GET.get("q")
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get("q", None)

        if query is not None:
            blog_results = Post.objects.search(query)
            course_results = Course.objects.search(query)

            # combine querysets
            queryset_chain = chain(blog_results, course_results)
            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)  # since qs is actually a list
            return qs
        return Post.objects.none()  # just an empty queryset as default
