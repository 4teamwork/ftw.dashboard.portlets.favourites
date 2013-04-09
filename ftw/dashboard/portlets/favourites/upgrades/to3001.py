from Products.CMFCore.utils import getToolByName
from ftw.dashboard.portlets.favourites.portlets import favourites
from ftw.upgrade import UpgradeStep
from plone.portlets.constants import USER_CATEGORY
from plone.portlets.interfaces import IPortletManager
from zope.component import queryUtility

# XXX could be removed in the next Release
# only used for problem-free portlet migration
from ftw.dashboard.portlets.favourites.browser.favourites import Assignment
Assignment


class ReplaceOldFavouritePortlets(UpgradeStep):

    def __call__(self):
        """Install and configure the new
        ftw.dashboard.portlets.favourites portlets.
        Also migrate old ftw.favorites portlets and remove old actions
        """
        # remove old favourite action
        actions_tool = getToolByName(self.portal, 'portal_actions')
        if 'addtofavorites' in actions_tool.document_actions:
            del actions_tool.document_actions['addtofavorites']

        # load profile again
        self.setup_install_profile(
            'profile-ftw.dashboard.portlets.favourites:default')

        self.migrate()

    def migrate(self):

        columns = ('plone.dashboard1',
                   'plone.dashboard2',
                   'plone.dashboard3',
                   'plone.dashboard4', )
        for managername in columns:
            manager = queryUtility(IPortletManager, name=managername)
            if not manager:
                continue
            category = manager.get(USER_CATEGORY, None)
            if not category:
                continue

            for mapping in category.values():
                for portletid in mapping.keys():
                    if portletid.startswith('favourites'):
                        del mapping[portletid]
                        mapping[portletid] = favourites.Assignment()
