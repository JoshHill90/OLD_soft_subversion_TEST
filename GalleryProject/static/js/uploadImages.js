// Grouping DOM element selections
const uploadButton = document.getElementById("uploadButton");
const loaderBar = document.getElementById('dotsLoader');
const imageUpload = document.getElementById("imageUpload");
const imageCreatePage = document.getElementById('imageCreatePage').value;
const url = document.getElementById('url').value;
const uploadDiv = document.getElementById('uploadsection');
const uploadAnimationDiv = document.getElementById('uploadAnimation');
const loadValid = document.getElementById('validate');
const LoadBackend = document.getElementById('backend');
const fileLoader = document.getElementById('fileLoader');
const fileLoaderRow = document.getElementById('fileLoaderRow');

// Function to display error message and reset UI
function displayError(message) {
    alert(message);
    uploadButton.style.display = 'block';
    loaderBar.style.display = 'none';
    loadValid.style.display = 'none';
	uploadDiv.classList.remove('noshow')
	uploadAnimationDiv.classList.add('noshow');
}

// Handling file upload button click
uploadButton.addEventListener("click", uploadFiles);

// Handling file upload
async function uploadFiles(event) {
    event.preventDefault();
    const csrftoken = getCookie('csrftoken');
    const fileLimit = 100;
    const imageFiles = imageUpload.files;

	uploadDiv.classList.add('noshow')
    uploadAnimationDiv.classList.remove('noshow');
    uploadButton.style.display = 'none';
    loaderBar.style.display = 'flex';
    loadValid.style.display = 'flex';

    if (imageFiles.length === 0) {
        // Using the displayError function for consistent error handling
        displayError("Please select at least one image file of a valid format to upload.");
        return;
    }

    if (imageFiles.length > fileLimit) {
        displayError(`Please select up to ${fileLimit} files.`);
        return;
    }

    for (let fileObj = 0; fileObj < imageFiles.length; fileObj++) {
        const maxSize = ((imageFiles[fileObj].size / 1024) / 1024).toFixed(4);
        const allowedFiles = /\.(png|gif|jpg|jpe?g|svg)$/i;

        if (imageFiles[fileObj].name === "item" || maxSize >= 10) {
            displayError("Please check your images, individual images can be no larger than 10Mb");
            return;
        }

        if (!allowedFiles.exec(imageFiles[fileObj].name)) {
            displayError("Only valid image types can be uploaded, PNG, GIF, JPEG, JPG, SVG");
            return;
        }
    }

    let data = { 'file_count': imageFiles.length, 'cf_data': 'cf_data' };
    LoadBackend.style.display = 'flex';

    try {
        // Using async/await for better readability
        const responseData = await (await fetch(url, {
            method: 'POST',
            body: JSON.stringify(data),
            credentials: 'same-origin',
            headers: {
                'cf_data': 'cf_data',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        })).json();

        loadValid.style.display = 'none';
        LoadBackend.style.display = 'none';

        // Using destructuring to get the result from uploadImages function
        const { backEndData, redirectUrl } = await uploadImages(responseData, imageFiles, imageCreatePage);
        delayedRedirect(backEndData, redirectUrl);
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while processing the request, please refresh and try again. If the issue persists, please contact the site admin.');
        return;
    }
}

// Function to upload images to the backend
async function uploadImages(responseData, imageFiles, pageURL) {
    let fileCounter = 0;
    const backEndData = [];

    fileLoader.classList.remove('noshow');

    for (const cfData of responseData) {
        const cloudflareId = cfData.cf_id;
        const cloudflareURL = cfData.cf_url;

        const imgMultiPart = new FormData();

        // Creating DOM elements for progress display
        const divCol = document.createElement('div');
        divCol.className = 'col-12 col-md-3 mb-1';
        fileLoaderRow.appendChild(divCol);

        const progLoader = document.createElement('div');
        progLoader.className = 'loaderFile';
        divCol.appendChild(progLoader);

        const nameLoader = document.createElement('p');
        nameLoader.className = 'p-p';
        nameLoader.innerHTML = '#' + fileCounter + ' ' + imageFiles[fileCounter].name;
        divCol.appendChild(nameLoader);

        imgMultiPart.append("file", imageFiles[fileCounter]);

        try {
            const response = await fetch(cloudflareURL, {
                method: "post",
                body: imgMultiPart,
            });

            if (!response.ok) {
                // Check if the response status is not OK (HTTP 2xx)
                console.error(`Request failed with status: ${response.status}`);
                progLoader.classList.remove('loaderFile');
                progLoader.classList.add('loadedFailed');
                return false;
            }

            // If the response is OK, continue with your logic
            progLoader.classList.remove('loaderFile');
            progLoader.classList.add('loadedFile');
            backEndData.push(cloudflareId);
        } catch (error) {
            console.error(error);

            progLoader.classList.remove('loaderFile');
            progLoader.classList.add('loadedFailed');
            return false;
        }

        fileCounter++;
        fileLoader.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }

    return { 'backEndData': backEndData, 'redirectUrl': pageURL };
}

// Function to handle delayed redirect
function delayedRedirect(backEndData, redirectUrl) {
    const csrfGet = getCookie('csrftoken');
    const data = { 'data': backEndData };

    fetch(redirectUrl, {
        method: 'POST',
        body: JSON.stringify(data),
        credentials: 'same-origin',
        headers: {
            'cf_data': 'cf_data',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfGet
        }
    })
    .then(response => response.text())
    .then(response => {
        const newURL = response.slice(1, -1);
        window.location.href = newURL;
    })
    .catch(error => console.error('Error:', error));
}
