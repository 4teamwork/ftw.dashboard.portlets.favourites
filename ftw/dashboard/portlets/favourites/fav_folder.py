#! -*- coding: UTF-8 -*-

def get_fav_folder(context):
    """ Returns the the favorite folder 
    trying get this names frm user home folder:
    favourites, favorites, Favorites and Favourites
    WARNING: the same implementation is in:
    skins/ftw*/addtofavourites.py
    """

    homeFolder = context.portal_membership.getHomeFolder()

    for fav_folder_name in ['favourites', 'Favourites', 'Favorites', 'favorites']:
        if hasattr(homeFolder, fav_folder_name):
            return getattr(homeFolder, fav_folder_name, None)

