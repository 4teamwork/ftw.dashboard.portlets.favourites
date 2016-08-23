from ftw.dashboard.portlets.favourites.adapter import AnnotationStorageFavouritesHandler
from ftw.dashboard.portlets.favourites.adapter import DefaultFavouritesHandler
from ftw.dashboard.portlets.favourites.interfaces import IFavouritesHandler
from ftw.dashboard.portlets.favourites.testing import FAVOURITES_ANNOTATION_STORAGE_LAYER
from ftw.dashboard.portlets.favourites.tests import FunctionalTestCase
from zope.component import getMultiAdapter


class TestFavouriteDefaultHandler(FunctionalTestCase):

    def test_lookup_adapter_returns_default_handler(self):
        handler = getMultiAdapter(
            (self.portal, self.request),
            IFavouritesHandler)
        self.assertIsInstance(handler, DefaultFavouritesHandler)


class TestAnnotationHandler(FunctionalTestCase):
    layer = FAVOURITES_ANNOTATION_STORAGE_LAYER

    def test_lookup_adapter_returns_annotation_handler(self):
        handler = getMultiAdapter(
            (self.portal, self.request),
            IFavouritesHandler)
        self.assertIsInstance(handler, AnnotationStorageFavouritesHandler)
