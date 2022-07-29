from BTrees.OOBTree import OOBTree
from ftw.dashboard.portlets.favourites.interfaces import IFavouritesHandler
from persistent.dict import PersistentDict
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import implements


ANNOTATION_KEY = "ftw.dashboard.portlets.favourites:favourites"


class NoHomeFolderError(Exception):
    """ Raised when the user has no homefolder
    """


class RegistryKeyError(Exception):
    """ Raised when there is no registry entry
    """


class DefaultFavouritesHandler(object):
    """ Provides functions to add, remove or reorder favourites
    """
    implements(IFavouritesHandler)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.addable_types = ['Link']

    def create_favourites_container(self):
        """ Create the favourites folder
        """
        alsoProvides(self.request, IDisableCSRFProtection)
        home_folder = self.get_home_folder()
        foldername = self.get_favourite_folder_name()

        home_folder.invokeFactory(
            'Folder',
            id=foldername,
            title=foldername)

        folder = ISelectableConstrainTypes(home_folder.get(foldername))

        folder.setConstrainTypesMode(1)
        folder.setImmediatelyAddableTypes(self.addable_types)
        folder.setLocallyAllowedTypes(self.addable_types)

    def add_favourite(self, fav_id, title, remote_url):
        """ Add favourite to the favourites folder
        """
        folder = self.get_favourites_container()
        folder.invokeFactory('Link', id=fav_id)
        favourite = folder.get(fav_id)

        favourite.remoteUrl = remote_url
        favourite.setTitle(title)
        favourite.reindexObject()
        return favourite

    def remove_favourite(self, fav_id):
        """ Remove favourite from th favourites folder
        """
        folder = self.get_favourites_container()

        try:
            folder.manage_delObjects(fav_id)

        except AttributeError:
            return False

        return True

    def rename_favourite(self, fav_id, title):
        """ Rename a favourite
        """
        folder = self.get_favourites_container()
        favourite = folder.get(fav_id)
        if favourite:
            favourite.setTitle(title)
            favourite.reindexObject()
            return True
        return False

    def order_favourites(self, fav_ids=[]):
        """ Reorder the favourites in the given order of fav_ids
        """
        folder = self.get_favourites_container()

        for i, fav_id in enumerate(fav_ids):
            obj = folder.get(fav_id, '')

            if not obj:
                continue

            folder.moveObject(fav_id, i)
            obj.reindexObject(idxs=['getObjPositionInParent'])

    def get_favourites_container(self):
        """ Returns the folder the favourites are stored in
        """
        home_folder = self.get_home_folder()
        folder_name = self.get_favourite_folder_name()

        if not home_folder.get(folder_name):
            self.create_favourites_container()

        return home_folder.get(folder_name)

    def get_favourites(self):
        """Return all favourites
        """
        folder = self.get_favourites_container()
        catalog = getToolByName(folder, 'portal_catalog')
        brains = catalog(self.get_favourites_filter_query())
        result = []

        for brain in brains:
            result.append({'id': brain.id,
                           'title': brain.Title,
                           'url': brain.getRemoteUrl.replace('resolveUid',
                                                             'resolveuid')})

        return result

    def get_favourites_filter_query(self):
        """Returns a catalog query to get favourites
        """
        folder = self.get_favourites_container()
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


class AnnotationStorageFavouritesHandler(object):
    """ Annotation storage handler
    """
    implements(IFavouritesHandler)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.userid = api.user.get_current().id

    @property
    def storage(self):
        if getattr(self, '_storage', None) is None:
            annotation = IAnnotations(api.portal.get())
            if ANNOTATION_KEY not in annotation:
                annotation[ANNOTATION_KEY] = OOBTree()
            self._storage = annotation[ANNOTATION_KEY]

        return self._storage

    def create_favourites_container(self):
        self.storage.insert(self.userid, PersistentDict())

    def add_favourite(self, fav_id, title, remote_url):
        self.get_favourites_container()[fav_id] = PersistentDict(
            url=remote_url, title=title, pos=-1)

    def remove_favourite(self, fav_id):
        del self.get_favourites_container()[fav_id]

    def rename_favourite(self, fav_id, title):
        self.get_favourites_container()[fav_id]['title'] = title

    def order_favourites(self, fav_ids=[]):
        for i, fav_id in enumerate(fav_ids):
            if not fav_id:
                continue

            self.get_favourites_container()[fav_id]['pos'] = i

    def get_favourites_container(self):
        if not self.storage.get(self.userid):
            self.create_favourites_container()
        return self.storage.get(self.userid)

    def get_favourites(self):
        container = self.get_favourites_container()
        result = []

        for key, value in sorted(container.iteritems(),
                                 key=lambda item: item[1].get('pos')):
            result.append({'id': key,
                           'title': value.get('title'),
                           'url': value.get('url')})

        return result
