$(document)
		.ready(
				function() {
					$("#id_guid").attr("readonly", "readonly");

					var cate_parent = $("#id_category").parent();
					var cate_val = $("#id_category").val();
					$("#id_category").remove();

					var list = "<select id=\"id_category\" name=\"category\"></select> ";

					cate_parent.append(list);

					$.getJSON("/blog/get_category", function(json) {
						$.each(json, function(i, item) {
							var tempText = "<option value=\"" + item + "\">"
									+ item + "</option>";

							$("#id_category").append(tempText);
						});
						$("#id_category").val(cate_val);
					});

					// 处理ueditor
					var body_parent = $("#id_body").parent();
					var body_val = $("#id_body").val();

					$("#id_body").remove();

					var body = "<div id='bodycontent'><script id=\"id_body\" name=\"body\" class=\"vLargeTextField\" type=\"text/plain\" >"
							+ body_val + "</script><div>";
					body_parent.append(body);

					$("#bodycontent").css({
						"margin-left" : $("#bodycontent").prev().width() + 12
					});
					var ue = UE.getEditor('id_body', {
						// 默认的编辑区域高度
						initialFrameHeight : 450,
						initialFrameWidth : 800,
						zIndex : 3,
						autoHeightEnabled : 'false',
						scaleEnabled : 'false',
						aid : $("#id_guid").val(),
						UEDITOR_HOME_URL:"/static/ueditor",
						toolbars: [[
							'fullscreen', 'source', '|', 'undo', 'redo', '|',
							'bold', 'italic', 'underline', 'fontborder', 'strikethrough', 'superscript', 'subscript', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', 'cleardoc', '|',
							'rowspacingtop', 'rowspacingbottom', 'lineheight', '|',
							'customstyle', 'paragraph', 'fontfamily', 'fontsize', '|',
							'directionalityltr', 'directionalityrtl', 'indent', '|',
							'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|',
							'link', 'unlink', 'anchor', '|', 'imagenone', 'imageleft', 'imageright', 'imagecenter', '|',
							 'insertimage', 'emotion', 'scrawl', 'insertvideo', 'music', 'attachment', 'map', 'gmap', 'insertframe', 'insertcode', 'webapp', 'pagebreak', 'template', 'background', '|',
							'horizontal', 'date', 'time', 'spechars', 'snapscreen', 'wordimage', '|',
							'inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols', 'charts', '|',
							'print', 'preview', 'searchreplace', 'help', 'drafts'
						]]
					});
				});
