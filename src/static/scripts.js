alt_text_output = document.getElementById("getalttext")
image_caption_output = document.getElementById("getcaption")

document.getElementById("upload-article").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("upload-article")
    const formData = new FormData(form);

    /* 
    
    validation needed on image and text 

    */

    console.log(formData)

    const response = await fetch('/post/', {
        method: 'POST',
        body: formData
    });

    if (response.redirected) {
        window.location.href = response.url;
    } 

    const result = await response.json();
    
    alt_text_output.value = result['generated-alt-text'];
    image_caption_output.getElementById("getcaption").value = result['generated-image-caption'];
});

document.getElementById("save-alt").addEventListener("click", async (e) => {
    e.preventDefault()
    
    let alt_text_content = alt_text_output.value

    const response = await fetch('/post/save-alt-text/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({alt_text: alt_text_content})
    });

    if (response.status == 401 ) {
        window.location.href = '/auth/login';
    } 

    if (response.ok) {
        console.log("Alt-Text Saved Successfully")
    } else {
        console.log("Saving Error")
    }
})


let loadFile = function(event) {
    let output = document.getElementById('output');
    const border = document.querySelector('.uploadimage');
    const border2 = document.getElementById('imagebox')
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src) 
    }

    border.style.border = "unset";
};  

document.getElementById("copy-alt").addEventListener("click", async (e) => {
    e.preventDefault()
    alt_text_output.select();
    alt_text_output.setSelectionRange(0, 9999);

    navigator.clipboard.writeText(alt_text_output.value);
    console.log("Alt-Text Copied to Clipboard")

    alt_text_output.blur();
});

document.getElementById("copy-caption").addEventListener("click", async (e) => {
    e.preventDefault()
    image_caption_output.select();
    image_caption_output.setSelectionRange(0, 9999);

    navigator.clipboard.writeText(image_caption_output.value);
    console.log("Image Caption Copied to Clipboard")

    image_caption_output.blur();
});