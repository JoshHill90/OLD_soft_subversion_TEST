from django.test import SimpleTestCase
from django.urls import reverse, resolve
from site_app.views import index_page, about_page, ContactView, o_main, InviteView


class TestUrls(SimpleTestCase):
    
    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertAlmostEquals(resolve(url).func, index_page)
    
    def test_about_url_is_resolved(self):
        url = reverse('about')
        self.assertAlmostEquals(resolve(url).func, about_page)
    
    def test_contact_url_is_resolved(self):
        url = reverse('contact')
        self.assertAlmostEquals(resolve(url).func.view_class, ContactView)
        
    def test_o_panel_url_is_resolved(self):
        url = reverse('o_panel')
        self.assertAlmostEquals(resolve(url).func, o_main)
        
    def test_o_panel_url_is_resolved(self):
        url = reverse('o_panel')
        self.assertAlmostEquals(resolve(url).func, InviteView)