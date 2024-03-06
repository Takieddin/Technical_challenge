document.addEventListener('DOMContentLoaded', function () {
    fetchImagesAndUpdateList();

    document.getElementById('addNew').addEventListener('click', function () {
        document.getElementById('fileInput').click();
    });

    document.getElementById('fileInput').addEventListener('change', function (event) {
        uploadImage(event.target.files[0]);
    });

    document.getElementById('generateFrame').addEventListener('click', function() {
        if (window.currentlySelectedImageId) {
            selectImage(window.currentlySelectedImageId);
        }
    });
});

function fetchImagesAndUpdateList() {
    fetch('/images')
        .then(response => response.json())
        .then(data => {
            updateImageList(data.images);
        })
        .catch(error => {
            console.error('Error fetching images:', error);
            displayErrorMessage('Failed to fetch images. Please try with diffrent depth values');
            alert('Failed to fetch images. Please try with diffrent depth values');
        });
}

function updateImageList(images) {
    const list = document.getElementById('imageList');
    list.innerHTML = '';
    images.forEach(image => {
        const listItem = document.createElement('li');
        listItem.textContent = image.name;
        listItem.addEventListener('click', function () {
            window.currentlySelectedImageId = image.id; // Store the current image ID globally
            selectImage(image.id);
            highlightSelectedItem(listItem, list);
        });
        list.appendChild(listItem);
    });
}

function highlightSelectedItem(selectedItem, list) {
    Array.from(list.children).forEach(item => {
        item.classList.remove('selected');
    });
    selectedItem.classList.add('selected');
}

function selectImage(imageId) {
    let queryParams = getQueryParams();
    fetch(`/images/${imageId}?${queryParams}`)
        .then(response => response.blob())
        .then(blob => {
            const imageUrl = URL.createObjectURL(blob);
            const mainImage = document.getElementById('main-image');
            mainImage.src = imageUrl;
            mainImage.onload = () => {
                if (window.panzoomInstance) {
                    window.panzoomInstance.destroy();
                }
                window.panzoomInstance = Panzoom(mainImage, {
                    maxScale: 10,
                    contain: 'false',
                    startScale: 1,
                    cursor: 'move',
                    which: 1 // Left mouse button drag to pan
                });
                mainImage.parentElement.addEventListener('wheel', window.panzoomInstance.zoomWithWheel);
            };
        })
        .catch(error => {
            displayErrorMessage('Failed to fetch images. Please try with diffrent depth values');
            console.error('Error fetching image:', error);
            alert('Failed to load selected image. Please try again later.');
        });
}

function uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    fetch('/images', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(() => {
            fetchImagesAndUpdateList();
        })
        .catch(error => {
            console.error('Error uploading image:', error);
            displayErrorMessage('Failed to fetch images. Please try with diffrent depth values');
            alert('Failed to upload image. Please try again later.');
        });
}

function getQueryParams() {
    const depthMin = document.getElementById('depthMinInput').value;
    const depthMax = document.getElementById('depthMaxInput').value;

    let params = new URLSearchParams();
    params.append('depth_min', depthMin);
    params.append('depth_max', depthMax);
    return params.toString();
}
function displayErrorMessage(message) {
    const errorDiv = document.getElementById('errorMessages');
    errorDiv.textContent = message; // Set the error message
    errorDiv.style.display = 'block'; // Make the error message visible
}