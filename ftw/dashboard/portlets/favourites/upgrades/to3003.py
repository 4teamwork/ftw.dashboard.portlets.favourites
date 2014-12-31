from ftw.upgrade import ProgressLogger
from ftw.upgrade import UpgradeStep


class MigrateFavouritesToFavorites(UpgradeStep):

    old_id = 'Favourites'
    new_id = 'Favorites'

    def __call__(self):
        mtool = self.portal.portal_membership
        member_ids = [member.getMemberId() for member in mtool.listMembers()]

        homefolders = [
            mtool.getHomeFolder(member_id) for member_id in member_ids]
        homefolders = filter(None, homefolders)

        for obj in ProgressLogger('Migrate favorites-folder name', homefolders):
            if not self.old_id in obj.objectIds():
                continue

            obj.manage_renameObject(id=self.old_id, new_id=self.new_id)
