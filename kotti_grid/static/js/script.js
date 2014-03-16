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
        grid_url = window.location.origin + "/@@gridbrowser";
        window.document.getElementById('grid-fieldname').value = field_name;
        window.open(grid_url, "Grid Browser", "width=800,height=600,status=yes,scrollbars=yes,resizable=yes");
    };

    window.gridbrowserdialog = {
        init: function() {
            var field = window.opener.document.getElementById('grid-fieldname').value;
            field = window.opener.document.getElementById(field)
            var url = field.getAttribute('data-url');
            var use = field.getAttribute('data-use');
            var custom_text = field.getAttribute('data-custom-text');
            var extra_style = field.getAttribute('data-extra-style');
            if (url !== null) $("input[name=url]").val(url);
            if (use !== null) $("select[name=use]").val(use);
            if (extra_style !== null) $("input[name=extra_style]").val(extra_style);
            if (custom_text !== null) tinyMCE.activeEditor.setContent(custom_text);
        },
        submit: function() {
            var url = $("input[name=url]").val();
            url = url.replace(window.location.origin, '');
            var use = $("select[name=use]").val();
            var custom_text = tinyMCE.activeEditor.getContent();
            var extra_style = $("input[name=extra_style]").val();
            var field_name = window.opener.document.getElementById('grid-fieldname').value;
            field = window.opener.document.getElementById(field_name)
            field.setAttribute('data-url', url);
            field.setAttribute('data-use', use);
            field.setAttribute('data-custom-text', custom_text);
            field.setAttribute('data-extra-style', extra_style);
            window.opener.reload_tile(field);
            return window.close();
        }
    };

    $('#gridbrowser_form .nav li a').click(function(event){
        var url = $(this).attr('href');
        url = url.replace('/@@gridbrowser', '');
        url = url.replace(window.location.origin, '');
        if (url.indexOf('..', url.length - 2) !== -1) {
            return true;
        }
        $("input[name=url]").val(url);
        var field_name = window.opener.document.getElementById('grid-fieldname').value;
        field = window.opener.document.getElementById(field_name)
        field.setAttribute('data-url', url);
        window.opener.reload_tile(field);
    });

    window.reload_tile = function(field) {
        var tile = $(field);
        var data = {};
        var url = tile.attr('data-url');
        var use = tile.attr('data-use');
        var custom_text = tile.attr('data-custom-text');
        var extra_style = tile.attr('data-extra-style');
        var size_x = tile.attr('data-sizex');
        data['url'] = url;
        data['use'] = use;
        data['custom_text'] = custom_text
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
    var slot = 'belowcontent';

    $.ajax({
        async: false,
        url: '/@@grid_settings',
        success: function(response) {
            resize_tiles = response['resize_tiles'];
            width = response['width'];
            height = response['height'];
            margin_x = response['margin_x'];
            margin_y = response['margin_y']
            slot = response['slot'];
        }
    });

    if(resize_tiles) {
        $(window).on('load', function() {
            if($('.gridster').length > 0) {
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
                        this.resize_widget($widget, data.size_x, data.size_y);
                    }, this));
                    this.generate_stylesheet();
                    return false;
                };

                $(window).resize( function() {
                    var window_width = $(window).width();
                    var cols = window.gridster.cols;
                    var new_width = $('.container').width() / cols - margin_x / (cols - 2);
                    var p = width * 100 / new_width;
                    var new_height = height * 100 / p;
                    window.gridster.resize_widget_dimensions({widget_base_dimensions: [new_width, new_height]});
                    if (slot = 'belowcontent') {
                        var conty = $('.container').get(0);
                        $('.gridster').offset({left: conty.getBoundingClientRect().left - 10})
                    }
                });
                $(window).resize();
            }
        });
    }
});

