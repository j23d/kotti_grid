$(function() {

    var qs = (function(a) {
      if (a == "") return {};
      var b = {};
      for (var i = 0; i < a.length; ++i)
      {
          var p=a[i].split('=');
          if (p.length != 2) continue;
          b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
      }
      return b;
    })(window.location.search.substr(1).split('&'));

    window.gridbrowser = function(field_name, url, type) {
        var grid_url;
        loc = window.location
        grid_url = loc.protocol + '//' + loc.host + "/@@gridbrowser";
        if (grid_url.indexOf("?") < 0) {
          grid_url = grid_url + "?type=" + type;
        } else {
          grid_url = grid_url + "&type=" + type;
        }
        window.document.getElementById('grid-fieldname').value = field_name;
        window.open(grid_url, "Grid Browser", "width=800,height=600,status=yes,scrollbars=yes,resizable=yes");
    };

    window.gridbrowserdialog = {
        init: function() {
          return $("select[name=image_scale]").change(function() {
            var image_scale_url;
            image_scale_url = "" + image_url + "/" + ($(this).val());
            $("#gridbrowser_image_preview").attr("src", image_scale_url);
            return $("input[name=url]").val(image_scale_url);
          });
        },
        submit: function(evt) {
            console.log(evt);
            var url = $("#gridbrowser_form input#url").val();
            var field = window.opener.document.getElementById('grid-fieldname').value;
            field = window.opener.document.getElementById(field)
            field.setAttribute('data-url', url);
            window.opener.reload_tile(field);
            return window.close();
        }
    };

    window.reload_tile = function(field) {
        var tile = $(field);
        var url = tile.attr('data-url');
        var params = '/@@tile-content?url=' + url;
        var size_x = tile.attr('data-sizex');
        if(size_x !== undefined) {
            params += '&size_x=' + size_x;
        }
        tile.children('.tile-content').load(params).fadeIn("slow");
    }


    function save_tiles() {
        var data = gridster.serialize()
        data = JSON.stringify(data, null, 2)
        $.post(
            'save-grid', {
                'tiles': data,
            },
            function (response) {
                if(!response === true) {
                    alert("Error while saving tiles: " + response);
                }
            }
        );
    }
    $('#save-tiles').click(function() {
        save_tiles();
        $("#tiles-saved-alert").fadeIn().delay(1000).fadeOut('slow');
    });

    $('#add-tile').popover({
            html: true,
            content: function(evt) {
                return popup('/@@add-tile', "tile-adder")
            }
    });

    function popup(link, div_id) {
        $.ajax({
            url: link,
            success: function(response){
                $('#'+div_id).html(response)}});
        return '<div id="'+ div_id +'">Loading...</div>'
    }

    window.rm_tile = function(tile) {
        window.gridster.remove_widget(tile);
        //save_tiles();
        $("#tile-removed-alert").fadeIn().delay(1000).fadeOut('slow');
    }

    var color_tile = undefined;
    $('.cpick').ColorPicker({
        onShow: function (colpkr) {
            color_tile = $(this).parent().parent();
            $(colpkr).fadeIn(500);
            return false;
        },
        onChange: function (hsb, hex, rgb) {
            color_tile.css('backgroundColor', '#' + hex);
        },
        // onHide: function (hsb, hex, rgb) {
        //     save_tiles();
        // }
    });

    window.gridster = $(".gridster ul").gridster({
        widget_margins: [10, 10],
        widget_base_dimensions: [150, 150],
        serialize_params: function($w, wgd) {
            return {
                //html: $w.html(),
                id: wgd.el[0].id,
                col: wgd.col,
                row: wgd.row,
                size_x: wgd.size_x,
                size_y: wgd.size_y,
                'class': $w.attr('class'),
                url: $w.attr('data-url'),
                type: $w.attr('data-type'),
                style: $w.attr('style')
            };
        },
        draggable: {
            stop: function(event, ui) {
                //save_tiles();
                event.preventDefault()
            }
        }
    }).data('gridster').disable();

});
