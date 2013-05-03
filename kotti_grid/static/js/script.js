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

    // see https://github.com/ducksboard/gridster.js/pull/77
    var resize_tiles = false;
    var width = 150;
    var height = 150;
    var margin_x = 10;
    var margin_y = 10;
    $.ajax({
        async: false,
        url: '/@@grid_settings',
        success: function(response) {
            resize_tiles = response['resize_tiles'];
            width = response['width'];
            height = response['height'];
            margin_x = response['margin_x'];
            margin_y = response['margin_y'];
        }
    });
    if(resize_tiles) {
        window.onload = function() {
            window.gridster.resize_widget_dimensions = function(options) {
                if (options.widget_margins) {
                  this.options.widget_margins = options.widget_margins;
                }

                if (options.widget_base_dimensions) {
                  this.options.widget_base_dimensions = options.widget_base_dimensions;
                }

                this.min_widget_width  = (this.options.widget_margins[0] * 2)
                    + this.options.widget_base_dimensions[0];
                this.min_widget_height = (this.options.widget_margins[1] * 2)
                    + this.options.widget_base_dimensions[1];

                var serializedGrid = this.serialize();
                this.$widgets.each($.proxy(function(i, widget) {
                    var $widget = $(widget);
                    var data = serializedGrid[i];
                    this.resize_widget($widget, data.sizex, data.sizey);
                }, this));

                this.generate_grid_and_stylesheet();
                this.get_widgets_from_DOM();
                this.set_dom_grid_height();

                return false;
            };

            $(window).resize( function() {
                console.log("resize");
                var window_width = $(window).width();
                var cols = window.gridster.cols;
                var base_dimension_x = $('.container').width() / cols - margin_x / 2;
                var base_dimension_y = height;
                window.gridster.resize_widget_dimensions({widget_base_dimensions: [base_dimension_x, base_dimension_y]});
            });
            $(window).resize();
        }
    }

});

