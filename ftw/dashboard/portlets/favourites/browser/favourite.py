import json
import time

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from ftw.dashboard.portlets.favourites import favouriteMessageFactory as _
from ftw.dashboard.portlets.favourites.interfaces import IFavouritesHandler
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getMultiAdapter
from zope.component import getUtility


# Try to get the plone.protect's createToken method, because it's only
# available since version 2.0.2, otherwise we just use a mocked method.
try:
    from plone.protect import createToken
    PLONE_PROTECT_AVAILABLE = True
except ImportError:
    PLONE_PROTECT_AVAILABLE = False


class RemoveFavourite(BrowserView):
    """Removes a favourite
    """

    def __call__(self, *args, **kwargs):

        handler = getMultiAdapter((self.context, self.request),
            IFavouritesHandler)

        fav_id = self.request.get('uid', '')

        handler.remove_favourite(fav_id)

        return 'ok'


class RenameFavourite(BrowserView):
    """Renames a favourite
    """

    def __call__(self, *args, **kwargs):

        handler = getMultiAdapter(
            (self.context, self.request),
            IFavouritesHandler
        )

        fav_id = self.request.get('uid', '')
        title = self.request.get('title', '')

        handler.rename_favourite(fav_id, title)

        return json.dumps({'success': True})


class AddFavourite(BrowserView):
    """ Add a favourite
    """

    def get_url(self):
        """Returns url for adding the current context to the favourites.
        """
        url = '{}/@@add_to_favourites/add'.format(self.context.absolute_url())

        if PLONE_PROTECT_AVAILABLE:
            url = '{}?_authenticator={}'.format(url, createToken())

        return url

    def add(self):
        """Add a favourite of the current context.
        """
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
