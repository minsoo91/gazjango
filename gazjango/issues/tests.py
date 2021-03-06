import unittest
from gazjango.articles.models import Article, Section
from gazjango.issues.models   import Issue
from datetime import date, timedelta

class IssueTestCase(unittest.TestCase):
    
    def setUp(self):
        self.news     = Section.objects.create(name="News", slug="news")
        self.features = Section.objects.create(name="Features", slug="features")
        self.html = 'h'
        
        b = dict(headline="Boring", text="Text", slug="boring", 
                 section=self.news, format=self.html)
        self.boring_article = Article.objects.create(**b)
        
        e = dict(headline="Excitement", text="Text", slug="exciting", 
                 section=self.features, format=self.html)
        self.exciting_article = Article.objects.create(**e)
        
        self.issue_today = Issue.objects.create()
        yesterday = date.today() - timedelta(days=1)
        self.issue_yesterday = Issue.objects.create(date=yesterday)
    
    def tearDown(self):
        for m in (Article, Section, Issue):
            m.objects.all().delete()
    
    def testOrdering(self):
        self.issue_today.articles.add(self.boring_article)
        self.assert_(self.issue_today.articles.count() == 1)
        self.assert_(self.issue_yesterday.articles.count() == 0)
        
        self.issue_yesterday.articles.add(self.boring_article)
        self.assert_(self.issue_today.articles.count() == 1)
        self.assert_(self.issue_yesterday.articles.count() == 1)
        
        fail = lambda: self.issue_today.articles.add(self.boring_article)
        self.assertRaises(Exception, fail)
        
        # TODO: this changed and is now broken :/
        self.assertEquals(self.issue_today.get_issuearticle_order(),
                [self.boring_article.issuearticle_set.get(issue=self.issue_today).pk])
        
        self.issue_today.articles.add(self.exciting_article)
        boring_ia   = self.boring_article.issuearticle_set.get(  issue=self.issue_today)
        exciting_ia = self.exciting_article.issuearticle_set.get(issue=self.issue_today)
        
        self.assertEquals(self.issue_today.get_issuearticle_order(),
                          [boring_ia.pk, exciting_ia.pk])
        
        self.issue_today.set_issuearticle_order([exciting_ia.pk, boring_ia.pk])
        self.assertEquals([a.pk for a in self.issue_today.articles_in_order().all()], 
                         [self.exciting_article.pk, self.boring_article.pk])
    
