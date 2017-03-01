/**
 * Created by alex on 16-11-14.
 */
var progress_json_url = $('input#progressJsonUrl').val();
var load_progress = function () {
    $.get(progress_json_url, function (result) {
        if (result.state == 'success') {
            var $tbody = $('tbody');
            $tbody.find('tr').remove();
            for (var i in result.datas) {
                var data = result.datas[i];
                var $tr = $('<tr></tr>');
                $tr.append($('<td>' + data['category_path'] + '</td>'));
                $tr.append($('<td><div class="progress"><div class="progress-bar progress-bar-info progress-bar-striped active" role="progressbar" style="width: ' + data.page_progress + '%; min-width: 20px;">' + data.page_progress + '%</div></div></td>'));
                $tr.append($('<td>' + data['success'] + '</td>'));
                $tr.append($('<td>' + data['failed'] + '</td>'));
                $tr.append($('<td>' + data['total'] + '</td>'));
                $tr.appendTo($tbody);
            }
        } else {
            $.alertable.alert('加载进度失败');
        }
    });
};

$(function () {
    load_progress();
    setInterval(load_progress, 5000);
});