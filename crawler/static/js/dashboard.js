$(function() {
	$('#task_favcrawler').click(function (e) {
		// favorite crawling start
		$.getJSON("/api/favcrawler/", {
			del: 1,
		})
		.done(function (data) {
			alert(data);
		})
		.fail(function () {
			alert("failed to call ajax api!");
		});
	});

	$('#task_piccrawler').click(function (e) {
		// pic crawling start
		$.getJSON("/api/piccrawler/", {
		})
		.done(function (data) {
			alert(data);
		})
		.fail(function () {
			alert("failed to call ajax api!");
		});
	});

	$('#task_regexfind').click(function (e) {
		alert("preparing service!");
	});

	$('#task_static').click(function (e) {
		alert("preparing service!");
	});

	$('#task_test').click(function (e) {
		$.getJSON("/api/testtwit/", {
		})
		.done(function (data) {
			alert(data);
		})
		.fail(function () {
			alert("failed to call ajax api!");
		});
	});

	$('#task_stop').click(function (e) {
		$.getJSON("/api/taskstop/", {
		})
		.done(function (data) {
			alert(data);
		})
		.fail(function () {
			alert("failed to call ajax api!");
		});
	});

	setInterval(2000, function () {
		// crawl current status from server
		$.getJSON("/api/getstatus/" + userid + "/", {
		})
		.done(function (data) {
			if (data.success == 1) {
				var valuer = data.value;
				var msg = data.message;
				$("#progress_bar").css('width', valeur+'%').attr('aria-valuenow', valeur);
				$("#progress_status").html(msg);
			} else {
				console.log("not successed to getstatus");
			}
		})
		.fail(function () {
			console.log("failed to retrieve status of user " + userid);
		});
	});
});
