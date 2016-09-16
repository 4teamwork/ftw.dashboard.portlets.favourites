# coding=UTF-8
from ftw.dashboard.portlets.favourites.adapter import AnnotationStorageFavouritesHandler
from ftw.dashboard.portlets.favourites.adapter import DefaultFavouritesHandler
from ftw.dashboard.portlets.favourites.interfaces import IFavouritesHandler
from ftw.dashboard.portlets.favourites.testing import FAVOURITES_ANNOTATION_STORAGE_LAYER
from ftw.dashboard.portlets.favourites.tests import FunctionalTestCase
from persistent.dict import PersistentDict
from zope.component import getMultiAdapter


class TestFavouriteDefaultHandler(FunctionalTestCase):

    def test_lookup_adapter_returns_default_handler(self):
        handler = getMultiAdapter(
            (self.portal, self.request),
            IFavouritesHandler)
        self.assertIsInstance(handler, DefaultFavouritesHandler)


class TestAnnotationHandler(FunctionalTestCase):
    layer = FAVOURITES_ANNOTATION_STORAGE_LAYER

    def setUp(self):
        super(TestAnnotationHandler, self).setUp()
        self.handler = getMultiAdapter(
            (self.portal, self.request),
            IFavouritesHandler)

    def test_lookup_adapter_returns_annotation_handler(self):
        self.assertIsInstance(self.handler, AnnotationStorageFavouritesHandler)

    def test_favourites_container_gets_created(self):
        self.handler.create_favourites_container()

        self.assertEqual(
            [('test_user_1_', PersistentDict()), ],
            [item for item in self.handler.storage.iteritems()])

    def test_favourites_container_gets_returned(self):
        self.assertEqual(
            PersistentDict(), self.handler.get_favourites_container())

    def test_favourite_gets_added(self):
        self.handler.add_favourite("id_1", "jamesö", "url/bond")

        self.assertEqual(
            PersistentDict(
                id_1=PersistentDict(title="jamesö", url="url/bond", pos=-1)),
            self.handler.get_favourites_container())

    def test_get_favourite_returns_items_as_list(self):
        self.handler.add_favourite("id_1", "james", "url/bond")

        self.assertEqual(
            [
                dict(id="id_1", title="james", url="url/bond"),
            ],
            self.handler.get_favourites())

    def test_order_favourites_sorts_correctly(self):
        self.handler.add_favourite("id_1", "james", "url/bond")
        self.handler.add_favourite("id_2", "chuck", "url/norris")
        self.handler.add_favourite("id_3", "tony", "url/stark")

        self.handler.order_favourites(['id_3', 'id_2', 'id_1'])

        self.assertEqual(
            [
                dict(id="id_3", title="tony", url="url/stark"),
                dict(id="id_2", title="chuck", url="url/norris"),
                dict(id="id_1", title="james", url="url/bond")
            ],
            self.handler.get_favourites())

    def test_favourites_get_renamed_correctly(self):
        self.handler.add_favourite("id_1", "james", "url/bond")

        self.handler.rename_favourite("id_1", "michael")

        self.assertEqual(
            "michael",
            self.handler.get_favourites_container()["id_1"]["title"])

    def test_favourites_get_deleted_correctly(self):
        self.handler.add_favourite("id_1", "james", "url/bond")

        self.handler.remove_favourite("id_1")

        self.assertEqual(
            [],
            self.handler.get_favourites())
