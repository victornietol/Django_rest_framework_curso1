async function enviarPeticion(event) {
    event.preventDefault();

    const url = "http://127.0.0.1:8000/login/"
    const form = document.getElementById("form");
    const _data = {
        username: form.username.value,
        password: form.password.value
    }
    
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {"Content-type": "application/json"},
            body: JSON.stringify(_data)
        });

        const body = await response.json(); // Obteniendo respuesta
        console.log(body);

        // Mensaje dependiendo la respuesta
        if (response.ok) {
            console.log(body.message);
        } else {
            console.log(body.error);
        }


    } catch (error) {
        console.error("Error: ", error);
    }
}