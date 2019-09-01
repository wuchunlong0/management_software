// 插件
(function($) {
    /* -----------------------------------------/
     * 功能：弹出层
     * 参数：
     * 返回：
     * 作者：ZHANGHAIBIN
    / ---------------------------------------- */
    $.fn.popupshow = function(options) {
        var settings = $.extend({
            'popupId': null, // 弹出层id
            'htmlUrl': null, // 要插入的HTML的URL
            'maskId': 'mask', // 遮罩id,null不显示遮罩
            'position': 'fixed', // 定位类别(参数fixed和absolute)
            'zindex': null, // z-index值
            'countdown': null,   // 倒计时关闭(正整数,以秒为单位)
            'timeNode': null,   // 倒计时输出位置
            'jumpUrl': null,    // 关闭时跳转URL
            'callback': null, // 弹出回调
            'closeCallback': null // 关闭回调
        }, options);

        var $popup = $("#" + settings.popupId);
        var $countdown = $('<div class="countdownTxt">');

        //弹出层显示
        if ($popup.length > 0) {
            // 给隐藏在页面中的弹层做标记
            $popup.show().attr("popmark", "popmark");
            // 设置zIndex值
            if (settings.zindex !== null) {
                $popup.css({zIndex: settings.zindex});
            }
            // 弹层定位
            _popupPsotion(settings.popupId, settings.position);
            //关闭弹层
            $("#" + settings.popupId + " .close").bind('click', _close);
            // 弹出回调
            if (settings.callback !== null) {
                settings.callback();
            }
            // 倒计时关闭
            if (settings.countdown !== null) {
                // 参数类型判断
                if (typeof settings.countdown == 'number' && settings.countdown > 0) {
                    _countdown(settings.countdown, settings.timeNode, settings.jumpUrl);
                } else {
                    throw new TypeError();
                }
            }
        } else if (settings.htmlUrl !== null) {
            $.ajax({
                	type: "GET",
                	url: settings.htmlUrl,
                	success: function(res) {
                    $('body').append(res);
                    var $popup = $("#" + settings.popupId);
                    // 设置zIndex值
                    if (settings.zindex !== null) {
                        $popup.css({zIndex: settings.zindex});
                    }
                    _popupPsotion(settings.popupId, settings.position);
                    //关闭弹层
                    $("#" + settings.popupId + " .close").bind('click', _close);
                    // 弹出回调
                    if (settings.callback !== null) {
                        settings.callback();
                    }
                    // 倒计时关闭
                    if (settings.countdown !== null) {
                        // 参数类型判断
                        if (typeof settings.countdown == 'number' && settings.countdown > 0) {
                            _countdown(settings.countdown, settings.timeNode, settings.jumpUrl);
                        } else {
                            throw new TypeError();
                        }
                    }
                	}
            });
        } else {
            return false;
        }

        //判断是否启用遮罩
        if (settings.maskId !== null) {
            var $mask = $("#" + settings.maskId);
            if ($mask.length > 0) {
                $mask.show();
            } else {
                var maskNode = $("<div class='mask' id='" + settings.maskId + "'>");
                $('body').append(maskNode);
            }
        }

        // 倒计时关闭
        function _countdown(time, node, url) {
            // 参数说明:
            // 1. time是设定的倒计时时间;
            // 2. node是自定义显示倒计时的位置;
            // 3. url是倒计时结束时跳转的url

            var _time = Math.ceil(time);
            var _popup = $("#" + settings.popupId);
            // 如果自定义了时间显示节点名, 则在指定位置显示倒计时
            if (node !== null) {
                _popup.find(node).html(_time + "秒");
            } else {
                _popup.children('.wrap').append($countdown).find($countdown).html(_time + "秒");
            }

            window.clearTimeout(this._t);
            this._t = window.setTimeout(function() {
                _time--;
                if (_time > 0) {
                    // 如果自定义了时间显示节点名, 则在指定位置显示倒计时
                    if (node !== null) {
                        _popup.find(node).html(_time + "秒");
                    } else {
                        _popup.children('.wrap').append($countdown).find($countdown).html(_time + "秒");
                    }
                   return _countdown(time - 1, node, url);
                } else {
                    $("#" + settings.popupId + " .close").click();
                    if (url !== null) {
                        document.location = url;
                        window.clearTimeout(this._t);
                    }
                }
            }, 1000);
        }

        //关闭弹层
        function _close() {
            // 关闭回调
            if (settings.closeCallback !== null) {
                settings.closeCallback();
            }
            if (settings.jumpUrl !== null) {
                document.location = settings.jumpUrl;
            }
            var _popup = $(this).parents("#" + settings.popupId);
            var _mark = _popup.attr("popmark");
            // 如果存在popmark属性则隐藏，否则删除
            if (_mark == "popmark") {
                _popup.hide();
            } else {
                _popup.remove();
            }
            $("#" + settings.maskId).hide();
        }

        //弹层定位
        function _popupPsotion(popupId, position) {
            var $popup = $("#" + popupId),
                $win = $(window),
                winW = $win.width(),
                winH = $win.height(),
                popupW = $popup.width(),
                popupH = $popup.height(),
                scrollT = $win.scrollTop(),
                scrollL = $win.scrollLeft();

            if (position == "fixed") {
                var popupTop = (winH - popupH) / 2,
                    popupLeft = (winW - popupW) / 2;

                $popup.css({
                    position: "fixed",
                    top: popupTop,
                    left: popupLeft,
                    margin: 0
                });
            } else if (position == "absolute") {
                var popupTop = (winH - popupH) / 2 + scrollT,
                    popupLeft = (winW - popupW) / 2 + scrollL;

                $popup.css({
                    position: "absolute",
                    top: popupTop,
                    left: popupLeft,
                    margin: 0
                });
            }
        }
        $(window).resize(function() {
            _popupPsotion(settings.popupId, settings.position);
        });
    };
})(jQuery);

