from ftw.dashboard.portlets.favourites import favouriteMessageFactory as _
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from ftw.dashboard.portlets.favourites.interfaces import IFavouritesHandler
from Products.Five.browser import BrowserView
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
import time


class RemoveFavourite(BrowserView):
    """Removes a favourite
    """

    def __call__(self, *args, **kwargs):

        handler = getMultiAdapter((self.context, self.request),
            IFavouritesHandler)

        fav_id = self.request.get('uid', '')

        handler.remove_favourite(fav_id)

        return 'ok'


class AddFavourite(BrowserView):
    """ Add a favourite
    """

    def __call__(self):

        handler = getMultiAdapter((self.context, self.request),
            IFavouritesHandler)

        view_url = self.context.absolute_url()

        fav_id = 'fav_' + getUtility(IIDNormalizer).normalize(time.time())
        utils = getToolByName(self.context, 'plone_utils')

        handler.add_favourite(
            fav_id,
            self.context.TitleOrId(),
            self.context.portal_url.getRelativeUrl(self.context),
            )

        title = self.context.title_or_id()
        if not isinstance(title, unicode):
            title = title.decode('utf-8')
        msg = _(
            u'${title} has been added to your Favourites.',
            mapping={u'title': title})

        utils.addPortalMessage(msg)

        return self.request.response.redirect(view_url)


class ReorderFavourites(BrowserView):
    """Reorder the favourites
    """

    def __call__(self):

        handler = getMultiAdapter((self.context, self.request),
            IFavouritesHandler)

        handler.order_favourites(self.request.get('favourites'))

        return 'ok'
