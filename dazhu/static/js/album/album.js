
jQuery(function() {
	var $ = jQuery, $list = $('#thelist'), $btn = $('#ctlBtn'), state = 'pending', uploader;

	uploader = WebUploader.create({
		pick : {
			id : '#picker'
		},
		formData : { // 上传时附带的参数
			aid : "123"
		},
		swf : '/static/ueditor/third-party/webuploader/Uploader.swf',
		server : '/album/upload',
		duplicate : true,
		compress : false,
		// 只允许选择图片文件。
		accept : {
			title : 'Images',
			extensions : 'gif,jpg,jpeg,bmp,png',
			mimeTypes : 'image/*'
		}
	});

	// 当有文件添加进来的时候
	uploader.on('fileQueued', function(file) {
		var $li = $('<div id="' + file.id + '" class="file-item thumbnail">'
				+ '<img>' + '<div class="info">' + file.name + '</div>'
				+ '</div>'), $img = $li.find('img');

		// $list为容器jQuery实例
		$list.append($li);

		// 创建缩略图
		// 如果为非图片文件，可以不用调用此方法。
		// thumbnailWidth x thumbnailHeight 为 100 x 100
		uploader.makeThumb(file, function(error, src) {
			if (error) {
				$img.replaceWith('<span>不能预览</span>');
				return;
			}

			$img.attr('src', src);
		}, 100, 100);
	});

	// 文件上传过程中创建进度条实时显示。
	uploader
			.on(
					'uploadProgress',
					function(file, percentage) {
						var $li = $('#' + file.id), $percent = $li
								.find('.progress .progress-bar');

						// 避免重复创建
						if (!$percent.length) {
							$percent = $(
									'<div class="progress progress-striped active">'
											+ '<div class="progress-bar" role="progressbar" style="width: 0%">'
											+ '</div>' + '</div>')
									.appendTo($li).find('.progress-bar');
						}

						$li.find('div.info').text('上传中');

						$percent.css('width', percentage * 100 + '%');
					});

	uploader.on('uploadSuccess', function(file) {
		$('#' + file.id).find('div.info').text('已上传');
	});

	uploader.on('uploadError', function(file) {
		$('#' + file.id).find('div.info').text('上传出错');
	});

	uploader.on('uploadComplete', function(file) {
		$('#' + file.id).find('.progress').fadeOut();
	});

	uploader.on('all', function(type) {
		if (type === 'startUpload') {
			state = 'uploading';
		} else if (type === 'stopUpload') {
			state = 'paused';
		} else if (type === 'uploadFinished') {
			state = 'done';
		}

		if (state === 'uploading') {
			$btn.text('暂停上传');
		} else {
			$btn.text('开始上传');
		}
	});

	$btn.on('click', function() {
		if (state === 'uploading') {
			uploader.stop();
		} else {
			uploader.upload();
		}
	});
});
