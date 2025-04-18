document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("login-form")
    const formData = new FormData(form);

    console.log(formData)

    const response = await fetch('/auth/login', {
        method: 'POST',
        body: formData
    });

    if (response.redirected) {
        window.location.href = response.url;
    } else {
        const result = await response.json();

        const invalidLoginDiv = document.querySelector('.invalid-login');
        if (result.error) { 
            invalidLoginDiv.style.display = 'none'; 
        } else {
            invalidLoginDiv.style.display = 'block'; 
        }
        console.log(result);
    }
});