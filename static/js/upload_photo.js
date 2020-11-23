import fetch_form from './fetch_form.js'

const canvas = document.querySelector('#canvas');
const context = canvas.getContext('2d');
const input = document.querySelector('input[type=file]');
const uploadButton = document.getElementById('upload-button')

input.addEventListener('change', function (event) {
    //console.log(input.files) 
    const reader = new FileReader();

    reader.onload = function () {
        const img = new Image();

        img.onload = function () {
            context.drawImage(img, 0, 0, canvas.width, canvas.height);

            uploadButton.addEventListener('click', function () {
                console.log('upload image')

                canvas.toBlob(function (blob) {
                    const form = new FormData();
                    form.append('image', blob, 'tmp_image.png');

                    fetch_form(form);
                })

                uploadButton.remove();
                input.remove();
            })
        }
        img.src = reader.result;

    }
    reader.readAsDataURL(input.files[0]);

}, false)