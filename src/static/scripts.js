const text_input = document.getElementById("gettext");
const sumbit_btn = document.getElementById("generate");

document.getElementById("upload-article").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("upload-article")
    const formData = new FormData(form);

    console.log(formData)

    const response = await fetch('/', {
        method: 'POST',
        body: formData
    });

    if (response.redirected) {
        window.location.href = response.url;
    } else {
        const result = await response.json();
        console.log(result);
    }
});


var loadFile = function(event) {
    var output = document.getElementById('output');
    const border = document.querySelector('.uploadimage');
    const border2 = document.getElementById('imagebox')
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src) 
    }

    border.style.border = "unset";
};  