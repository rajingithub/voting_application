from django.http import HttpResponse,HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from .models import Question,Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     # template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list
#     }
#     return render(request,'polls/index.html',context)
#     # return HttpResponse(template.render(context,request))

# def IndexView(generic.ListView):
#     template_name = "polls/index.html"
#     context_object_name = "latest_question_list"

#     def get_queryset(self):
#         return Question.objects.order_by("pub_date")[:5]

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
    def get(self,request):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 2)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # return render(request,"polls/detail.html",{"question":question,"error_message":"You didn't select a choice."})
        return render(request,"polls/index.html",{'latest_question_list':page_obj})
        

# def detail(request,question_id):
#     question = get_object_or_404(Question,pk = question_id)
#     return render(request,'polls/detail.html',{'question':question})
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
        #queryset = Question.objects.filter(pub_date__lte=timezone.now())
    

# def results(request,question_id):
#     # response = "You are looking at the results of question %s."
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,"polls/results.html",{"question":question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
    except (KeyError,Choice.DoesNotExist):
        return render(request,"polls/detail.html",{"question":question,"error_message":"You didn't select a choice."})
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

    # return HttpResponse("You are voting for question %s."%question_id)
