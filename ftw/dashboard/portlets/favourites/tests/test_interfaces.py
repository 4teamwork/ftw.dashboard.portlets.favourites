from ftw.dashboard.portlets.favourites.adapter import AnnotationStorageFavouritesHandler
from ftw.dashboard.portlets.favourites.adapter import DefaultFavouritesHandler
from ftw.dashboard.portlets.favourites.interfaces import IFavouritesHandler
from unittest import TestCase
from zope.interface.verify import verifyClass


class TestVerifyInterfaces(TestCase):

    def test_favourites_handler(self):
        verifyClass(IFavouritesHandler, DefaultFavouritesHandler)

    def test_favourites_annotation_storage(self):
        verifyClass(IFavouritesHandler, AnnotationStorageFavouritesHandler)
