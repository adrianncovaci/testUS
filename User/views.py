from django.shortcuts import render
from .models import Class, Test, Submission
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .forms import SumbissionForm
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.template.loader import get_template

from .utils import render_to_pdf #created in step 4


# Create your views here.

class ClassListView(LoginRequiredMixin, generic.ListView):
    model = Class
    template_name = 'User/class_list.html'
    context_object_name = 'class_list'
    

def ClassDetailView(request, pk):
    class_group = get_object_or_404(Class, pk=pk)
    tests = class_group.tests.all()
    class_list = Class.objects.all()
    return render(request, 'User/class_detail.html', {'class_group': class_group, 'tests': class_group.tests.all, 'class_list': class_list})


def SubmissionListView(request, pk):
    submissions = Submission.objects.filter(test=pk)
    return render(request, 'User/submission_list.html', {'submissions': submissions})


def CreateSubmission(request):
    data = dict()

    if request.method == 'POST':
        form = SumbissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = SumbissionForm()

    context = {'form': form}
    data['html_form'] = render_to_string('User/submission_create.html',
        context,
        request=request
    )
    return JsonResponse(data)


class GeneratePDF(generic.View):
    def get(self, request, pk, *args, **kwargs):
        submission = Submission.objects.get(pk=pk)
        data = {
            'submission': submission
        }
        pdf = render_to_pdf('pdf/work.html', data)
        return HttpResponse(pdf, content_type='application/pdf')