// Ajax Setup
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function run_the_timer(timer, button) {
    clearInterval(timer);  //This sentence is very important

    let time = Number(sessionStorage.getItem("timer"));
    timer = setInterval(function () {
        if (time <= 0) {
            button.innerText = `ارسال مجدد کد`;
            button.disabled = false;
        } else {
            button.disabled = true;
            button.innerText = `${time} ثانیه تا درخواست مجدد کد`;
            time--;
            sessionStorage.setItem("timer", time);
        }
    }, 1000);
    return timer;
}

window.onload = function () {
    let button = document.getElementById('resend-code');

    if (sessionStorage.getItem("timer") == null || isNaN(sessionStorage.getItem("timer"))) {
        sessionStorage.setItem("timer", 120);
    }
    let timer = sessionStorage.getItem("timer");
    timer = run_the_timer(timer, button)

    button.onclick = function () {
        sessionStorage.setItem("timer", 120);
        timer = run_the_timer(timer, button);

        $.ajax({
            url: $('#resend-code').attr('data-url'),
            method: 'post',
            success: function (result) {
                if (result['status'] === 200) {
                    $("#message-place").load(location.href + " #message-place");
                }
            }
        });
    }
}