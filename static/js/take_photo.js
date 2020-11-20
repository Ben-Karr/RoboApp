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

            fetch(`${window.origin}/predict`, {
                method: "POST",
                body: form,
                })
            .then(function (response) {

                if (response.status !== 200) {
                    console.log('Wrong');
                    return
                    }

                response.json().then(function (data) {
                    let label = data.label;
                    let confidence = data.confidence;
                    let div = document.createElement('div');
                    div.innerHTML = `<h1> Your circuit is ${label} with a certainty of ${Math.round(confidence * 1000) / 10} % </h1>`;
                    document.body.append(div);
                    })
            })
            .catch(error => {
                console.log(error);
            });
        })
    
        video.srcObject.getTracks().forEach(function (track) {
            track.stop();
        });

        photoButton.remove();
        uploadButton.remove();
        video.remove();

    })
})