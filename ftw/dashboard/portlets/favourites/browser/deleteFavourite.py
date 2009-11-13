from Products.Five import BrowserView
from ftw.dashboard.portlets.favourites.fav_folder import get_fav_folder

class deleteFavourite(BrowserView):

    def __call__(self,*args, **kwargs):
        
        id = self.request.get('id');
        favFolder = get_fav_folder(self.context)

        favFolder.manage_delObjects([id,])
           
        return '';
