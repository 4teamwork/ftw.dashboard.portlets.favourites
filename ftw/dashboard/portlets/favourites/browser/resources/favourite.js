jq(function(){
    jq('.favourite').each(function(){
        if(!jq('#regio-content').hasClass('documentEditable')){
            jq(this).children('.portletItem').each(function(){
                if(!jq(this).hasClass('portletItemEmpty')){
                    jq(this).append('<a class="close favouriteRemove" title="entfernen"><img alt="Widget entfernen" src = "++resource++icon_remove_box.gif"/></a>')
                }
            });
        }
    });


    //Remove Favourite
    jq('.favouriteRemove').click(function(){
        var item =  jq('.favouriteRemove:first').parents('.portletItem');
        var id = item.attr("id");
        jq.ajax({
            type :      'POST',
            url :       './ftw.dashboard.portlets.favourite.delete',
            data :      'id='.concat(id)
        });
        
        item.hide().remove();
    });
  
}); 