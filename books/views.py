from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import forms
from . import models
from django.contrib import messages
from datetime import datetime
from django.utils import timezone

# Create your views here.
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView


class DetailPostView(DetailView):
    model = models.Post
    pk_url_kwarg = "id"
    template_name = "post_details.html"

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object  # post model er object ekhane store korlam
        comments = post.comments.all()
        comment_form = forms.CommentForm()

        context["comments"] = comments
        context["comment_form"] = comment_form
        return context


all_purchases_info = []


@login_required
def purchase_car(request, id):
    global all_purchases_info
    car = models.Post.objects.get(pk=id)
    if car.quantity > 0:
        car.quantity -= 1
        car.save()
        messages.success(request, "Purchase successful!")
        purchase_time = timezone.now()

        # Create a dictionary containing the purchased car's information
        purchased_car_info = {
            "name": car.title,
            "purchase_time": purchase_time,
        }
        all_purchases_info.append(purchased_car_info)

        # Pass the purchased car's information to the HTML page
        return render(
            request,
            "order_history.html",
            {"all_purchases_info": all_purchases_info},
        )
    else:
        messages.error(request, "No more cars available!")
        return redirect("homepage")
