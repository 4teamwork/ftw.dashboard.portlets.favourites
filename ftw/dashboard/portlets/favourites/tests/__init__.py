from ftw.dashboard.portlets.favourites.testing import FAVOURITES_PLONE_LAYER
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest import TestCase
from zope.event import notify
from zope.traversing.interfaces import BeforeTraverseEvent
import transaction


class FunctionalTestCase(TestCase):
    layer = FAVOURITES_PLONE_LAYER

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        notify(BeforeTraverseEvent(self.portal, self.portal.REQUEST))

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, list(roles))
        transaction.commit()