/* -----------------------------------------/
 * 功能：为空验证
 * 参数：
 * 返回：
 * 作者：ZHANGHAIBIN
/ ---------------------------------------- */
function emptyCheck(obj, e, args) {
    var settings = $.extend({
        'note': '该项为必填项', // 提示文本
        'minlength': null, // 最小长度验证(参数：正整数)
        'maxlength': null, // 最大值长度验证(参数：正整数)
        'valelem': null,    // 取值元素(默认this)
        'target': null, // 文本插入目标位置
        'tagname': 'span', // html标签名称
        'successhint': true,   // 是否显示成功提示
        'callback': null // 回调函数
    },args);

    var $this = $(obj);
    // 检查是否自定义取值元素
    if (settings.valelem !== null) {
        var val = $.trim(settings.valelem.val());
    } else {
        var val = $.trim($this.val());
    }
    var _note = '<'+ settings.tagname + ' class="note errTxt">' + settings.note + '</' + settings.tagname + '>';
    var _successNote = '<'+ settings.tagname + ' class="note successTxt"><i class="icon icon-success"></i></' + settings.tagname + '>';

    if (!val || val === 'null') {
        e.preventDefault();
        // 删除错误提示
        delNote();
        // 判断提示文本是否设置
        if (settings.note === null) {
            // 插入提示
            insetNote('<'+ settings.tagname + ' class="note errTxt">该项为必填项</' + settings.tagname + '>');
        } else {
            // 插入提示
            insetNote(_note);
        }
        // 获取焦点时删除提示
        $this.bind("focus", function() {
            delNote();
        });
        return false;
    } else {
        if (settings.minlength !== null && settings.maxlength !== null) {
            if (typeof settings.minlength != 'number' && typeof settings.minlength != 'number') return new TypeError();
            var _val = $.trim($this.val());
            if (_val.length < settings.minlength) {
                var _note = '<'+ settings.tagname + ' class="note errTxt"><i class="icon icon-warn"></i>字段长度最少' + settings.minlength + '个字符</' + settings.tagname + '>';
                e.preventDefault();
                // 插入提示
                insetNote(_note);
                return false;
            } else if (_val.length > settings.maxlength) {
                var _note = '<'+ settings.tagname + ' class="note errTxt"><i class="icon icon-warn"></i>字段长度超过' + settings.maxlength + '个字符</' + settings.tagname + '>';
                e.preventDefault();
                // 插入提示
                insetNote(_note);
                return false;
            } else {
                return successFn(_successNote);
            }

        } else if (settings.minlength !== null) {
            if (typeof settings.minlength != 'number') return new TypeError();
            var _val = $.trim($this.val());
            var _note = '<'+ settings.tagname + ' class="note errTxt"><i class="icon icon-warn"></i>字段长度最少' + settings.minlength + '个字符</' + settings.tagname + '>';
            if (_val.length < settings.minlength) {
                e.preventDefault();
                // 插入提示
                insetNote(_note);
                return false;
            } else if (settings.maxlength !== null) {
                if (typeof settings.maxlength != 'number') return new TypeError();
                var _val = $.trim($this.val());
                var _note = '<'+ settings.tagname + ' class="note errTxt"><i class="icon icon-warn"></i>字段长度超过' + settings.maxlength + '个字符</' + settings.tagname + '>';
                if (_val.length > settings.maxlength) {
                    e.preventDefault();
                    // 插入提示
                    insetNote(_note);
                    return false;
                } else {
                    return successFn(_successNote);
                }
            } else {
                return successFn(_successNote);
            }
        } else if (settings.maxlength !== null) {
            if (typeof settings.maxlength != 'number') return new TypeError();
            var _val = $.trim($this.val());
            var _note = '<'+ settings.tagname + ' class="note errTxt"><i class="icon icon-warn"></i>字段长度超过' + settings.maxlength + '个字符</' + settings.tagname + '>';
            if (_val.length > settings.maxlength) {
                e.preventDefault();
                // 插入提示
                insetNote(_note);
                return false;
            } else if (settings.minlength !== null) {
                if (typeof settings.minlength != 'number') return new TypeError();
                var _val = $.trim($this.val());
                var _note = '<'+ settings.tagname + ' class="note errTxt"><i class="icon icon-warn"></i>字段长度最少' + settings.minlength + '个字符</' + settings.tagname + '>';
                if (_val.length < settings.minlength) {
                    e.preventDefault();
                    // 插入提示
                    insetNote(_note);
                    return false;
                } else {
                    return successFn(_successNote);
                }
            } else {
                return successFn(_successNote);
            }
        } else {
            return successFn(_successNote);
        }
    }
    // 插入提示
    function insetNote(note) {
        // 删除提示
        delNote();
         // 判断文本插入目标是否设置
        if (settings.target === null) {
            $this.parent().append(note);
        } else {
            settings.target.append(note);
        }
    }
    // 删除提示
    function delNote() {
        if (settings.target !== null) {
            settings.target.find('.note.errTxt').remove();
            settings.target.find('.note.successTxt').remove();
        } else {
            var _errNote = $this.siblings('.note.errTxt');
            var _successNote = $this.siblings('.note.successTxt');
            _errNote.remove();
            _successNote.remove();
        }
    }
    // 验证正确
    function successFn(note) {
        if (settings.successhint === true){
            // 删除提示
            delNote();
            // 插入成功提示
            if (settings.target === null) {
                $this.parent().find('.note.successTxt').remove();
                $this.parent().append(note);
            } else {
                settings.target.find('.note.successTxt').remove();
                settings.target.append(note);
            }
        }
        // 执行回调函数
        if (settings.callback !== null) {
            return settings.callback(val, e);
        } else {
            return [true, val];
        }
    }
}

