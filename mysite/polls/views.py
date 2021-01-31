import json
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from polls import models
from .models import QuestionTags, Choice, Question, createQuestion
from django.templatetags.static import static



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):

        #Return the last five published questions (not including those set to be
        #published in the future).

        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    #from this point on, errorrs may occur


@csrf_exempt
def createq(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        store_data = data
        q = Question(question_text = store_data["Question"], pub_date=timezone.now())
        q.save()
        for key, value in store_data["OptionVote"].items():
            q.choice_set.create(choice_text=key, votes=value)
        tags_list = QuestionTags.objects.values_list('tags_text', flat=True)


        for tag in store_data["Tags"]:          #loop to stop duplication
            tagfind = 0                         #of tags
            for dupe in tags_list:
                if dupe == tag:
                    q.tags.add(QuestionTags.objects.get(tags_text=tag))
                    tagfind = 1
                    break
            if tagfind == 0:
                t = QuestionTags(tags_text = tag)
                t.save()
                q.tags.add(t)

        return HttpResponse(request)

    elif request.method == 'GET':
        ls = []
        
        question = Question.objects.all()
        
        for x in range(len(question)):

            q = question[x]
            qd = str(q.id)  # instance of question
            #print(qd)
            cho_vot = (Choice.objects.filter(question=q).values("choice_text", "votes"))
            cv_dict = {}
            for c in cho_vot:  # concatenating choice and votes
                ch = c["choice_text"]
                vo = str(c["votes"])
                cv_dict[ch] = vo  # dictionary of choices and votes
            ls_tags = []
            t = QuestionTags.objects.filter(question=q).values("tags_text")
            for l in t:
                ls_tags.append(l["tags_text"])
                                                #list of tags
            ls_dict = { "QID":qd, "Question": q.question_text, "OptionVote": cv_dict, "Tags": ls_tags}

            ls.append(ls_dict)
            #print(ls)
            #try:
          #  questn = Question.objects.get(pk = Question_id)
           # qid = questn.id
            #cho_vot = (Choice.objects.filter(question=questn).values("choice_text","votes"))
            #cv_dict={}
            """for c in cho_vot:  # concatenating choice and votes
                ch = c["choice_text"]
                vo = str(c["votes"])
                cv_dict[ch] = vo  # dictionary of choices and votes
            
            ls_dict = {"QID":qid, "Question": questn.question_text, "OptionVote": cv_dict, "Tags": ls_tags}
            ls.append(ls_dict)  
        except Question.DoesNotExist:
            pass"""

        return HttpResponse(json.dumps(ls, indent=4), content_type="application/json")

        #*******DOPE********
def detail(request, question_id):
    global Question_id
    Question_id=question_id
    return render(request, 'polls/polldetail.html')


def poll_details(request):

    global ls
    ls= []
    try:
        questn = Question.objects.get(pk=Question_id)
        cho_vot = (Choice.objects.filter(question=questn).values("choice_text", "votes"))
        cv_dict = {}
        for c in cho_vot:  # concatenating choice and votes
            ch = c["choice_text"]
            vo = str(c["votes"])
            cv_dict[ch] = vo  # dictionary of choices and votes

        # list of tags
        ls_dict = {"QID":Question_id, "Question": questn.question_text, "OptionVote": cv_dict}
        ls.append(ls_dict)

    except Question.DoesNotExist:
        pass


    return HttpResponse(json.dumps(ls, indent=4), content_type="application/json")



#********DOPE**********
#for getting tags in jquery
def get_tags(request):
    ls_tags=[]
    tags_dict={}
    t = QuestionTags.objects.all().values("tags_text")
    for key in t:
        ls_tags.append(key["tags_text"])
    tags_dict["Tags"]=ls_tags
    return HttpResponse(json.dumps(tags_dict, indent=4), content_type="application/json")

def home_view(request):

    filterd_tags=request.GET.getlist('selctd_tags[]')

    #print(filterd_tags)
    html = "<html><body>It is now .</body></html>"

    ls=[]
    listid=[]
    for y in filterd_tags:

        t = QuestionTags.objects.filter(tags_text=y).values("question")
        #print(t)
        if t.exists():
            for things in t:
                q_id = things['question']
                listid.append(q_id)
            #print(listid)
    listid=list(set(listid))
    for x in listid:
        try:
            questn = Question.objects.get(id=x)
            qid = str(questn.id)
            cho_vot = (Choice.objects.filter(question=questn).values("choice_text", "votes"))
            cv_dict = {}
            for c in cho_vot:  # concatenating choice and votes
                ch = c["choice_text"]
                vo = str(c["votes"])
                cv_dict[ch] = vo  # dictionary of choices and votes
            ls_tags = []
            t = QuestionTags.objects.filter(question=questn).values("tags_text")
            for l in t:
                ls_tags.append(l["tags_text"])
            # list of tags
            ls_dict = {"QID":qid,"Question": questn.question_text, "OptionVote": cv_dict, "Tags": ls_tags}
            ls.append(ls_dict)
            #print(ls)
        except Question.DoesNotExist:
            pass
    return HttpResponse(json.dumps(ls, indent=4), content_type="application/json")
@csrf_exempt
def pollvotes(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        print(data)
        try:
            quest = Question.objects.get(pk = Question_id)
            cho_vot = (Choice.objects.filter(question=quest).values("choice_text", "votes"))
            cv_dict = {}
            for c in cho_vot:  # concatenating choice and votes
                ch = c["choice_text"]
                if([ch] == data):

                    int(c["votes"])
                    c["votes"] = c["votes"] + 1
                    
                    
                vo = str(c["votes"])
                cv_dict[ch] = vo  # dictionary of choices and votes
                print(cv_dict)
            for key, value in cv_dict.items():
                quest.choice_set.create(choice_text=key, votes=value)

        except Question.DoesNotExist:
            pass
        

    
    return HttpResponse(request)

