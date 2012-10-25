# coding=UTF-8
from ftw.dashboard.portlets.favourites.adapter import \
    DefaultFavouritesHandler, NoHomeFolderError, RegistryKeyError
from ftw.dashboard.portlets.favourites.testing import FAVOURITES_ZCML_LAYER
from ftw.testing import MockTestCase
from mocker import ANY
from plone.registry.interfaces import IRegistry


class RemoveFavourite(MockTestCase):

    layer = FAVOURITES_ZCML_LAYER

    def setUp(self):
        super(RemoveFavourite, self).setUp()

        self.request = {}
        self.context = self.stub()

        self.folder = self.mocker.mock(count=False)
        self.expect(self.folder.manage_delObjects('valid')).result('ok')
        self.expect(
            self.folder.manage_delObjects('invalid')).throw(AttributeError)

        self.handler = self.mocker.patch(
            DefaultFavouritesHandler(self.context, self.request))
        self.expect(self.handler.get_favourites_folder()).result(self.folder)

    def test_valid_id(self):

        self.replay()

        result = self.handler.remove_favourite('valid')

        self.assertEquals(result, True)

    def test_invalid_id(self):

        self.replay()

        result = self.handler.remove_favourite('invalid')

        self.assertEquals(result, False)


class OrderFavourites(MockTestCase):

    layer = FAVOURITES_ZCML_LAYER

    def setUp(self):
        super(OrderFavourites, self).setUp()

        self.request = {}
        self.context = self.stub()

        self.rtool = self.mocker.mock(count=False)
        self.mock_utility(self.rtool, IRegistry)

        self.moved_objects = []

        self.obj_to_move = self.mocker.mock(count=False)
        self.expect(self.obj_to_move.reindexObject(idxs=ANY)).result(True)

        self.folder = self.mocker.mock(count=False)
        self.expect(self.folder.get('obj_1', ANY)).result(self.obj_to_move)
        self.expect(self.folder.get('obj_2', ANY)).result(self.obj_to_move)
        self.expect(self.folder.get('invalid', ANY)).result(None)
        self.expect(self.folder.moveObject(ANY, ANY)).call(
            lambda x, y: self.moved_objects.append(x))

        self.handler = self.mocker.patch(
            DefaultFavouritesHandler(self.context, self.request))
        self.expect(self.handler.get_favourites_folder()).result(self.folder)

    def test_all_valid(self):


        self.replay()

        self.handler.order_favourites(['obj_1', 'obj_2'])

        self.assertEquals(self.moved_objects, ['obj_1', 'obj_2'])

    def test_with_invalid_ids(self):

        self.replay()

        self.handler.order_favourites(['invalid', 'obj_1'])

        self.assertEquals(self.moved_objects, ['obj_1'])


class GetFavouriteFolderName(MockTestCase):

    layer = FAVOURITES_ZCML_LAYER

    def setUp(self):
        super(GetFavouriteFolderName, self).setUp()

        self.request = {}
        self.context = self.stub()

        self.rtool = self.mocker.mock(count=False)
        self.mock_utility(self.rtool, IRegistry)

        self.handler = DefaultFavouritesHandler(self.context, self.request)

    def test_with_registry(self):

        folder = object()
        self.expect(self.rtool.get(
            'ftw.dashboard.portlets.favourites.foldername')).result(folder)

        self.replay()

        result = self.handler.get_favourite_folder_name()

        self.assertEquals(folder, result)

    def test_without_registry(self):

        self.expect(self.rtool.get(
            'ftw.dashboard.portlets.favourites.foldername')).result(None)

        self.replay()

        self.assertRaises(
            RegistryKeyError, self.handler.get_favourite_folder_name)


class GetHomeFolder(MockTestCase):

    layer = FAVOURITES_ZCML_LAYER

    def setUp(self):
        super(GetHomeFolder, self).setUp()

        self.request = {}
        self.context = self.stub()

        self.mtool = self.mocker.mock(count=False)
        self.mock_tool(self.mtool, 'portal_membership')

        self.handler = DefaultFavouritesHandler(self.context, self.request)

    def test_with_homefolder(self):

        folder = object()
        self.expect(self.mtool.getHomeFolder()).result(folder)

        self.replay()

        result = self.handler.get_home_folder()

        self.assertEquals(folder, result)

    def test_without_homefolder(self):

        self.expect(self.mtool.getHomeFolder()).result(None)

        self.replay()

        self.assertRaises(NoHomeFolderError, self.handler.get_home_folder)
