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
            var field = window.opener.document.getElementById('grid-fieldname').value;
            field = window.opener.document.getElementById(field)
            var url = field.getAttribute('data-url');
            var use = field.getAttribute('data-use');
            var extra_style = field.getAttribute('data-extra-style');
            if (url !== null) $("input[name=url]").val(url);
            if (use !== null) $("select[name=use]").val(use);
            if (extra_style !== null) $("input[name=extra_style]").val(extra_style);
        },
        submit: function() {
            var url = $("input[name=url]").val();
            var use = $("select[name=use]").val();
            var extra_style = $("input[name=extra_style]").val();
            var field = window.opener.document.getElementById('grid-fieldname').value;
            field = window.opener.document.getElementById(field)
            field.setAttribute('data-url', url);
            field.setAttribute('data-use', use);
            field.setAttribute('data-extra-style', extra_style);
            window.opener.reload_tile(field);
            return window.close();
        }
    };

    window.reload_tile = function(field) {
        var tile = $(field);
        var data = {};
        var url = tile.attr('data-url');
        var use = tile.attr('data-use');
        var extra_style = tile.attr('data-extra-style');
        var size_x = tile.attr('data-sizex');
        data['url'] = url;
        data['use'] = use;
        data['extra_style'] = extra_style
        var uri = '/@@tile-content';
        if(size_x !== undefined) {
            data['size_x'] = size_x;
        }
        tile.children('.tile-content').load(uri, data).fadeIn("slow");
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
                } else {
                    window.location.href = window.location.href;
                }
            }
        );
    }
    $('#save-tiles').click(function() {
        save_tiles();
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

    if ($('.cpick').length > 0) {
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
    }
});
