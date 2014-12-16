from zope.interface import Interface


class IFavouritesHandler(Interface):
    """The IFavouritesHandler adapter provides functionality to create
    favourites folder and add or remove
    """

    def create_favourites_folder(self):
        """ Create the favourites folder
        """

    def add_favourite(self, fav_id, title, remote_url):
        """ Add favourite to the favourites folder
        """

    def remove_favourite(self, fav_id):
        """ Remove favourite from th favourites folder
        """

    def rename_favourite(self, fav_id, title):
        """ Rename a favourite
        """

    def order_favourites(self, fav_ids=[]):
        """ Reorder the favourites in the given order of fav_ids
        """

    def get_favourites_folder(self):
        """ Returns the folder the favourites are stored in
        """

    def get_favourites(self):
        """Return all favourites
        """

    def get_favourites_filter_query(self):
        """Returns a catalog query to get favourites
        """

    def get_favourite_folder_name(self):
        """ Return the foldername where we want to store favourites
        """

    def get_home_folder(self):
        """ Return the homefolder of the logged-in user.
        """
