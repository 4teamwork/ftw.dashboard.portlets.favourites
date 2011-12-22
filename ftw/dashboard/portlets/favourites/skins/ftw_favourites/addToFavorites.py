## Script (Python) "addtoFavorites"
##title=Add item to favourites (Plone Version)
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=

from Products.CMFPlone.utils import base_hasattr

RESPONSE = context.REQUEST.RESPONSE
homeFolder=context.portal_membership.getHomeFolder()
state = context.restrictedTraverse("@@plone_context_state")
view_url = '%s/%s' % (context.absolute_url(), state.view_template_id())
if not homeFolder:
    context.plone_utils.addPortalMessage(context.translate(u'Can\'t access home folder. Favorite is not added.', domain="ftw.dashboard.portlets.favourites"), 'error')
    return RESPONSE.redirect(view_url)

if not base_hasattr(homeFolder, 'Favorites'):
    homeFolder.invokeFactory('Folder', id='Favorites', title='Favorites')
    addable_types = ['Link']
    favs = homeFolder.Favorites
    if base_hasattr(favs, 'setConstrainTypesMode'):
        favs.setConstrainTypesMode(1)
        favs.setImmediatelyAddableTypes(addable_types)
        favs.setLocallyAllowedTypes(addable_types)

targetFolder = homeFolder.Favorites
new_id='fav_' + str(int( context.ZopeTime()))
myPath=context.portal_url.getRelativeUrl(context)
fav_id = targetFolder.invokeFactory('Link', id=new_id, title=context.TitleOrId(), remote_url=myPath)
if fav_id:
    favorite = getattr(targetFolder, fav_id, None)
else:
    favorite = getattr(targetFolder, new_id, None)

title = context.Title() or context.id

if isinstance(title, unicode):
    # The title is usually encoded in utf8, but in some dexterity
    # versions it may be unicode in certain circumstances.
    title = title.encode('utf-8')

if favorite:
    favorite.reindexObject()
    msg = context.translate(u'${title} has been added to your favourites.',
                            mapping={u'title' : title},
                            domain="ftw.dashboard.portlets.favourites",)
    context.plone_utils.addPortalMessage(msg)
else:
    msg = context.translate(u'There was a problem adding ${title} to your favourites.',
                            mapping={u'title' : title},
                            domain="ftw.dashboard.portlets.favourites",)
    context.plone_utils.addPortalMessage(msg, type='error')

return RESPONSE.redirect(view_url)
