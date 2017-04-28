function fill_recently_bought(data, textStatus, jgXHR)
{
   $('#recently_bought').html(data);
}

function fill_active(data, textStatus, jgXHR)
{
   $('#only_active').html(data);
}

function makeinactive()
{
    $(this).css('background-color', 'yellow').delay(500).hide(500);

    // changes item from active to inactive (item.active=True into False)
    $.ajax({
                type: "POST",
                url: this.id + '/switch/',
                data: {
                    'pk':  this.id,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: fill_recently_bought,
                dataType: 'html'
            });

    // updates the list of active items

    setTimeout(function(){ 
        $.ajax({
                type: "POST",
                url: '/only_active/',
                data: {
                    'pk':  this.id,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: fill_active,
                dataType: 'html'
            });
    }, 1000);
}


function makeactive()
{
    $(this).css('background-color', 'yellow').delay(500).hide(500);

    // changes item from inactive to active (item.active=False into True)
    $.ajax({
                type: "POST",
                url: this.id + '/switch2/',
                data: {
                    'pk':  this.id,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: fill_active,
                dataType: 'html'
            });

    // updates the list of active items

    setTimeout(function(){ 
        $.ajax({
                type: "POST",
                url: '/only_inactive/',
                data: {
                    'pk':  this.id,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: fill_recently_bought,
                dataType: 'html'
            });
    }, 1000);
}


function show_menu() {
    $('#main_menu').toggleClass('hidden');
}

// function change_active_list() {
//     alert('dziala')
// }

// function formsubmit() {
//     alert('submituje2');
// }

$(document).on('click', '.active',  makeinactive);
$(document).on('click', '.inactive',  makeactive);
// $(document).on('click', '#select_list',  show_lists);
$(document).on('click', '#main_menu_toggle',  show_menu);

$('.message button').click(function() {$('.message').hide()});
// $(document).on('click', '.list_items',  change_active_list);

// $(document).on('submit', '#new_user_form',  formsubmit);