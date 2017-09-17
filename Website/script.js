function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}

function getPhoneNumber() {
	var phoneNum = document.getElementById("num").value
	var reg = new RegExp('^[0-9]+$');
	if (phoneNum.length == 11 && reg.test(phoneNum)) {
		sendNumber(phoneNum);	
	} else {
		alert("Invalid input");
	}
}

function sendNumber(phoneNum) {
    var xhr = new XMLHttpRequest();
    var url = "https://1861e012.ngrok.io/website";
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var json = JSON.parse(xhr.responseText);
        //console.log(json.phone + ", " + json.password);
    }
        };
    var data = JSON.stringify({"phone": phoneNum});
    xhr.send(data);
}


