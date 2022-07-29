from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import Layer
from plone.testing import zca
from plone.testing.z2 import installProduct
from zope.configuration import xmlconfig


class FavouritesZCMLLayer(Layer):
    """A layer which only sets up the zcml, but does not start a zope
    instance.
    """

    defaultBases = (zca.ZCML_DIRECTIVES, )

    def testSetUp(self):
        self['configurationContext'] = zca.stackConfigurationContext(
            self.get('configurationContext'))

    def testTearDown(self):
        del self['configurationContext']


FAVOURITES_ZCML_LAYER = FavouritesZCMLLayer()


class FavouritesPloneLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ftw.dashboard.portlets.favourites
        xmlconfig.file(
            'configure.zcml',
            ftw.dashboard.portlets.favourites,
            context=configurationContext)
        installProduct(app, 'ftw.dashboard.portlets.favourites')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'ftw.dashboard.portlets.favourites:default')
        applyProfile(portal, 'plone.app.contenttypes:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])

        portal.invokeFactory("Folder", id="Members", title="Member")
        mtool = portal.portal_membership
        mtool.setMemberareaCreationFlag()
        mtool.createMemberArea(TEST_USER_ID)

FavouritesPloneFixture = FavouritesPloneLayer()
FAVOURITES_PLONE_LAYER = IntegrationTesting(
    bases=(
        FavouritesPloneFixture,
        set_builder_session_factory(functional_session_factory)),
    name="ftw.dashboard.portlets.favourites:Integration")


class FavouritesAnnotationStorageLayer(FavouritesPloneLayer):

    def setUpPloneSite(self, portal):
        super(FavouritesAnnotationStorageLayer, self).setUpPloneSite(portal)
        applyProfile(portal, 'ftw.dashboard.portlets.favourites:annotationstorage')

FavouritesAnnotationStorageFixture = FavouritesAnnotationStorageLayer()
FAVOURITES_ANNOTATION_STORAGE_LAYER = FunctionalTesting(
    bases=(
        FavouritesAnnotationStorageFixture,
        set_builder_session_factory(functional_session_factory)),
    name="ftw.dashboard.portlets.favourites:functional annotationstorage")
