from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.dashboard.portlets.favourites import _
from ftw.dashboard.portlets.favourites.fav_folder import get_fav_folder
from ftw_formhelper import ftwAddForm, ftwEditForm
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implements


class IFavouritePortlet(IPortletDataProvider):
    count = schema.Int(title=_(u"Number of items to display"),
                       description=_(u"How many items to list."),
                       required=True,
                       default=5)


class Assignment(base.Assignment):
    implements(IFavouritePortlet)

    def __init__(self, count=5):
        self.count = count

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
        return self._data()

    def favObjects(self):
        return self.getObject()

    #XXX: @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def _data(self):
        homeFolder = self.context.portal_membership.getHomeFolder()
        if homeFolder is None:
            return []

        count = getattr(self.data, 'count', 10)
        favFolder = get_fav_folder(self.context)
        if favFolder:
            return favFolder.getFolderContents()[:count]

        return []


class AddForm(ftwAddForm):
    form_fields = form.Fields(IFavouritePortlet)
    label = _(u"Add Favorite Portlet")
    description = _(u"This portlet displays your Favorites")

    def create(self, data):
        return Assignment(count=data.get('count', 5))


class EditForm(ftwEditForm):
    form_fields = form.Fields(IFavouritePortlet)
    label = _(u"Edit Favorite Portlet")
    description = _(u"This portlet displays your Favorites")
