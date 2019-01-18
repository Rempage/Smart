smart = {
    'light': function (state) {
        url = '/light/' + state
        $.ajax({
            url: url,
            success: function (data) {
                if (data['succ'] === 1) {
                    alert(data['state'])
                }
            }
        })
    }
}