# coding=UTF-8
from ftw.dashboard.portlets.favourites.testing import FAVOURITES_PLONE_LAYER
from unittest2 import TestCase
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from zope.component import getUtility, getMultiAdapter

from ftw.dashboard.portlets.favourites.portlets import favourites


class FavouriteTests(TestCase):

    layer = FAVOURITES_PLONE_LAYER

    def setUp(self):

        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_portlet_type_registered(self):

        portlet = getUtility(
            IPortletType, name='ftw.dashboard.portlets.favourites')
        self.assertEquals(portlet.addview, 'ftw.dashboard.portlets.favourites')

    def test_interfaces(self):

        portlet = favourites.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_renderer(self):

        context = self.portal
        request = self.request
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(
            IPortletManager, name='plone.dashboard1', context=self.portal)
        assignment = favourites.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, favourites.Renderer))

        self.failUnless(renderer.available,
                        "Renderer should be available by default.")


class TestRenderer(TestCase):

    layer = FAVOURITES_PLONE_LAYER

    def setUp(self):

        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def renderer(
        self,
        context=None,
        request=None,
        view=None,
        manager=None,
        assignment=None):

        context = context or self.portal
        request = request or self.request
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = getUtility(
            IPortletManager, name='plone.dashboard1', context=self.portal)
        assignment = favourites.Assignment()

        return getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)

    def test_render(self):

        self.portal.restrictedTraverse('add_to_favourites')()

        r = self.renderer(assignment=favourites.Assignment())
        r = r.__of__(self.portal)
        r.update()
        output = r.render()

        self.assertIn('<a href="" title="Plone site">', output)
