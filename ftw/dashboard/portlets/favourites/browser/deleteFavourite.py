from Products.Five import BrowserView


class deleteFavourite(BrowserView):

    def __call__(self, *args, **kwargs):

        id = self.request.get('id')
        context = self.context
        homeFolder=context.portal_membership.getHomeFolder()
        favFolder = homeFolder.favourites

        favFolder.manage_delObjects([id, ])

        return ''
