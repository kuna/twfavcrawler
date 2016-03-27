$(function() {
	$('#task_favcrawler').click(function (e) {
		// favorite crawling start
		$.getJSON("/api/favcrawler/" + userid + "/", {
			del: 1,
		})
		.done(function (data) {
			alert(data.message);
		})
		.fail(function () {
			alert("failed to call ajax api!");
		});
	});

	$('#task_piccrawler').click(function (e) {
		// pic crawling start
		$.getJSON("/api/piccrawler/" + userid + "/", {
		})
		.done(function (data) {
			alert(data.message);
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
			alert(data.message);
		})
		.fail(function () {
			alert("failed to call ajax api!");
		});
	});

	$('#task_stop').click(function (e) {
		$.getJSON("/api/taskstop/" + userid + "/", {
		})
		.done(function (data) {
			alert(data.message);
		})
		.fail(function () {
			alert("failed to call ajax api!");
		});
	});

	setInterval(function () {
		// crawl current status from server
		$.getJSON("/api/status/" + userid + "/", {
		})
		.done(function (data) {
			if (data.success == 1) {
				var valeur = data.value;
				var msg = data.message;
				if (valeur != undefined) {
					$("#progress_bar").css('width', valeur+'%').attr('aria-valuenow', valeur);
				}
				$("#progress_status").html(msg);
			} else {
				console.log("not successed to getstatus");
			}
		})
		.fail(function () {
			console.log("failed to retrieve status of user " + userid);
		});
	}, 2000);
});
