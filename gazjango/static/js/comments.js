/*
    TODO: when a comment is posted, highlight it
    TODO: make speaking_officially box disable when it's anonymous
*/

function fullSetup() {
    setupShowLinks();
    setupSubmission();
    // setupVoteLinks();
    setupApproveLinks();
}
$(fullSetup);


// ======================
// = hiding and showing =
// ======================

var speed = 'normal';

function hideFunctionFor(id) {
    return function() {
        $('#c-' + id)
            .removeClass('shown-comment').addClass('hidden-comment')
            .find('.commentText')
                .slideUp(speed)
                .end()
            .find('.showLink')
                .html('show anyway')
                .unbind('click')
                .click(showFunctionFor(id));
        return false;
    };
}
function showFunctionFor(id) {
    return function() {
        $('#c-' + id)
            .removeClass('hidden-comment').addClass('shown-comment')
            .find('.commentText')
                .slideDown(speed)
                .end()
            .find('.showLink')
                .html('hide')
                .unbind('click')
                .click(hideFunctionFor(id));
        return false;
  };
}

function loadFunctionFor(id) {
    return function() {
        $('#c-' + id)
            .find('.commentText')
                .hide()
                .load('show-comment/' + id + '/', function() {
                    $(this).slideDown(speed);
                })
                .removeClass('hidden-comment').addClass('shown-comment')
                .end()
            .find('.showLink')
                .html('hide')
                .unbind('click')
                .click(hideFunctionFor(id));
        return false;
    }
}

function setupShowLinks() {
    $('.hidden-comment').each(function() {
        var id = this.id.substring('2');
        $(this).find('.showLink').unbind('click').click(loadFunctionFor(id));
    });
}



// ====================
// = posting comments =
// ====================

var default_comment_name;
$(function() {
    default_comment_name = $('input[name="name"]').val();
});

function syncNameDisabled() {
    setNameDisabled($('input[name="anonymous"]:checked').length == 0);
}

function setNameDisabled(disabled) {
    var namebox = $('input[name="name"]').attr('disabled', disabled);
    if (disabled) {
        namebox.val(default_comment_name);
    }
}

function newComments() { newComments('normal'); }

function newComments(speed) {
    comments = $('.comment');
    if (comments.length == 0) {
        last_num = 0;
    } else {
        last_num = comments.get(comments.length - 1).id.substr(2);
    }
    $.get('comments/' + last_num + '/', {}, function(data, textStatus) {
        $('#comments').append(data);
        fullSetup();
        
        var new_comments = $('.comment.new');
        var i = 0;
        callback = function() {
            i++;
            if (i < new_comments.length) {
                new_comments.eq(i).slideDown(speed, callback).removeClass('new');
            }
        }        
        new_comments.eq(0).slideDown(speed, callback);
    });
}

function setupSubmission() {
    syncNameDisabled();
    $('input[name="anonymous"]').click(syncNameDisabled);
    $('input[type=reset]').click(function() {
        setNameDisabled(true);
    });
    $('#submitComments textarea')
        .focus(function() {
            if ($(this).val() == "Have your say.") { $(this).val(''); }
        });
}

function strStartsWith(start, str) {
    return str.substr(0, start.length) == start;
}

function submitComment() {
    data = {};
    $('#commentForm :input').each(function() {
        data[$(this).attr('name')] = $(this).val();
    });
    // explicit override for checkboxes since they're not working right
    anon = $('#commentForm :input[name="anonymous"]:checked').length;
    offic = $('#commentForm :input[name="speaking_officially"]:checked').length;
    data.anonymous = anon == 1 ? "on" : "";
    data.speaking_officially = offic == 1 ? "on" : "";
    
    $.post($('#commentForm form').attr('action'), data,
       function(resp, textStatus) {
           if (resp == 'success') {
               newComments();
               $('#commentForm input[type=reset]').click();
               $()
           } else if (strStartsWith('redirect: ', resp)) {
               window.location = resp.substr('redirect: '.length);
           } else {
               // it's okay to kill the <h4>, since it's unlikely that
               // many people will have javascript on but css off :)
               $('#commentForm').html(resp);
           }
       }
    );
    return false;
}



// ==========
// = voting =
// ==========

// function setupVoteLinks() {
//     $('a.vote').each(function() {
//         $(this)
//             .unbind('click')
//             .click(function() {
//                 $.post($(this).attr('href'), {}, function() {
//                     refreshComments();
//                 });
//                 return false;
//             });
//     });
// }


// =============
// = approving =
// =============

function setupApproveLinks() {
    $('.approveLink').click(function(event) {
        var comment = $(this).parents('.comment');
        var id = comment.attr('id').substring(2);
        event.preventDefault();
        
        $.post($(this).attr('href'), {}, function(resp) {
            var loaded = $.trim(comment.find('.commentText').html()) != "";
            loaded ? showFunctionFor(id)() : loadFunctionFor(id)();
            
            comment.find('.commentAuthorship').html(resp);
        });
    });
}
