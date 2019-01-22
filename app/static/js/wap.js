smart = {
    'light': function (state) {
        url = '/light/' + state
        $.ajax({
            url: url,
            success: function (data) {
                if (data['succ'] === 1) {
                }
            }
        })
    },
    'level': function (e, level) {
        $(e).siblings('li').removeClass('btn_sel').addClass('btn_nor')
        $(e).removeClass('btn_nor').addClass('btn_sel')
        url = '/light/level/' + level
        $.ajax({
            url: url,
            success: function (data) {
                if (data['succ'] === 1) {
                }
            }
        })
    }
}