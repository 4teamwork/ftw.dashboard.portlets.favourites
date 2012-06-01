from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.testing.z2 import installProduct
from zope.configuration import xmlconfig
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles


class FavouritesPloneLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

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

        setRoles(portal, TEST_USER_ID, ['Manager'])

        portal.invokeFactory("Folder", id="Members", title="Member")
        mtool = portal.portal_membership
        mtool.setMemberareaCreationFlag()
        mtool.createMemberArea(TEST_USER_ID)
        self.home = mtool.getHomeFolder()

FavouritesPloneFixture = FavouritesPloneLayer()
FAVOURITES_PLONE_LAYER = IntegrationTesting(
    bases=(FavouritesPloneFixture, ),
    name="ftw.dashboard.portlets.favourites:Integration")
