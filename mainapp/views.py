from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .core import leaderboard_functions, personal_stats_functions, progress_functions, common_functions
from django.shortcuts import redirect
from .forms import LeaderBoardForm, PersonalStatsForm, ProgressForm, ProgressFormVersus, BestMessageForm, FeedbackForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


def group_required(*group_names):
    """View decorator : requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)


def index_view(request):
    template = loader.get_template('index.html')
    leaderboard = common_functions.refactor_dict(leaderboard_functions.get_leader_board())
    names = list(leaderboard.keys())
    top1, top2, top3 = names[0], names[1], names[2]
    return HttpResponse(template.render({'top1': top1, 'top2': top2, 'top3': top3}, request))


def leaderboard_view(request):
    if request.method == 'POST':

        form = LeaderBoardForm(request.POST)
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        top_best = request.POST['top_best']
        top_worst = request.POST['top_worst']
        graph_type = request.POST['graph_type']

        b64 = leaderboard_functions.get_leader_board_image(str(start_date), str(end_date),
                                                           top_best, top_worst, graph_type)
        template = loader.get_template('leaderboard_post.html')
        return HttpResponse(template.render({'chart': b64, 'form': form}, request))
    else:
        template = loader.get_template('leaderboard.html')
        return HttpResponse(template.render({'form': LeaderBoardForm()}, request))


def personal_stats_view(request):
    if request.method == 'POST':
        form = PersonalStatsForm(request.POST)
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        name = request.POST['name']
        word = request.POST['word']

        context = personal_stats_functions.get_personal_stats(name, start_date, end_date, word)
        context = context | {'name': name, 'form': form, 'start_date': start_date, 'end_date': end_date, 'word': word}
        context['name'] = name
        context['form'] = form
        template = loader.get_template('personal_stats_post.html')
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('personal_stats.html')
        return HttpResponse(template.render({'form': PersonalStatsForm()}, request))


def progress_view(request):
    if request.method == 'POST':
        form = ProgressForm(request.POST)
        name = request.POST['name']
        mode = request.POST['mode']
        graph_type = request.POST['graph_type']

        b64 = progress_functions.get_image_progress(name, mode, graph_type)
        context = {'chart': b64, 'form': form}
        template = loader.get_template('progress_post.html')
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('progress.html')
        return HttpResponse(template.render({'form': ProgressForm()}, request))


def progress_versus_view(request):
    if request.method == 'POST':
        form = ProgressFormVersus(request.POST)
        if form.is_valid():
            names = form.cleaned_data.get('names')
            b64 = progress_functions.get_image_progress_versus(names)
            context = {'chart': b64, 'form': form}
            template = loader.get_template('progress_versus_post.html')
            return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('progress_versus.html')
        return HttpResponse(template.render({'form': ProgressFormVersus()}, request))


@login_required()
def feedback_view(request):  # any user can send feedback : use signup form to create account
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            # save article to db
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('mainapp:feedback')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})


@group_required('see-messages-auth')
def best_message_view(request):  # must have special permissions, this page will reveal messages
    if request.method == 'POST':
        form = BestMessageForm(request.POST)
        react = request.POST['react']
        n_msg = int(request.POST['n_msg'])
        top_list = progress_functions.get_best_messages(react, n=n_msg)
        context = {'top_list': top_list, 'form': form}
        template = loader.get_template('best_message_post.html')
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('best_message.html')
        return HttpResponse(template.render({'form': BestMessageForm()}, request))
