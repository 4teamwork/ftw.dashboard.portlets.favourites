jq(function(){

    // Make favourites removeable
    if(jq('.documentEditable').length !== 0){
        jq('.draggable-favourites').each(function(){
            jq(this).children('.favourite-item').each(function(){
                if(!jq(this).hasClass('portletItemEmpty')){
                    jq(this).append('<a class="close favouriteRemove" title="entfernen"><img alt="remove" src = "'+portal_url+'/++resource++ftw.dashboard.portlets.favourites.resources/icon_remove_favourite.gif"/></a>');
                }
            });
        });
    };

    // Remove favourite
    jq('.favouriteRemove').click(function(e){
        e.stopPropagation();
        e.preventDefault();
        var record = jq(this).closest('dd');
        jq.ajax({
            type :      'POST',
            url :       './remove_from_favourites',
            data :      'uid='.concat(record.attr("id"))
        });
        record.hide().remove();
    });

    // Make favourites sortable
    var update_favourites_order = function(event, ui) {

        var customSerialization = function(portlet) {
            // prepare data
            var data = new Array();
            var items = jq(portlet).find('dd');

            for(var i=0; i<items.length; i++) {
                data.push('favourites:list=' + items[i].id);
            }
            return data.join('&');
        };

        // send changes to server and update hashes
        jq.ajax({
            type :      'POST',
            url :       './@@reorder_favourites',
            data :      customSerialization(this)
        });
    };

    jq('dl.favourite-listing').sortable({
      items : 'dd.favourite-item',
      cursor: 'move',
      revert: true,
      tolerance : 'pointer',
      update : update_favourites_order
    });

});
