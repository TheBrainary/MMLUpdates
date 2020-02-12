async function PackageApp() {
	appname = ""
	const {value: formValues} = await Swal.fire({
	title: 'App Details',
	html:
		'<label class="control-label" >App Name</label>' +
		'<input id="swal-input1" class="swal2-input" style="margin:0px auto 20px auto">',
	focusConfirm: false, 
	preConfirm: () => {
		appname = document.getElementById('swal-input1').value
		return document.getElementById('swal-input1').value
	}
	})
	if (formValues) {
		document.getElementById('BlocklyFrame').contentWindow.send_data_package(event,this,appname)
	return appname
	}
}

function test2(){
	Swal.fire({
  title: 'App Name',
  input: 'text',
  inputAttributes: {
    autocapitalize: 'off'
  },
  showCancelButton: true,
  confirmButtonText: 'Install',
  showLoaderOnConfirm: true,
  preConfirm: (login) => {
		
		return login
  }})
  }


function wifiSet(){
	Swal.fire({
		position: 'top-end',
		type: 'success',
		title: 'WiFi details have been saved\n\nMiRo will connect shortly.',
		showConfirmButton: false,
		timer: 1500
	})	
}

function Test(){
	var x = PackageApp()
	var p = Promise.reslove(x)
	p.then(function(v) {
		console.log(v[0]); // 1
	});
	
}

