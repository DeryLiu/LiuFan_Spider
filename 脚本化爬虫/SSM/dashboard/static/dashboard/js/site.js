/**
 * Created by alex on 16-11-4.
 */
var deleteSite = function (url, site_names) {
    $.post(
        url,
        {
            site_names: site_names,
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
        },
        function (result, status) {
            if (status == 'success' && result['state'] == 'success') {
                location.href = $("a.active").attr('href');
            } else {
                console.log(result);
            }
        }
    );
}

$(function () {
    /**
     * 图片上传
     */
    $(".file-loading").fileinput({
        language: 'zh',
        allowedFileExtensions: ['jpg', 'jpeg', 'gif', 'png'],
        showUpload: true,
        dropZoneEnabled: true,
        minImageWidth: 200,
        minImageHeight: 200,
        maxImageWidth: 1000,
        maxImageHeight: 1000,
        maxFileSize: 1024,
        minFileCount: 0,
        maxFileCount: 1,
        enctype: 'multipart/form-data'
    });

    /**
     * 添加站点
     */
    $("#btnAddSite").on('click', function () {
        var $name = $('input#siteAddName');
        if ($name.val() == '' || $name.val() == null || typeof($name.val()) == 'undefined') {
            $name.popover('show');
            return;
        }
        var $url = $('input#siteAddUrl');
        if ($url.val() == '' || $url.val() == null || typeof($url.val()) == 'undefined') {
            $url.popover('show');
            return;
        }
        var $spider = $('input#siteAddSpiderClass');
        if ($spider.val() == '') {
            $spider.prop('show');
            return;
        }
        $("#siteAddForm").submit();
    });

    /**
     * 修改站点
     */
    $("#btnUpdateSite").on('click', function () {
        var $name = $('input#siteUpdateName');
        if ($name.val() == '' || $name.val() == null || typeof($name.val()) == 'undefined') {
            $name.popover('show');
            return;
        }
        var $url = $('input#siteUpdateUrl');
        if ($url.val() == '' || $url.val() == null || typeof($url.val()) == 'undefined') {
            $url.popover('show');
            return;
        }
        var $spider = $('input#siteUpdateSpiderClass');
        if ($spider.val() == '') {
            $spider.prop('show');
            return;
        }
        $("#siteUpdateForm").submit();
    });

    /**
     * 点击修改站点
     */
    var $btnUpdateSite = $('.btn-update-site');
    $btnUpdateSite.on('click', function () {
        $('input#siteUpdateId').val($(this).data('site-id'));
        $('input#siteUpdateName').val($(this).data('site-name'));
        $('input#siteUpdateUrl').val($(this).data('site-url'));
        $('input#siteUpdateSpiderClass').val($(this).data('site-spider-class'));
    });

    /**
     * 删除站点
     */
    var site_names = [];
    var site_remove_url = $('input.btn-bulk-remove-site').data('href-site-remove');
    $(".btn-remove-site").on('click', function () {
        site_names = [];
        site_names.push($(this).data('site-name'));
        $.alertable.confirm('确定要删除 ' + site_names + '?').then(function (data) {
            deleteSite(site_remove_url, site_names);
        });
    });

    /**
     * 点击批量删除
     */
    var $bulkRemoveSite = $('.btn-bulk-remove-site');
    $bulkRemoveSite.on('click', function () {
        if (site_names.length > 0) {
            $.alertable.confirm('确定要删除 ' + site_names + '?').then(function (data) {
                deleteSite(site_remove_url, site_names);
            });
        }
    });

    /**
     * 全选站点
     */
    var $chkAll = $('input.chk-all');
    var $chkItem = $('input.chk-item');
    $chkAll.on('click', function () {
        site_names = [];
        if ($chkAll.prop('checked')) {
            $chkItem.prop('checked', true);
            $.each($chkItem, function () {
                site_names.push($(this).data('site-name'));
            });
            $bulkRemoveSite.prop('disabled', false);
        } else {
            $chkItem.prop('checked', false);
            $bulkRemoveSite.prop('disabled', true);
        }
    });

    /**
     * 单选站点
     */
    $chkItem.on('click', function () {
        site_names = [];
        var chkCount = 0;
        $.each($chkItem, function () {
            if ($(this).prop('checked')) {
                site_names.push($(this).data('site-name'));
                chkCount++;
            }
        });
        $bulkRemoveSite.prop('disabled', false);
        if (chkCount == $chkItem.length) {
            $chkAll.prop('checked', true);
        } else {
            $chkAll.prop('checked', false);
            if (chkCount == 0) {
                $bulkRemoveSite.prop('disabled', true);
            }
        }
    });

    /**
     * 初始化站点
     */
    $('.btn-init-site').on('click', function () {
        if (!$(this).hasClass('disabled')) {
            $(this).text('初始化中');
            $(this).addClass('disabled');
            var url = $(this).data('init-href');
            $.get(
                url,
                function (result) {
                    if (result.state == 'success') {
                        $.alertable.alert('站点初始化中，请稍等！')
                    } else {
                        $.alertable.alert(result.msg)
                    }
                }
            );
        }
    });
});