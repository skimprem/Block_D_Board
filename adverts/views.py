from django.shortcuts import render, redirect
from adverts.models import Advert, Feedback, AdvertFeedback
from django.views.generic import ListView, DetailView, CreateView
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from adverts.forms import AdvertForm, FeedbackForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from adverts.tasks import feedback_pub_notification, advert_pub_notification, feedback_del_notification, feedback_acc_notification, feedback_rej_notification
from adverts.filters import FeedbackFilter

class AdvertList(ListView):
    model = Advert
    ordering = 'pub_time'
    template_name = 'adverts/adverts.html'
    context_object_name = 'adverts'
    paginate_by = 10

class AdvertDetail(DetailView):
    model = Advert
    template_name = 'adverts/advert.html'
    context_object_name = 'advert'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'advert-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'advert-{self.kwargs["pk"]}', obj)

        return obj

class AdvertCreate(
    # PermissionRequiredMixin
    LoginRequiredMixin,
    CreateView):
    form_class = AdvertForm
    model = Advert
    template_name = 'adverts/create.html'
    def form_valid(self, form):
        advert = form.save(commit=False)
        advert.user = User.objects.get(pk=self.request.user.pk)
        advert.save()
        advert_pub_notification.apply_async([advert.pk])
        return redirect('/')


class FeedbackCreate(
    # PermissionRequiredMixin
    LoginRequiredMixin,
    CreateView):
    form_class = FeedbackForm
    model = Feedback
    template_name = 'adverts/feedback.html'
    def form_valid(self, form):
        advert_id = self.request.GET.get('advert_id')
        feedback = form.save(commit=False)
        feedback.user = User.objects.get(pk=self.request.user.pk)
        feedback.save()
        AdvertFeedback.objects.create(feedback=feedback, advert=Advert.objects.get(pk=advert_id))
        feedback_pub_notification.apply_async([feedback.pk])
        return redirect('/')

@login_required
def feedback_list(request):
    user = User.objects.get(username=request.user)
    adverts = Advert.objects.filter(user=user)
    feedbacks = Feedback.objects.all()
    context = {'adverts' : adverts, 'feedbacks' : feedbacks}
    return render(request, 'adverts/feedbacks.html', context=context)

class FeedbackList(
    LoginRequiredMixin,
    ListView):
    model = Feedback
    ordering = 'pub_time'
    template_name = 'adverts/feedbacks.html'
    context_object_name = 'feedbacks'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = FeedbackFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

def feedback_delete(request):
    feedback_id = request.GET.get('feedback_id')
    feedback_del_notification.apply_async([feedback_id])
    Feedback.objects.get(pk=feedback_id).delete()
    return redirect('/feedbacks/')

def feedback_accept(request):
    feedback_id = request.GET.get('feedback_id')
    feedback = Feedback.objects.get(pk=feedback_id)
    feedback.accept = True
    feedback_acc_notification.apply_async([feedback_id])
    feedback.save()
    return redirect('/feedbacks/')

def feedback_reject(request):
    feedback_id = request.GET.get('feedback_id')
    feedback = Feedback.objects.get(pk=feedback_id)
    feedback.accept = False 
    feedback_rej_notification.apply_async([feedback_id])
    feedback.save()
    return redirect('/feedbacks/')