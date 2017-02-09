from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .models import AssignedChores


class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class IndexView(LoggedInMixin, TemplateView):

    template_name = 'chores/chores.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        user = self.request.user
        assigned_chores = AssignedChores.objects.filter(user=user).first()
        context['assigned_chores'] = assigned_chores
        return context
