export async function uploadFile(file){   
    
//formData is a standard browser format for sending files over HTTP.HTTP can't send raw JS objects — needs standard packaging

    const formData = new FormData();   // Creates an empty FormData to wrap the file uploaded by the user
    formData.append("file",file);      // Appends the uploaded file from user to send it to FastAPI

    const response = await fetch("http://127.0.0.1:8000/upload", {   // fetch sends a POST request to the URL (FastAPI). The file travels from React → FastAPI
        method: "POST",
        body: formData
    });
    const data = await response.json();     //response.json() specifically parses the raw HTTP response into a JavaScript object
    return data;            
}