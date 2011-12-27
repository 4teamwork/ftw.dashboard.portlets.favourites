from Products.CMFCore.utils import getToolByName
from ftw.dashboard.portlets.favourites.interfaces import IFavouritesLocation
from zope.component import adapts, getMultiAdapter
from zope.interface import Interface, implements


DEFAULT_IDS = ['favourites', 'Favourites', 'Favorites', 'favorites']


class DefaultFavouritesLocation(object):
    implements(IFavouritesLocation)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context

    def get_favorites_folder(self, ids=None):
        """ Returns the the favorite folder
        trying get this names frm user home folder:
        favourites, favorites, Favorites and Favourites
        WARNING: the same implementation is in:
        skins/ftw*/addtofavourites.py
        """

        mtool = getToolByName(self.context, 'portal_membership')
        homeFolder = mtool.getHomeFolder()
        if not homeFolder:
            return None

        if ids is None:
            ids = DEFAULT_IDS

        for fav_folder_name in ids:
            if hasattr(homeFolder, fav_folder_name):
                return getattr(homeFolder, fav_folder_name, None)

    def get_favourites_filter_query(self):
        """Returns a catalog query for filtering objects in favorites
        folder when listing them in the portlet.
        The query is empty by default since we expect only favorites in the
        favourites folder.
        """
        return {}


def get_fav_folder(context):
    # deprecated
    location = getMultiAdapter((context, context.REQUEST), IFavouritesLocation)
    return location.get_favorites_folder()
