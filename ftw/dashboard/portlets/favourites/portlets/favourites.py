from ftw.dashboard.portlets.favourites import favouriteMessageFactory as _
from ftw.dashboard.portlets.favourites.interfaces import IFavouritesHandler
from plone.app.portlets.browser.formhelper import NullAddForm
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getMultiAdapter
from zope.interface import implements


# Try to get the plone.protect's createToken method, because it's only
# available since version 2.0.2, otherwise we just use a mocked method.
try:
    from plone.protect import createToken
except ImportError:
    def createToken():
        return ''


class IFavouritePortlet(IPortletDataProvider):
    """ Portlet to handle favourites
    """


class Assignment(base.Assignment):
    implements(IFavouritePortlet)

    @property
    def title(self):
        return _(u"Favourites", default="Favourites")


def _render_cachekey(fun, self):
    return render_cachekey(fun, self)


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/favourites.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def items(self):
        handler = getMultiAdapter((self.context, self.request),
                                  IFavouritesHandler)

        return handler.get_favourites()

    def render(self):
        return xhtml_compress(self._template())

    def authenticator_token(self):
        return createToken()


class AddForm(NullAddForm):

    def create(self):
        return Assignment()

    def nextURL(self):
        status = IStatusMessage(self.request)
        # title = ''
        status.addStatusMessage(_(u'Portlet edited'), type='info')

        return self.request.form.get('referer')
