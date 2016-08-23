from zope.interface import Interface


class IFavouritesHandler(Interface):
    """The IFavouritesHandler adapter provides functionality to create
    favourites container and add or remove
    """

    def create_favourites_container():
        """ Create the favourites container
        """

    def add_favourite(fav_id, title, remote_url):
        """ Add favourite to the favourites container
        """

    def remove_favourite(fav_id):
        """ Remove favourite from th favourites container
        """

    def rename_favourite(fav_id, title):
        """ Rename a favourite
        """

    def order_favourites(fav_ids=[]):
        """ Reorder the favourites in the given order of fav_ids
        """

    def get_favourites_container():
        """ Returns the container the favourites are stored in
        """

    def get_favourites():
        """Return all favourites
        """


class IFavouritesAnnotationStorageLayer(Interface):
    """ Browser layer for annotation storage
    """
