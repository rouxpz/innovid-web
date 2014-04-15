var form = document.getElementById("upload");
var formData = new FormData(form);

//getElementById
function $id(id) {
	return document.getElementById(id);
}

//output information
function Output(msg) {
	var m = $id("messages");
	m.innerHTML = msg + m.innerHTML;
}

//call initialization file
if (window.File && window.FileList && window.FileReader) {
	Init();
}

//initialize
function Init() {

	var fileselect = $id("fileupload"),
		filedrag = $id("filedrag"),
		submitbutton = $id("submitbutton");

	//file select
	fileselect.addEventListener("change", FileSelectHandler, false);

	//is XHR2 available?
	var xhr = new XMLHttpRequest();
	if(xhr.upload) {

		//file drop
		filedrag.addEventListener("dragover", FileDragHover, false);
		filedrag.addEventListener("dragleave", FileDragHover, false);
		filedrag.addEventListener("drop", FileSelectHandler, false);
		filedrag.style.display = "block";

		fileselect.style.display = "none";

		submitbutton.onclick = function() {
			// t = document.getElementById('title').value
			// formData.append('title', t)
			// alert(formData['fileupload']);
			try {
			xhr.open('POST', "/", true);
			xhr.setRequestHeader("Content-Type", "multipart/form-data");
			xhr.send(formData);
		} catch (err) {
			alert("uh oh there was an error");
		}
		};
	}
}

// file drag hover
function FileDragHover(e) {
	e.stopPropagation();
	e.preventDefault();
	e.target.className = (e.type == "dragover" ? "hover" : "");
}

// file selection
function FileSelectHandler(e) {

	// cancel event and hover styling
	FileDragHover(e);

	// fetch FileList object
	var files = e.target.files || e.dataTransfer.files;

	// process all File objects
	for (var i = 0, f; f = files[i]; i++) {
		ParseFile(f);
		formData.append('fileupload', f);
		console.log(formData['file']);
	}

	console.log(formData);

}

function ParseFile(file) {

	Output(
		"<p>File information: <strong>" + file.name +
		"</strong> type: <strong>" + file.type +
		"</strong> size: <strong>" + file.size +
		"</strong> bytes</p>"
	);	
}