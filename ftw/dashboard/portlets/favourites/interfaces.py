from zope.interface import Interface


class IFavouritesLocation(Interface):
    """The IFavouritesLocation adapter provides information about where the
    favorites are stored.
    """

    def get_favorites_folder(self):
        """ Returns the the favorite folder
        trying get this names frm user home folder:
        favourites, favorites, Favorites and Favourites
        WARNING: the same implementation is in:
        skins/ftw*/addtofavourites.py
        """

    def get_favourites_filter_query(self):
        """Returns a catalog query for filtering objects in favorites
        folder when listing them in the portlet.
        The query is empty by default since we expect only favorites in the
        favourites folder.
        """
