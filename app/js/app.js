(function($) {
	//全局配置(通常所有页面引用该配置，特殊页面使用mui.init({})来覆盖全局配置)
	$.initGlobal({
		swipeBack: true
	});
	var back = $.back;
	$.back = function() {
		var current = plus.webview.currentWebview();
		if (current.mType === 'main') { //模板主页面
			current.hide('auto');
			setTimeout(function() {
				document.getElementById("title").className = 'mui-title mui-fadeout';
				current.children()[0].hide("none");
			}, 200);
		} else if (current.mType === 'sub') {
			if ($.targets._popover) {
				$($.targets._popover).popover('hide');
			} else {
				current.parent().evalJS('mui&&mui.back();');
			}
		} else {
			back();
		}
	}
})(mui);


function get_default_campus() {
	//plus.storage.setItem("campus", "e")
	var c = plus.storage.getItem("campus")
	var campus;
	if (c == null) {
		campus = ["central_campus", "east_campus"]
	} else {
		if (c == "c:e") {
			campus = ["central_campus", "east_campus"]
		} else if (c == "c") {
			campus = ["central_campus"]
		} else {
			campus = ["east_campus"]
		}
	}
	console.log(campus);
	return campus;
}