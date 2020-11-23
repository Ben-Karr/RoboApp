import fetch_form from './fetch_form.js'

const canvas = document.querySelector('#canvas');
const context = canvas.getContext('2d');
const video = document.querySelector('#video');
const uploadButton = document.getElementById('upload-button');
const photoButton = document.getElementById('snap');

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({
        video: { //width: {ideal: 1920},
            //height: {ideal: 1080},
            facingMode: "environment",
        }
    }).then(stream => {
        video.srcObject = stream;
        video.play()
    });
}

photoButton.addEventListener('click', () => {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    uploadButton.addEventListener('click', function () {

        canvas.toBlob(function (blob) {
            const form = new FormData();
            form.append('image', blob, 'tmp_image.png');

            fetch_form(form);
        })
    
        video.srcObject.getTracks().forEach(function (track) {
            track.stop();
        });

        photoButton.remove();
        uploadButton.remove();
        video.remove();

    })
})