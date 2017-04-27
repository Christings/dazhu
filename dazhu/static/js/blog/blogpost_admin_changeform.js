$(document)
	.ready(
		function() {
		    $('body').on('click', '.insert_attachment', function (){
                testEditor.insertValue("!["+$(this).prev().attr("item_name")+"]("+$(this).prev().text()+")");
            });

			$("#id_guid").attr("readonly", "readonly");
			$.getJSON("/account/get_user_info", function(json) {
				username = json[1] + json[2];
				$("#id_author").val(username);
			});
			
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

			//处理markdown
			var body_parent = $("#id_body").parent();
			var body_val = $("#id_body").val();
			$("#id_body").remove();
			var body = "<div id='bodycontent'><div>";
			body_parent.append(body);

			var attachment = "<label>attachment:</label>"+
			"<div id='attachment_box' style='width:70%;float:left;'><div>";
			body_parent.append(attachment);
			$.getJSON("/blog/get_attachment?aid="+$("#id_guid").val(), function(json) {
				attachment_html = "";
				$.each(json, function(i, item) {
					attachment_html += "<div>"+
					"<span style='margin:10px' item_name='"+item.sourceName+"' >"+
					    "<a target='_blank' href='/admin/ueditor/attachment/"+item.id+"/change/'>/static/upload/" + item.rndName + "</a>"+
					"</span>"+
					"<input type='button' class='insert_attachment' style='height:20px;padding:2px;' value='insert'/>"+
					"</div>";
				});
				$("#attachment_box").html(attachment_html);
			});

			testEditor = editormd("bodycontent", {
				width   : "70%",
				value	: body_val,
				name	: "body",
				emoji	: true,
				height  : 640,
				syncScrolling : "single",
				path    : "/static/editor.md/lib/",
				imageUpload    : true,
				imageFormats   : ["jpg", "jpeg", "gif", "png", "bmp", "webp", "txt", "zip"],
				imageUploadURL : "/blog/upload?aid="+$("#id_guid").val(),
			});



			// 处理ueditor
			// var body_parent = $("#id_body").parent();
			// var body_val = $("#id_body").val();

			// $("#id_body").remove();

			// var body = "<div id='bodycontent'><script id=\"id_body\" name=\"body\" class=\"vLargeTextField\" type=\"text/plain\" >"
			// 		+ body_val + "</script><div>";
			// body_parent.append(body);

			// $("#bodycontent").css({
			// 	"margin-left" : $("#bodycontent").prev().width() + 12
			// });
			// var ue = UE.getEditor('id_body', {
			// 	// 默认的编辑区域高度
			// 	initialFrameHeight : 400,
			// 	initialFrameWidth : "100%",
			// 	zIndex : 3,
			// 	autoHeightEnabled : 'false',
			// 	scaleEnabled : 'false',
			// 	aid : $("#id_guid").val(),
			// 	UEDITOR_HOME_URL:"/static/ueditor/",
			// 	toolbars: [[
			// 		'fullscreen', 'source', '|', 'undo', 'redo', '|',
			// 		'bold', 'italic', 'underline', 'fontborder', 'strikethrough', 'superscript', 'subscript', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', 'cleardoc', '|',
			// 		'rowspacingtop', 'rowspacingbottom', 'lineheight', '|',
			// 		'customstyle', 'paragraph', 'fontfamily', 'fontsize', '|',
			// 		'directionalityltr', 'directionalityrtl', 'indent', '|',
			// 		'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|',
			// 		'link', 'unlink', 'anchor', '|', 'imagenone', 'imageleft', 'imageright', 'imagecenter', '|',
			// 		 'insertimage', 'emotion', 'scrawl', 'insertvideo', 'music', 'attachment', 'map', 'gmap', 'insertframe', 'insertcode', 'webapp', 'pagebreak', 'template', 'background', '|',
			// 		'horizontal', 'date', 'time', 'spechars', 'snapscreen', 'wordimage', '|',
			// 		'inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols', 'charts', '|',
			// 		'print', 'preview', 'searchreplace', 'help', 'drafts'
			// 	]]
			// });
		});
