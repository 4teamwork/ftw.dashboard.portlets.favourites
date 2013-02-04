$(function(){

    // Make favourites removeable
    if($('.documentEditable').length !== 0){
        $('.draggable-favourites').each(function(){
            $(this).children('.favourite-item').each(function(){
                if(!$(this).hasClass('portletItemEmpty')){
                    $(this).append('<a class="close favouriteRemove" title="entfernen"><img alt="remove" src = "'+portal_url+'/++resource++ftw.dashboard.portlets.favourites.resources/icon_remove_favourite.gif"/></a>');
                }
            });
        });
    }

    // Remove favourite
    $('.favouriteRemove').click(function(e){
        e.stopPropagation();
        e.preventDefault();
        var record = $(this).closest('dd');
        $.ajax({
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
            var items = $(portlet).find('dd');

            for(var i=0; i<items.length; i++) {
                data.push('favourites:list=' + items[i].id);
            }
            return data.join('&');
        };

        // send changes to server and update hashes
        $.ajax({
            type :      'POST',
            url :       './@@reorder_favourites',
            data :      customSerialization(this)
        });
    };

    $('dl.favourite-listing').sortable({
      items : 'dd.favourite-item',
      cursor: 'move',
      revert: true,
      tolerance : 'pointer',
      update : update_favourites_order
    });

});
