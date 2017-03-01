/**
 * Created by alex on 16-11-10.
 */
var csrfToken = $("input[name='csrfmiddlewaretoken']").val();
var taskRemoveUrl = $('input.btn-bulk-remove-task').data('task-remove-url');
var $treeObj = null;
var nodeString = '';
var taskNames = [];
var setting = {
    check: {
        enable: true,
        chkboxType: {
            "Y": "ps",
            "N": "ps"
        }
    },
    data: {
        simpleData: {
            enable: true
        }
    },
    callback: {
        onCheck: function(event, treeId, treeNode) {
            var $checkedNodes = $treeObj.getCheckedNodes();
            nodeString = '';
            var categoryNames = '';
            for (var i in $checkedNodes) {
                var $node = $checkedNodes[i];
                if (!$node.isParent) {
                    categoryNames += $node.name + ',';
                    nodeString += $node.id.toString() + ',';
                }
            }
            if (categoryNames.endsWith(',')) {
                categoryNames = categoryNames.substring(0, categoryNames.length-1);
            }
            if (nodeString.endsWith(',')) {
                nodeString = nodeString.substring(0, nodeString.length-1);
            }
            $('#taskCategory').val(nodeString);
            $('#taskShowCategory').val(categoryNames);
        }
    }
};

/**
 * 验证表单
 * @returns {boolean}
 */
var validForm = function () {
    var $name = $('#taskName');
    var popoverArray = [];
    if ($name.val() == '') {
        popoverArray.push($name);
    }
    var $site = $('#taskSite');
    if ($site.val() == '') {
        popoverArray.push($site);
    }
    var $rate = $('#taskRate');
    if ($rate.val() == '') {
        popoverArray.push($rate);
    }
    var $start_time = $('#taskStartTime');
    if ($start_time.val() == '') {
        popoverArray.push($start_time);
    }
    var $category = $('#taskShowCategory');
    if ($category.val() == '') {
        popoverArray.push($category);
    }
    var $task_type = $('#taskTaskType');
    if ($task_type.val() == '') {
        popoverArray.push($task_type);
    }
    if (popoverArray.length > 0) {
        for (var i in popoverArray) {
            popoverArray[i].popover('show');
        }
        return false;
    }
    return true;
};

/**
 * 删除任务
 * @param url
 * @param tasks
 * @param csrfToken
 */
var deleteTasks = function (url, tasks, csrfToken) {
    $.post(
            url,
            {
                task_names: tasks,
                csrfmiddlewaretoken: csrfToken
            },
            function (result, status) {
                if (status == 'success' && result['state'] == 'success') {
                    location.href = result['redirect'];
                } else {
                    console.log(result);
                }
            }
    );
};

var updateForm = function (values) {
    console.log(values);
    $('#taskModal').find('h4.modal-title').text(values.taskFormName);
    $('#taskId').val(values.taskId);
    $('#taskName').val(values.taskName);
    $('#taskSite').val(values.taskSite);
    $('#taskRate').val(values.taskRate);
    $('#taskStartTime').val(values.taskStartTime);
    $('#taskTaskType').val(values.taskType);
    $('#taskCategory').val(values.categoryKeys);
    $('#taskShowCategory').val(values.categoryNames);
};

$(function () {
    $('.btn-add-task').on('click', function () {
        var values = {taskFormName: '添加站点', taskId: '', taskName: '', taskSite: '', taskRate: '', taskStartTime: '', taskType: '', categoryKeys: '', categoryNames: ''};
        updateForm(values);
    });

    $('.btn-update-task').on('click', function () {
        var $btn = $(this);
        var values = {
            taskFormName: '修改站点',
            taskId: $btn.data('task-id'),
            taskName: $btn.data('task-name'),
            taskSite: $btn.data('task-site'),
            taskRate: $btn.data('task-rate'),
            taskStartTime: $btn.data('task-start_time'),
            taskType: $btn.data('task-task_type'),
            categoryKeys: $btn.data('task-category-keys'),
            categoryNames: $btn.data('task-category-names')
        };
        updateForm(values);
    });

    $('#taskSite').on('change', function () {
        var json_url = $(this).find('option:selected').data('category-json-url');
        $.get(
            json_url,
            function (result) {
                if (result['state'] == 'success' && result['datas'].length > 0) {
                    $treeObj = $.fn.zTree.init($("#categoryTree"), setting, result['datas']);
                } else if($treeObj != null){
                    $treeObj.destroy();
                    $treeObj = null;
                }
            }
        );
    })
    $('#taskStartTime').datetimepicker({
        format: 'yyyy-mm-dd hh:ii',
        todayBtn: "linked",
        language: 'zh-CN'
    });

    $('#taskShowCategory').on('click', function () {
        if ($treeObj != null) {
            $('#categoryTree').slideToggle();
        }
    });

    $('#btnSubmitTask').on('click', function () {
        if (validForm()) {
            $('#taskForm').submit();
        }
    });

    /**
     * 点击删除任务
     */
    $('.btn-delete').on('click', function () {
        taskNames = [$(this).data('task-name')];
        $.alertable.confirm('确定要删除 ' + $(this).data('task-name') + '?').then(function (data) {
            deleteTasks(taskRemoveUrl, taskNames, csrfToken);
        });
    });

    /**
     * 点击批量删除
     */
    var $bulkRemoveTask = $('.btn-bulk-remove-task');
    $bulkRemoveTask.on('click', function () {
        console.log(taskNames);
        console.log(taskRemoveUrl);
        $.alertable.alert(taskNames);
        if (taskNames.length > 0) {
            $.alertable.confirm('确定要删除 ' + taskNames  + '吗?').then(function (data) {
                deleteTasks(taskRemoveUrl, taskNames, csrfToken);
            });
        }
    });

    /**
     * 全选站点
     */
    var $chkAll = $('input.chk-all');
    var $chkItem = $('input.chk-item');
    $chkAll.on('click', function () {
        taskNames = [];
        if ($chkAll.prop('checked')) {
            $chkItem.prop('checked', true);
            $.each($chkItem, function () {
                taskNames.push($(this).data('task-name'));
            });
            $bulkRemoveTask.prop('disabled', false);
        } else {
            $chkItem.prop('checked', false);
            $bulkRemoveTask.prop('disabled', true);
        }
        console.log(taskNames);
    });

    /**
     * 单选站点
     */
    $chkItem.on('click', function () {
        taskNames = [];
        var chkCount = 0;
        $.each($chkItem, function () {
            if ($(this).prop('checked')) {
                taskNames.push($(this).data('site-name'));
                chkCount++;
            }
        });
        $bulkRemoveTask.prop('disabled', false);
        if (chkCount == $chkItem.length) {
            $chkAll.prop('checked', true);
        } else {
            $chkAll.prop('checked', false);
            if (chkCount == 0) {
                $bulkRemoveTask.prop('disabled', true);
            }
        }
    });

    /**
     * 启动任务
     */
    $('.btn-start-task').on('click', function () {
        var $btn = $(this);
        $.get(
            $btn.data('task-start-url'),
            function (result) {
                if (result['state'] == 'success') {
                    $btn.text('已启动');
                    $btn.addClass('disabled');
                    $.alertable.alert('任务已启动');
                } else {
                    $.alertable.alert(result['msg']);
                }
            }
        );
    });
});