// 项目公用方法
var DOWNLOAD = {
    init: function() {
        this.bindEle();
        this.sideNav();
        this.TopSearch();
    },
    bindEle: function() {
        $('#headsearch .search-btn').bind('click', DOWNLOAD.TopSearch);
        $('.resource .img-view').bind('mouseover', DOWNLOAD.viewPosition);
    },
    sideNav: function() {
        var $sideNav = $('#sidenav'),
            $navs = $sideNav.find('.navs'),
            $navLi = $navs.find('li'),
            $subnav = $sideNav.find('.subnav'),
            $item = $subnav.find('.subnav-item');

        $navLi.each(function(i) {
            var _this = $(this);
            _this.mouseleave(function() {
                // 延迟关闭菜单
                DOWNLOAD.t = setTimeout(function() {
                    _this.removeClass('active');
                    $subnav.removeClass('open');
                    $item.removeClass('active');
                }, 400);
            }).mouseenter(function() {
                // 清除延迟，阻止代码执行
                clearTimeout(DOWNLOAD.k);
                clearTimeout(DOWNLOAD.t);
                _this.addClass('active').siblings('li').removeClass('active');
                $subnav.addClass('open');
                $item.removeClass('active').eq(i).addClass('active');
            });
        });
        // 子导航hover事件
        $subnav.mouseenter(function(){
            // 清除延迟，阻止代码执行
            clearTimeout(DOWNLOAD.k);
            clearTimeout(DOWNLOAD.t);
        }).mouseleave(function() {
            DOWNLOAD.k = setTimeout(function() {
                $subnav.removeClass('open');
                $item.removeClass('active');
                $navLi.removeClass('active');
            }, 400);
        });
    },
    TopSearch: function() {
        //头部搜索
        $("input[name='q']").bind("focus", function() {
            $('.search-btn').addClass("active");
            $('.hot-words').hide()
            $(this).css({paddingRight: "55px"});
        });
        $("input[name='q']").bind("focusout", function() {
            $('.search-btn').removeClass("active");
            $('.hot-words').show();
        });
        // 搜索结果
        $('#J_keywordList .result-list').delegate('.current', "click", function() {
            var val = $(this).text();
            $("input[name='q']").val(val);
        });
    },
    viewPosition: function() {
        var _this = $(this),
            $img = _this.find('.img-wrap img'),
            win = $(window),
            winHeight = win.height(),
            scrollT = win.scrollTop(),
            boxT = _this.offset().top,
            viewBottom = boxT + 300 - scrollT,   // 300是放大图的高度
            imgWidth = $img.width(),
            imgHeight = $img.height();

        var _url = $img.attr("src");
        var _html = $('<div class="img-preview"><span><img src="' + _url + '"/></span></div>');
        _this.append(_html);

        if (imgWidth - imgHeight >= 0) {
            _html.find('img').css({width: "100%"});
        } else {
            _html.find('img').css({height: "100%"});
        }

        if (winHeight < viewBottom) {
            $('.img-preview').css({top: "auto", bottom: 0});
        }

        _this.bind('mouseout', function() {
            _this.find('.img-preview').css({top: 0, bottom: "auto"}).remove();
        });
    },
    loginHint: function() {
        var $this = $(this);
        $this.popupshow({
            popupId: 'loginHint',
            htmlUrl: web_url + 'src/popup/login-hint.html',
        });
        return false;
    }
};

$(function() {
    DOWNLOAD.init();
})
