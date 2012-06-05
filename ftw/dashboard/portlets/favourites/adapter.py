from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry


class NoHomeFolderError(Exception):
    """ Raised when the user has no homefolder
    """


class RegistryKeyError(Exception):
    """ Raised when there is no registry entry
    """


class DefaultFavouritesHandler(object):
    """ Provides functions to add, remove or reorder favourites
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.addable_types = ['Link']

    def create_favourites_folder(self):
        """ Create the favourites folder
        """
        home_folder = self.get_home_folder()
        foldername = self.get_favourite_folder_name()

        home_folder.invokeFactory(
            'Folder',
            id=foldername,
            title=foldername)

        folder = home_folder.get(foldername)

        folder.setConstrainTypesMode(1)
        folder.setImmediatelyAddableTypes(self.addable_types)
        folder.setLocallyAllowedTypes(self.addable_types)

    def add_favourite(self, fav_id, title, remote_url):
        """ Add favourite to the favourites folder
        """
        folder = self.get_favourites_folder()
        folder.invokeFactory(
            'Link',
            id=fav_id,
            title=title,
            remote_url=remote_url)

        favourite = folder.get(fav_id)
        favourite.reindexObject()

        return favourite

    def remove_favourite(self, fav_id):
        """ Remove favourite from th favourites folder
        """
        folder = self.get_favourites_folder()

        try:
            folder.manage_delObjects(fav_id)

        except AttributeError:
            return False

        return True

    def order_favourites(self, fav_ids=[]):
        """ Reorder the favourites in the given order of fav_ids
        """
        folder = self.get_favourites_folder()

        for i, fav_id in enumerate(fav_ids):
            obj = folder.get(fav_id, '')

            if not obj:
                continue

            folder.moveObject(fav_id, i)
            obj.reindexObject(idxs=['getObjPositionInParent'])

    def get_favourites_folder(self):
        """ Returns the folder the favourites are stored in
        """
        home_folder = self.get_home_folder()
        folder_name = self.get_favourite_folder_name()

        if not home_folder.get(folder_name):
            self.create_favourites_folder()

        return home_folder.get(folder_name)

    def get_favourites(self):
        """Return all favourites
        """
        folder = self.get_favourites_folder()
        catalog = getToolByName(folder, 'portal_catalog')
        brains = catalog(self.get_favourites_filter_query())

        return brains

    def get_favourites_filter_query(self):
        """Returns a catalog query to get favourites
        """
        folder = self.get_favourites_folder()
        query = {
            'path': {'query': '/'.join(folder.getPhysicalPath())},
            'portal_type': self.addable_types,
            'sort_on': 'getObjPositionInParent',
        }

        return query

    def get_favourite_folder_name(self):
        """ Return the foldername where we want to store favourites
        """
        registry = getUtility(IRegistry)
        name = registry.get('ftw.dashboard.portlets.favourites.foldername')

        if not name:
            raise RegistryKeyError(
                'Could not read the favourite ' \
                + 'folder name from the registry.')

        return name

    def get_home_folder(self):
        """ Return the homefolder of the logged-in user.
        """
        mtool = getToolByName(self.context, 'portal_membership')
        home_folder = mtool.getHomeFolder()

        if not home_folder:
            raise NoHomeFolderError(
                "Can't access home folder. " \
                "Please make sure you're owner of a homefolder")
        return home_folder
