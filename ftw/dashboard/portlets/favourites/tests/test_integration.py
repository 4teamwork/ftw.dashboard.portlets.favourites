from ftw.dashboard.portlets.favourites.adapter import DefaultFavouritesHandler
from ftw.dashboard.portlets.favourites.interfaces import IFavouritesHandler
from ftw.dashboard.portlets.favourites.testing import FAVOURITES_PLONE_LAYER
from unittest import TestCase
from zope.component import getMultiAdapter


class FavouriteTests(TestCase):

    layer = FAVOURITES_PLONE_LAYER

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.home = self.portal.portal_membership.getHomeFolder()

    def test_registry(self):
        value = self.portal.portal_registry.get(
            "ftw.dashboard.portlets.favourites.foldername")

        self.assertEquals(value, u"Favourites")

    def test_adapter_registration(self):

        handler = getMultiAdapter((self.portal, self.request),
            IFavouritesHandler)

        self.assertTrue(isinstance(handler, DefaultFavouritesHandler))

    def test_integration(self):

        self.portal.invokeFactory(
            "Folder", id="test_folder", title="Test Folder")

        # Adding
        self.portal.restrictedTraverse('add_to_favourites').add()
        self.portal.test_folder.restrictedTraverse('add_to_favourites').add()

        content = self.home['Favourites'].listFolderContents()

        self.assertTrue(len(content) == 2)
        self.assertEquals('Test Folder', content[1].title)
        self.assertEquals('test_folder', content[1].remoteUrl)

        # Ordering
        links = [link.id for link in content]
        links.reverse()
        self.request['favourites'] = links

        self.assertEquals(
            content, self.home['Favourites'].listFolderContents())

        self.portal.restrictedTraverse('reorder_favourites')()

        self.assertNotEquals(
            content, self.home['Favourites'].listFolderContents())

        # Removing
        self.request['uid'] = content[0].id

        self.portal.restrictedTraverse('remove_from_favourites')()

        self.assertTrue(len(self.home['Favourites'].listFolderContents()) == 1)

        # Cleanup
        self.portal.manage_delObjects(['test_folder'])
        self.home.Favourites.manage_delObjects(
            [link.id for link in self.home['Favourites'].listFolderContents()])
