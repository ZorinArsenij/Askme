function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getLikes(type) {
    var $this = $(this);
    $.ajax({
        url: "/like_" + type + "/" + $this.data("id"),
        method: "GET",
        dataType: "json",
        data: {
            "type": type
        }
    }).done(function(data) {
        if (data["like"]) {
            $this.removeClass("fa-heart-o");
            $this.addClass("fa-heart");
        } else {
            console.log("join 4");
            $this.removeClass("fa-heart");
            $this.addClass("fa-heart-o");
        }
    });
}

$(document).ready(function() {
    $(".comment .like-icon").each(function() {
        var $this = $(this);
        $.ajax({
            url: "/like_comment/" + $this.data("id"),
            method: "GET",
            dataType: "json",
            data: {
                "type": "Comment"
            }
        }).done(function(data) {
            if (data["like"]) {
                $this.removeClass("fa-heart-o");
                $this.addClass("fa-heart");
            } else {
                console.log("join 4");
                $this.removeClass("fa-heart");
                $this.addClass("fa-heart-o");
            }
        });
    });
});

$(document).ready(function() {
    $(".question .like-icon").each(function() {
        var $this = $(this);
        $.ajax({
            url: "/like_comment/" + $this.data("id"),
            method: "GET",
            dataType: "json",
            data: {
                "type": "Question"
            }
        }).done(function(data) {
            if (data["like"]) {
                $this.removeClass("fa-heart-o");
                $this.addClass("fa-heart");
            } else {
                console.log("join 4");
                $this.removeClass("fa-heart");
                $this.addClass("fa-heart-o");
            }
        });
    });
});

$(document).ready(function() {
    $(".question-item .like-icon").each(function() {
        var $this = $(this);
        $.ajax({
            url: "/like_comment/" + $this.data("id"),
            method: "GET",
            dataType: "json",
            data: {
                "type": "Question"
            }
        }).done(function(data) {
            if (data["like"]) {
                $this.removeClass("fa-heart-o");
                $this.addClass("fa-heart");
            } else {
                console.log("join 4");
                $this.removeClass("fa-heart");
                $this.addClass("fa-heart-o");
            }
        });
    });
});

$(document).ready(function () {
   $(".comment .like-icon").on("click", function () {
       var $this = $(this);
       $.ajax({
           url: "/like_comment/" + $this.data("comment_id"),
           method: "POST",
           dataType: "json",
           data: {
                "type": "Comment",
                "csrfmiddlewaretoken": getCookie("csrftoken")
           }
       }).done(function(data) {
            if (data["like"]) {
                $this.removeClass("fa-heart-o");
                $this.addClass("fa-heart");
            } else {
                console.log("join 4");
                $this.removeClass("fa-heart");
                $this.addClass("fa-heart-o");
            }
        });
   });
});

$(document).ready(function() {
    $(".question .like-icon").on("click", function() {
        var $this = $(this);
        $.ajax({
            url: "/like_comment/" + $this.data("id"),
            method: "POST",
            dataType: "json",
            data: {
                "type": "Question",
                "csrfmiddlewaretoken": getCookie("csrftoken")
            }
        }).done(function(data) {
            if (data["like"]) {
                $this.removeClass("fa-heart-o");
                $this.addClass("fa-heart");
            } else {
                $this.removeClass("fa-heart");
                $this.addClass("fa-heart-o");
            }
        });
    });
});

$(document).ready(function() {
    $(".question-item .like-icon").on("click", function() {
        var $this = $(this);
        $.ajax({
            url: "/like_comment/" + $this.data("id"),
            method: "POST",
            dataType: "json",
            data: {
                "type": "Question",
                 "csrfmiddlewaretoken": getCookie("csrftoken")
            }
        }).done(function(data) {
            if (data["like"]) {
                $this.removeClass("fa-heart-o");
                $this.addClass("fa-heart");
            } else {
                $this.removeClass("fa-heart");
                $this.addClass("fa-heart-o");
            }
        });
    });
});