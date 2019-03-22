/**
 * Created by alex on 16-11-7.
 */
var category_ids = [];
var page = 1;
var keyword = '';
var $treeObj = null;

var get_leaf_node = function (node) {
    if (node.children == undefined) {
        return [node.id];
    }
    var ids = [];
    node.children.forEach(function (child) {
        var children_ids = get_leaf_node(child);
        ids = ids.concat(children_ids);
    });
    return ids;
};


var display_category_products = function (ids, page, kw) {
    $.post(
        $('#categoryProductsUrl').val(),
        {
            ids: ids,
            page: page,
            keyword: kw,
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
        },
        function (result) {
            console.log(result);
            var $tbody = $('#productTable').find('tbody');
            $tbody.empty();
            if (result.state == 'success') {
                // 设置产品
                for (var i in result.datas) {
                    var data = result.datas[i];
                    var $tr = $('<tr></tr>');
                    $tr.append('<td>' + data.id + '</td>');
                    $tr.append('<td>' + data.name + '</td>');
                    $tr.append('<td>' + data.categoryName + '</td>');
                    $tr.append('<td>' + data.server + '</td>');
                    $tr.append('<td>' + data.status + '</td>');
                    $tr.append('<td><a class="btn btn-info btn-xs" role="button" href="">更新</a></td>');
                    $tr.appendTo($tbody);
                }

                // 设置翻页
                var current = result['page'];
                var total = result['total'];
                $('#totalPage').text(total);
                $('#currentPage').text(current);
                var $previous = $('.previous');
                if (current == 1) {
                    $previous.addClass('disabled');
                    $previous.find('a.pager-item').data('page', '');
                } else {
                    $previous.removeClass('disabled');
                    $previous.find('a.pager-item').data('page', current - 1);
                }
                var $next = $('.next');
                if (current < total) {
                    $next.removeClass('disabled');
                    $next.find('a.pager-item').data('page', current + 1);
                } else {
                    $next.addClass('disabled');
                    $next.find('a.pager-item').data('page', '');
                }

                // 显示关键字
                if (result['keyword'] != '') {
                    $('#keywordInfo').text('关键字：' + result['keyword']);
                } else {
                    $('#keywordInfo').text('');
                }
            } else {
                $.alertable.alert('该分类下没有找到产品');
            }
        }
    );
};

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
        onClick: function(event, treeId, treeNode, clickFlag) {
            category_ids = get_leaf_node(treeNode);
            page = 1;
            keyword = '';
            display_category_products(category_ids, page, keyword);
        }
    }
};

// var demoData = [
//     {id: 1, pId: 0, name: "Ebay", open: true},
//     {id: 2, pId: 1, name: "服装"},
//     {id: 3, pId: 1, name: "家居"},
//     {id: 4, pId: 2, name: "男装"},
//     {id: 5, pId: 2, name: "女装"}
// ];

$(function () {
    var filter = function (node) {
        return !('children' in node);
    };
    var $url = $("#topCategoryUrl").val();
    $.get(
        $url,
        function (result) {
            if (result['state'] == 'success') {
                $treeObj = $.fn.zTree.init($("#categoryTree"), setting, result['datas']);
                var leaf_nodes = $treeObj.getNodesByFilter(filter);
                for (var i in leaf_nodes) {
                    category_ids.push(leaf_nodes[i].id);
                }
            } else {
                $.alertable.alert('加载品类失败！');
            }
        }
    );

    $('.pager-item').on('click', function () {
        page = $(this).data('page');
        if (page != '' && page != undefined && page != null) {
            display_category_products(category_ids, page, keyword);
        }
    });

    $('#searchButton').on('click', function () {
        keyword = $('#keyword').val();
        if (keyword != '') {
            page = 1;
            display_category_products(category_ids, page, keyword);
        } else {
            $.alertable.alert('搜索条件不能为空');
        }
    });

    $('#btn_update').on('click', function () {
        var $checkedNodes = $treeObj.getCheckedNodes();
        var category_ids = [];
        for (var i in $checkedNodes) {
            var $node = $checkedNodes[i];
            if (!$node.isParent) {
                category_ids.push($node.id);
            }
        }
        console.log(category_ids);
        $.post(
            $(this).data('update-url'),
            {
                category_ids: category_ids,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            },
            function (result) {
                if (result.state == 'success') {
                    $.alertable.alert('品类更新中，请稍等！')
                } else {
                    $.alertable.alert(result.msg)
                }
            }
        );
    });
});