$(function() {
	$('#twit_favcrawler').click(function (e) {
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

	$('#twit_piccrawler').click(function (e) {
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

	$('#twit_regexfind').click(function (e) {
		alert("preparing service!");
	});

	$('#twit_static').click(function (e) {
		alert("preparing service!");
	});

	$('#twit_test').click(function (e) {
		$.getJSON("/api/testtwit/", {
		})
		.done(function (data) {
			alert(data);
		})
		.fail(function () {
			alert("failed to call ajax api!");
		});
	});
});
