from django.template  import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from articles.models  import Article

def article(request, slug, year, month, day, template="story.html"):
    story = get_object_or_404(Article, slug=slug,
                pub_date__year=year, pub_date__month=month, pub_date__day=day)
    data = {
        'story': story,
        'related': story.related_list(3),
        'topstory': Article.published_objects.get_top_story(),
        'comments': []
    }
    rc = RequestContext(request)
    return render_to_response("story.html", data, context_instance=rc)


homepage      = lambda request, **kwargs: render_to_response("base.html", locals())
search        = lambda request, **kwargs: render_to_response("base.html", locals())
comment       = lambda request, **kwargs: render_to_response("base.html", locals())
print_article = lambda request, **kwargs: render_to_response("base.html", locals())
email_article = lambda request, **kwargs: render_to_response("base.html", locals())
archives      = lambda request, **kwargs: render_to_response("base.html", locals())

articles_for_year  = lambda request, **kwargs: render_to_response("base.html", locals())
articles_for_month = lambda request, **kwargs: render_to_response("base.html", locals())
articles_for_day   = lambda request, **kwargs: render_to_response("base.html", locals())

announcement            = lambda request, **kwargs: render_to_response("base.html", locals())
announcements           = lambda request, **kwargs: render_to_response("base.html", locals())
announcements_for_year  = lambda request, **kwargs: render_to_response("base.html", locals())
announcements_for_month = lambda request, **kwargs: render_to_response("base.html", locals())
announcements_for_day   = lambda request, **kwargs: render_to_response("base.html", locals())

announcement_kind           = lambda request, **kwargs: render_to_response("base.html", locals())
announcement_kind_for_year  = lambda request, **kwargs: render_to_response("base.html", locals())
announcement_kind_for_month = lambda request, **kwargs: render_to_response("base.html", locals())
announcement_kind_for_day   = lambda request, **kwargs: render_to_response("base.html", locals())

category           = lambda request, **kwargs: render_to_response("base.html", locals())
category_for_year  = lambda request, **kwargs: render_to_response("base.html", locals())
category_for_month = lambda request, **kwargs: render_to_response("base.html", locals())
category_for_day   = lambda request, **kwargs: render_to_response("base.html", locals())
