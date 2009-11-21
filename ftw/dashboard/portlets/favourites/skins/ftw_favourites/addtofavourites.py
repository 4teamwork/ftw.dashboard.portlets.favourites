## Script (Python) "addtofavourites"
##title=Add item to favourites (Plone Version)
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=

from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone import PloneMessageFactory as _

RESPONSE = context.REQUEST.RESPONSE
homeFolder=context.portal_membership.getHomeFolder()
state = context.restrictedTraverse("@@plone_context_state")
view_url = '%s/%s' % (context.absolute_url(), state.view_template_id())
if not homeFolder:
    context.plone_utils.addPortalMessage(_(u'Can\'t access home folder. favourite is not added.'), 'error')
    return RESPONSE.redirect(view_url)

targetFolder = None
for fav_folder_name in ['favourites', 'Favourites', 'Favorites', 'favorites']:
    if hasattr(homeFolder, fav_folder_name):
        targetFolder =getattr(homeFolder, fav_folder_name, None)
	break

if not targetFolder:
    homeFolder.invokeFactory('Folder', id='favourites', title='favourites')
    addable_types = ['Favorite']
    targetFolder = homeFolder.favourites
    if base_hasattr(targetFolder, 'setConstrainTypesMode'):
        targetFolder.setConstrainTypesMode(1)
        targetFolder.setImmediatelyAddableTypes(addable_types)
        targetFolder.setLocallyAllowedTypes(addable_types)
        targetFolder.manage_addProperty('layout','fav_folder_view',type='string')

new_id='fav_' + str(int( context.ZopeTime()))
fav_id = targetFolder.invokeFactory('Favorite', id=new_id, title=context.TitleOrId(), remote_url='resolveUid/%s' % context.UID())
favourite = getattr(targetFolder, fav_id, None)

if favourite:
    favourite.reindexObject()
    msg = _(u'${title} has been added to your favourites.',
            mapping={u'title' : context.title_or_id()})
    context.plone_utils.addPortalMessage(msg)
else:
    msg = _(u'There was a problem adding ${title} to your favourites.',
            mapping={u'title' : context.title_or_id()})

return RESPONSE.redirect(view_url)
favourites
