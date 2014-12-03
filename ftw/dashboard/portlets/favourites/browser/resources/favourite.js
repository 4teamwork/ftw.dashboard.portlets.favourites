jQuery(function($) {

  var favouriteId;
  var $titleInputField;
  var $favouriteContainer;
  var $editing = null;
  var keyCodes = {
    'escape': 27,
    'enter': 13
  };
  var editFavouriteElement = '<a class="close favouriteRename" title="umbenennen"><img alt="rename" src = "' + portal_url + '/++resource++ftw.dashboard.portlets.favourites.resources/icon_rename_favourite.gif"/></a>';
  var removeFavouriteElement = '<a class="close favouriteRemove" title="entfernen"><img alt="remove" src = "' + portal_url + '/++resource++ftw.dashboard.portlets.favourites.resources/icon_remove_favourite.gif"/></a>';
  var submitFavouriteElement = '<a class="close favouriteSubmit" title="speichern"><img alt="save" src = "' + portal_url + '/++resource++ftw.dashboard.portlets.favourites.resources/icon_submit_favourite.gif"/></a>';


  var makeFavouritesEditable = function($element) {
    if ($('.documentEditable').length !== 0) {
      if ($element) {
        if (!$element.hasClass('portletItemEmpty')) {
          $element.append(removeFavouriteElement);
          $element.append(editFavouriteElement);
          $element.append(submitFavouriteElement);
        }
      } else {
        $('.draggable-favourites').each(function() {
          $(this).children('.favourite-item').each(function() {
            if (!$(this).hasClass('portletItemEmpty')) {
              $(this).append(removeFavouriteElement);
              $(this).append(editFavouriteElement);
              $(this).append(submitFavouriteElement);
            }
          });
        });
      }

    }

    $('.favouriteRemove').off('click').on('click', function(event) {
      removeFavourite.call(this, event);
    });

    $('.favouriteRename').off('click').on('click', function() {
      makeFavouriteRenameable.call(this);
    });

    $('.favouriteSubmit').off('click').on('click', function() {
      renameFavourite.call(this);
    });

  };

  var removeFavourite = function(event) {
    event.stopPropagation();
    event.preventDefault();
    var $record = $(this).closest('dd');
    if ($editing && $editing.is($record)) {
      $editing = null;
    }
    var removeResponse = $.ajax({
      type: 'POST',
      url: './remove_from_favourites',
      data: 'uid=' + $record.attr("id")
    });
    $record.hide().remove();
  };

  var reloadFavourite = function() {
    $editing = null;
    var reloadResponse = $.get(window.location.href);
    reloadResponse.done(function(data) {
      $favouriteContainer.empty().html($('#' + favouriteId, data).html());
      makeFavouritesEditable($favouriteContainer);
      $editButton = $favouriteContainer.find('.favouriteRename');
      $submitButton = $favouriteContainer.find('.favouriteSubmit');
      $editButton.show();
      $submitButton.hide();
    });

    reloadResponse.fail(function() {
      reloadPage();
    });

    return false;
  };

  var renameFavourite = function() {
    var renameResponse = $.ajax({
      type: 'POST',
      url: './rename_favourite',
      data: 'uid=' + favouriteId + '&title=' + $titleInputField.val()
    });
    renameResponse.done(function() {
      reloadFavourite();
    });
    renameResponse.fail(function() {
      reloadPage();
    });
  };

  var handleFavouriteRename = function(event) {
    if (favouriteId) {
      var code = event.keyCode || event.which;
      switch (code) {
        case keyCodes.enter:
          renameFavourite();
          break;
        case keyCodes.escape:
          reloadFavourite();
          break;
        default:
          // Do nothing
      }
    }
  };

  var handleLooseFocus = function(event) {
    var $target = $(event.target);
    if (!($target.is($titleInputField) || $target.parent().hasClass('favouriteRename'))) {
      reloadFavourite();
    }
  };

  var makeFavouriteRenameable = function() {
    if (!$editing) {
      $favouriteContainer = $(this).closest('dd');
      $editButton = $favouriteContainer.find('.favouriteRename');
      $submitButton = $favouriteContainer.find('.favouriteSubmit');
      $editing = $favouriteContainer;
      if ($favouriteContainer.find('input').length === 0) {
        var $titleWrapper = $favouriteContainer.find('span');
        var $title = $titleWrapper.find('a');
        var titleText = $title.text().trim();
        favouriteId = $favouriteContainer.attr("id");
        $titleInputField = $('<input type="text" name="rename_favourite" />').attr('id', favouriteId).val(titleText);
        $titleWrapper.hide();
        $editButton.hide();
        $submitButton.show();
        $favouriteContainer.append($titleInputField).fadeIn('fast');
        $titleInputField.focus().select();
        $titleInputField.off('keyup').on('keyup', handleFavouriteRename);
        $(document).off('click').on('click', handleLooseFocus);
      }

    }

  };

  // FF-hack
  var reloadPage = function() {
    setTimeout(function() {
      window.location.reload();
    }, 1000);
  };

  // Make favourites sortable
  var update_favourites_order = function(event, ui) {

    var customSerialization = function(portlet) {
      // prepare data
      var data = [];
      var items = $(portlet).find('dd');

      for (var i = 0; i < items.length; i++) {
        data.push('favourites:list=' + items[i].id);
      }
      return data.join('&');
    };

    // send changes to server and update hashes
    $.ajax({
      type: 'POST',
      url: './@@reorder_favourites',
      data: customSerialization(this)
    });
  };

  $('dl.favourite-listing').sortable({
    items: 'dd.favourite-item',
    cursor: 'move',
    revert: true,
    tolerance: 'pointer',
    update: update_favourites_order
  });

  makeFavouritesEditable();

});
