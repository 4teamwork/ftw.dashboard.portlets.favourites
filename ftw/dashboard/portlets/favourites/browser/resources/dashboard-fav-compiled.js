jQuery(function(e){var t,i,a,o=e("body").attr("data-portal-url"),n=e(".portlet.favourite-listing").data("authenticator-token"),r=null,u={escape:27,enter:13},s='<a class="close favouriteRename" title="umbenennen"><img alt="rename" src = "'+o+'/++resource++ftw.dashboard.portlets.favourites.resources/icon_rename_favourite.gif"/></a>',f='<a class="close favouriteRemove" title="entfernen"><img alt="remove" src = "'+o+'/++resource++ftw.dashboard.portlets.favourites.resources/icon_remove_favourite.gif"/></a>',c='<a class="close favouriteSubmit" title="speichern"><img alt="save" src = "'+o+'/++resource++ftw.dashboard.portlets.favourites.resources/icon_submit_favourite.gif"/></a>',l=function(t){t?t.hasClass("portletItemEmpty")||(t.append(f),t.append(s),t.append(c)):e(".draggable-favourites").each(function(){e(this).children(".favourite-item").each(function(){e(this).hasClass("portletItemEmpty")||(e(this).append(f),e(this).append(s),e(this).append(c))})}),e(".favouriteRemove").click(function(e){e.stopPropagation(),e.preventDefault(),d.call(this,e)}),e(".favouriteRename").click(function(e){e.stopPropagation(),e.preventDefault(),b.call(this)}),e(".favouriteSubmit").click(function(e){e.stopPropagation(),e.preventDefault(),p.call(this)})},d=function(t){t.stopPropagation(),t.preventDefault();var i=e(this).closest("dd");r&&r.is(i)&&(r=null);e.ajax({type:"POST",url:"./remove_from_favourites",data:"uid="+i.attr("id"),beforeSend:function(e){e.setRequestHeader("X-CSRF-TOKEN",n)}});i.hide().remove()},v=function(){r=null,e.ajax({url:window.location.href,beforeSend:function(e){e.setRequestHeader("X-CSRF-TOKEN",n)},success:function(i){a.empty().html(e("#"+t,i).html()),l(a),$editButton=a.find(".favouriteRename"),$submitButton=a.find(".favouriteSubmit"),$editButton.show(),$submitButton.hide()},error:function(){g()}})},p=function(){e.ajax({type:"POST",url:"./rename_favourite",data:"uid="+t+"&title="+i.val(),beforeSend:function(e){e.setRequestHeader("X-CSRF-TOKEN",n)},success:function(){v()},error:function(){g()}})},m=function(e){if(t){switch(e.keyCode||e.which){case u.enter:p();break;case u.escape:v()}}},h=function(t){var a=e(t.target);a.is(i)||a.parent().hasClass("favouriteRename")||v()},b=function(){if(!r&&(a=e(this).closest("dd"),$editButton=a.find(".favouriteRename"),$submitButton=a.find(".favouriteSubmit"),r=a,0===a.find("input").length)){var o=a.find("span"),n=o.find("a"),u=n.text().trim();t=a.attr("id"),i=e('<input type="text" name="rename_favourite" />').attr("id",t).val(u),o.hide(),$editButton.hide(),$submitButton.show(),a.append(i).fadeIn("fast"),i.focus().select(),i.off("keyup").on("keyup",m),e(document).off("click").on("click",h)}},g=function(){setTimeout(function(){window.location.reload()},1e3)},R=function(t,i){e.ajax({type:"POST",url:"./@@reorder_favourites",data:function(t){for(var i=[],a=e(t).find("dd"),o=0;o<a.length;o++)i.push("favourites:list="+a[o].id);return i.join("&")}(this),beforeSend:function(e){e.setRequestHeader("X-CSRF-TOKEN",n)}})};e("dl.favourite-listing").sortable({items:"dd.favourite-item",cursor:"move",revert:!0,tolerance:"pointer",update:R}),l();var S=e(".favourite-item"),w=function(t){var i=S.filter(function(i,a){return e("a",a).html().trim().toLowerCase().indexOf(t.trim().toLowerCase())>=0});e(".draggable-favourites").html(i),""===t.trim()&&e(".draggable-favourites").html(S)};e("#favourite_filter").keyup(function(){w(e(this).val())})}),define("favourite",function(){}),require(["favourite"],function(e){}),define("main",function(){});