from gazjango.issues.management.commands import SendingOutCommand
from django.core.management.base         import CommandError
from django.core.mail                    import mail_admins
from django.http                         import Http404

from gazjango.issues.models        import Issue
from gazjango.issues.views         import show_issue
from gazjango.options.helpers      import is_publishing
from gazjango.subscriptions.models import Subscriber

import datetime

class Command(SendingOutCommand):
    subscriber_base = Subscriber.issues
    
    def set_content(self, dummy_request):
        if not is_publishing():
            raise CommandError('Not in publishing mode.')
        
        issue, created = Issue.objects.populate_issue()
        if not issue.articles.count():
            mail_admins('ERROR IN SENDING GAZETTE ISSUE FOR '+
                        issue.date.strftime('%A, %B %d, %Y'),
                        "there were no articles, but we're in publish mode!")
            raise CommandError('No issue, so not sending it.')
        
        self.html_content = show_issue(dummy_request, issue).content
        self.text_content = show_issue(dummy_request, issue, plain=True).content
        
        dummy_request.GET['racy'] = 'no'
        self.tame_html_content = show_issue(dummy_request, issue).content
        self.tame_text_content = show_issue(dummy_request, issue, plain=True).content
    
    def contents_for_subscriber(self, subscriber):
        if subscriber.racy_content:
            return (self.text_content, self.html_content)
        else:
            return (self.tame_text_content, self.tame_html_content)
    
