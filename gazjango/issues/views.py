from django.db.models           import Q
from django.template            import RequestContext
from django.shortcuts           import render_to_response
from gazjango.misc.view_helpers import get_by_date_or_404, filter_by_date, boolean_arg

from gazjango.announcements.models import Announcement
from gazjango.articles.models      import Article
from gazjango.issues.models        import Issue, Menu, Event
from gazjango.jobs.models          import JobListing
from gazjango.comments.models      import PublicComment

import datetime

def issue_for_date(request, year, month, day, plain=False):
    issue = get_by_date_or_404(Issue, year, month, day, field='date')
    return show_issue(request, issue, plain)

def latest_issue(request, plain=False):
    return show_issue(request, Issue.objects.latest(), plain)

def show_issue(request, issue, plain=False):
    tomorrow = issue.date + datetime.timedelta(days=1)
    comments = PublicComment.visible.filter(time__lt=tomorrow).order_by('-time')
    
    one_week = datetime.timedelta(days=7)
    if issue.date == datetime.date.today():
        jobs = JobListing.unfilled.get_for_show(num=5, cutoff=one_week)
    else:
        jobs = JobListing.published.get_for_show(num=5, base_date=issue.date, cutoff=one_week)
    
    articles = issue.articles_in_order(racy=boolean_arg(request.GET, 'racy', True))
    try:
        topstory = articles[0]
    except IndexError:
        raise Http404
    
    data = {
        'issue': issue,
        'topstory': articles[0],
        'midstories': articles[1:3],
        'lowstories': articles[3:],
        'jobs': jobs,
        'comments': comments[:5],
        'for_email': boolean_arg(request.GET, 'for_email', False)
    }
    template = "issue/issue." + ('txt' if plain else 'html')
    return render_to_response(template, data)


def issues_list(request, year=None, month=None):
    issues = filter_by_date(Issue.objects.all(), year, month, field='date')
    data = {
        'issues': issues,
        'year': year,
        'month': month
    }
    rc = RequestContext(request)
    return render_to_response("issue/issues_list.html", data, context_instance=rc)


def rsd_now(request, plain=False):
    today = datetime.date.today()
    return show_rsd(request, today.year, today.month, today.day, plain)

def show_rsd(request, year, month, day, plain=False):
    date = datetime.date(int(year), int(month), int(day))
    not_event = Q(event_date=None)
    current = Announcement.community.filter(date_start__lte=date, date_end__gte=date)
    current = current.order_by('-date_start', 'pk')
    
    one_week = datetime.timedelta(days=7)
    if date == datetime.date.today():
        jobs = JobListing.unfilled.get_for_show(num=5, cutoff=one_week)
    else:
        jobs = JobListing.published.get_for_show(num=5, base_date=date, cutoff=one_week)
    
    tomorrow = date + datetime.timedelta(days=1)
    comments = PublicComment.visible.filter(time__lt=tomorrow).order_by('-time')
    
    base = Article.published.filter(pub_date__lt=tomorrow, is_racy=False)
    t,m,l = Article.published.get_stories(num_top=3, num_mid=0, num_low=0, base=base)
    
    data = {
        'year': year, 'month': month, 'day': day,
        'date': date,
        'announcements': current.filter(not_event),
        'events': current.exclude(not_event),
        'jobs': jobs,
        'comments': comments[:3],
        'stories': t,
        'for_email': boolean_arg(request.GET, 'for_email', False)
    }
    template = "issue/rsd." + ('txt' if plain else 'html')
    return render_to_response(template, data)



def menu_partial(request):
    if datetime.datetime.now().hour < 21:
        menu = Menu.objects.for_today()
    else:
        menu = Menu.objects.for_tomorrow()
    return render_to_response("scraped/menu.html", { 'menu': menu })


def events_partial(request):
    today = datetime.date.today()
    events = Event.objects.for_date(today, forward=datetime.timedelta(days=40))
    return render_to_response("scraped/events.html", {'events': events})
