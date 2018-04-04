$("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

var timeFormat = function (secs) {
    if (secs == undefined || isNaN(secs)) {
        return '0:00';
    }
    secs = Math.round(secs);
    var mins = '' + Math.round(secs / 60);
    secs = '' + (secs % 60);
    if (secs.length < 2) {
        secs = '0' + secs;
    }
    if (secs > 0)
        secs -= 1;
    return mins + ':' + secs;
};

$('.jp-shuffle').click(function () {
    var jpPlayer = $('.jp-audio');
    if (jpPlayer.hasClass('jp-state-shuffled')) {
        jpPlayer.removeClass('jp-state-shuffled');
    }
    else {
        jpPlayer.addClass('jp-state-shuffled');
    }
});

$('.jp-next').click(function () {
    var nextVar = $(next).closest('tr').next('tr');
    nextVar.click();
});

$('.jp-previous').click(function () {
    var prevVar = $(next).closest('tr').prev('tr');
    prevVar.click();
});

$('#importModal').click(function () {
    $('#modal').modal({
        backdrop: 'static',
        keyboard: false
    })
});

$('#closeModal').click(function () {
    $('#files').val('')
});

function importMusic(e) {
    $('#modal').modal({backdrop: 'static', keyboard: false});
    var formData = new FormData();
    var files = e.parentElement.children[0].files;
    for (var i = 0; i < files.length; i++)
        formData.append("file[]", files[i]);
    ajaxImport(formData, "/import", "importMusic");
}

function openDialog(e) {
    $("#dialog").dialog({
        autoOpen: true,
        resizable: false,
        draggable: false,
        modal: true,
        position: {my: 'left top', at: 'left bottom', of: e.target}
    });
}
function click_Playlist(e) {
    var clickedElement = e.parentElement;
    $("#dialogPlaylist").dialog({
        title: 'Rename ' + clickedElement.className,
        autoOpen: true,
        resizable: false,
        draggable: false,
        modal: true,
        position: {my: 'left top', at: 'left bottom', of: clickedElement}
    });
}

function ajaxImport(jsonData, pfad, bedeutung) {
    $.ajax({
        url: pfad,
        data: jsonData,
        error: function () {
            alert('Fehler')
        },
        success: function (data) {
            if (bedeutung == 'importMusic') {
                $('#modal').modal('hide');
                $('#fileModal').modal({
                    backdrop: 'static',
                    keyboard: false
                });
                $('#fileList').text(data.result);
                $('#files').val('');
                router.navigate('/', true);
                router.navigate('item/query/', true);
            }
        },
        type: 'post',
        processData: false,
        contentType: false
    });
}

function ajaxCall(jsonData, pfad, bedeutung) {
    $.ajax({
        url: pfad,
        data: jsonData,
        error: function () {
            alert('Fehler')
        },
        success: function (data) {
            if (bedeutung === 'SongToPlaylist') {
                alert("Song has been added to playlist " + data.result);
            } else if (bedeutung === 'CreatePlaylist') {
                if (data.result === 'playlistexist') {
                    alert("Playlist already exists!");
                }
                else {
                    $('#Playlist').val('');
                    $('#PlaylistOrder').load("/#item/query #PlaylistElements");
                    $('#playlistListe').load("/#item/query #addtoPlaylist");
                    alert('The Playlist ' + data.result + ' was sucessfully created!');
                }
            } else if (bedeutung === 'deletePlaylist') {
                $('div.' + data.result.replace(/ /g, ".")).remove();
                $('#PlaylistOrder').load("/#item/query #PlaylistElements");
                $('#playlistListe').load("/#item/query #addtoPlaylist");
                router.navigate('item/query/', true);
                alert('The Playlist ' + data.result + ' was sucessfully deleted!');
            } else if (bedeutung === 'changePlaylist') {
                $('div.' + data.result.oldVal.replace(/ /g, ".")).remove();
                $('#PlaylistOrder').load("/#item/query #PlaylistElements");
                $('#playlistListe').load("/#item/query #addtoPlaylist");
                $('#editTextBox').val("");
                $('#dialogPlaylist').dialog("close");
                alert('The Playlist ' + data.result.oldVal + ' was changes to ' + data.result.newVal);
            } else {
                $('.star' + data.result + ' #star' + data.result).remove();
                $('td #star' + data.result).clone(true).appendTo('span .star' + data.result);
            }
        },
        type: 'post'
    });
}

$(function () {

    var BeetsRouter = Backbone.Router.extend({
        routes: {
            "item/query/:query": "itemQuery"
        },
        itemQuery: function (query) {
            var queryURL = query.split(/\s+/).map(encodeURIComponent).join('/');
            $('#view').load("/#playlist/query/" + queryURL + " #view", function () {
                $.getJSON('/item/query/' + queryURL, function (data) {
                    var models = _.map(
                        data['results'],
                        function (d) {
                            return new Item(d);
                        }
                    );
                    var results = new Items(models);
                    app.showItems(results);
                });
            });
        }
    });
    router = new BeetsRouter();

    var AppPlaylistView = Backbone.Router.extend({
        routes: {
            "playlist/query/:query": "itemQuery"
        },
        itemQuery: function (query) {
            var queryURL = query.split(/\s+/).map(encodeURIComponent).join('.');
            $('#view').load("/#playlist/query/" + queryURL + " #view", function () {
                $.getJSON('playlist/query/' + queryURL, function (data) {
                    var models = _.map(
                        data['results'],
                        function (d) {
                            return new Item(d);
                        }
                    );
                    var results = new Items(models);
                    $('.foot-stat').load("/playlist_link/" + query + " .item-count");
                    app.showItems(results);
                });
            });
        }
    });
    var playlist = new AppPlaylistView();

    var Item = Backbone.Model.extend({
        urlRoot: '/item'
    });
    var Items = Backbone.Collection.extend({
        model: Item
    });

    var ItemEntryView = Backbone.View.extend({
        tagName: "tr",
        template: _.template($('#item-entry-template').html()),
        events: {
            'click': 'select',
            "touchstart": 'select'
        },
        initialize: function () {
            this.playing = false;
        },
        render: function () {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        },
        select: function (e) {
            if (e.target.getAttribute('id') !== 'more' &&
                e.target.parentNode.getAttribute('class') != 'rate' &&
                e.target.getAttribute('id') !== 'action' &&
                e.target.getAttribute('id') !== 'rate' &&
                e.target.getAttribute('class') !== 'rate') {

                var selected = $(this).hasClass("highlight");
                $("tr").removeClass("highlight");
                if (!selected)
                    $(this.el).addClass("highlight");
                app.selectItem(this.model, e.currentTarget);
            }
            else if (e.target.getAttribute('id') === 'more') {
                openDialog(e);
                ID = this.model.id;
            }
        }
    });


    var AppView = Backbone.View.extend({
        el: $('body'),
        events: {
            'click #search': 'querySubmit',
            'click #submitplaylist': 'queryClick',
            'click #home': 'queryHomeClick',
            'click #Delete_the_Playlist': 'queryDeletePlaylist',
            'click #renamePlaylistButton': 'queryRenamePlaylist',
            'click #sendPlaylist': 'sendPlaylist',
            'click #reset': 'resetRating',
            'click #savePlaylist': 'savePlaylist'

        },
        loadList: function () {
            router.navigate('item/query/', true);
        }, savePlaylist: function (ev) {
            ev.preventDefault();
            var input = document.getElementById('Playlist').value;
            var only_this = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789- ";
            if (input.length === 0) {
                alert("Bitte einen Wert eintragen!");
                return false;
            }
            for (var i = 0; i < input.length; i++) {
                var badInput = String(input.charAt(i));
                if (only_this.indexOf(input.charAt(i)) < 0 || input.charAt(0) === " ") {
                    alert('Bitte keine Sonderzeichen verwenden. Das Sonderzeichen ' + badInput + ' ist nicht erlaubt');
                    return false;
                }
            }

            var jsonData = {
                PListName: input
            };
            ajaxCall(jsonData, '/create_playlist', 'CreatePlaylist');

        }, resetRating: function (ev) {
            ev.preventDefault();
            var jsonData = {
                id: 'star' + ID,
                name: 0
            };
            $('#star' + ID).raty('score', 0);
            ajaxCall(jsonData, '/rating', 'StarBewertung');

        }, sendPlaylist: function (ev) {
            ev.preventDefault();
            var jsonData = {
                PlayLID: $('#addtoPlaylist').val(),
                Song: ID
            };
            ajaxCall(jsonData, '/add_to_playlist', 'SongToPlaylist');

        }, queryRenamePlaylist: function (ev) {
            ev.preventDefault();
            var playlistName = $('#dialogPlaylist').dialog('option', 'title').split(" ")[1];
            jsonData = {
                oldVal: playlistName,
                newVal: $('#editTextBox').val()
            };
            ajaxCall(jsonData, "/rename_Playlist", "changePlaylist");
        }, queryDeletePlaylist: function (ev) {
            ev.preventDefault();
            jsonData = {
                PlayLID: ev.target.parentElement.className,
                Song: '1'
            };
            ajaxCall(jsonData, "/delete_Playlist", "deletePlaylist");
        }, queryClick: function (ev) {
            ev.preventDefault();
            playlist.navigate('playlist/query/' + encodeURIComponent(ev.currentTarget.name), true);
        },
        queryHomeClick: function (ev) {
            ev.preventDefault();
            router.navigate('item/query/', true);
            $('.foot-stat').load("/ .item-count");
        },
        querySubmit: function (ev) {
            ev.preventDefault();
            var query = $('#query');
            if (query.val() != '') {
                router.navigate('item/query/' + encodeURIComponent(query.val()), true);
                $('.foot-stat').load("/item_link/" + encodeURIComponent(query.val()) + " .item-count");
                query.val("");
            }
            else {
                alert("Please insert a charackter in query textbox!")
            }
        },
        initialize: function () {
            this.loadList();
        },
        showItems: function (items) {
            rateItem = items;
            $('#results').empty();
            items.each(function (item) {
                var view = new ItemEntryView({model: item});
                item.entryView = view;
                $('#results').append(view.render().el);
            });
            if (!$.fn.DataTable.isDataTable('#table')) {
                $('#table').DataTable({
                    responsive: true,
                    "paging": false,
                    "info": false,
                    "filter": false,
                    "columns": [
                        {"width": "1%"},
                        {"width": "30%"},
                        {"width": "30%"},
                        {"width": "5%"},
                        {"width": "25%"},
                        {"width": "9%"}
                    ]
                });
            }
            $.fn.raty.defaults.path = 'static/images';
            var tableRows = $('table tbody tr');
            for (var i = 0; i < tableRows.length; i++) {
                var starID = tableRows.find('td:last')[i].children[0].id;
                $('#' + starID).raty({
                    score: function () {
                        return rateItem.models[i].attributes.rating
                    },
                    click: function (score) {
                        var url = '/rating';
                        var jsonData = {
                            id: this.id,
                            name: score
                        };
                        ajaxCall(jsonData, url, 'StarBewertung')
                    }
                });
            }
        },
        selectItem: function (item, nextItem) {
            next = nextItem;
            url1 = '/play/' + item.get('id') + '/file';
            title = item._previousAttributes.title;
            var urlPath = window.location.origin + url1;
            jQuery.get(urlPath, function (data) {
                var jqJplayer = $("#jquery_jplayer_1");
                jqJplayer.jPlayer("destroy");

                jqJplayer.jPlayer({
                    ready: function () {
                        $(this).jPlayer("setMedia", {
                            title: title,
                            mp3: url1
                        }).jPlayer("play");
                    },
                    ended: function () {
                        var jpPlayer = $('.jp-audio');
                        if (jpPlayer.hasClass('jp-state-shuffled') && !jpPlayer.hasClass('jp-state-looped')) {
                            var rows = $('table > tbody > tr');
                            var randomNumber = Math.floor((Math.random() * rows.length));
                            rows[randomNumber].click();
                        }
                        else if ($('.jp-state-looped').val() === undefined) {
                            var nextVar = $(next).closest('tr').next('tr');
                            nextVar.click();
                        }
                    },
                    swfPath: "../../dist/jplayer",
                    supplied: "mp3",
                    wmode: "window",
                    useStateClassSkin: true,
                    autoBlur: false,
                    smoothPlayBar: true,
                    keyEnabled: true,
                    remainingDuration: true,
                    toggleDuration: true,
                    shuffleOnLoop: true
                });

            });
        }
    });
    var app = new AppView();

});
