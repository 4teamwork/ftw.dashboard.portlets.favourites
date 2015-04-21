import json
from unittest2 import TestCase

from ftw.dashboard.portlets.favourites.testing import FAVOURITES_PLONE_LAYER


class RenameFavouriteTests(TestCase):

    layer = FAVOURITES_PLONE_LAYER

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.home = self.portal.portal_membership.getHomeFolder()

    def test_rename_favourite(self):
        self.portal.invokeFactory("Folder", id="test_folder", title="Test Folder")
        self.portal.test_folder.restrictedTraverse('add_to_favourites').add()

        favourite = self.home['Favourites'].listFolderContents()[0]

        new_title = "Renamed Test Folder"
        self.portal.REQUEST.set('uid', favourite.getId())
        self.portal.REQUEST.set('title', new_title)

        ajax_rename_view = self.portal.test_folder.restrictedTraverse('rename_favourite')
        response = json.loads(ajax_rename_view())

        self.assertEqual(response['success'], True)
        self.assertEqual(
            self.home['Favourites'].listFolderContents()[0].title,
            new_title
        )
