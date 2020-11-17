let canvas = document.querySelector('#canvas');
let context = canvas.getContext('2d');
let video = document.querySelector('#video');



if ( navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
    navigator.mediaDevices.getUserMedia({video: { //width: {ideal: 1920},
                                                  //height: {ideal: 1080},
                                                  facingMode: "environment",
                                                }
                                        }).then(stream => {
        video.srcObject = stream;
        video.play()
    });
}

document.getElementById('snap').addEventListener('click', () => {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);


    video.srcObject.getTracks().forEach(function(track) {
        track.stop();
      });

    canvas.toBlob(function (blob){
        const form = new FormData();
        form.append('image', blob, 'tmp_image.png');
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/take', true);
        xhr.send(form);
    })

    video.style.display = "none";
    document.querySelector("#snap").style.display = "none";
})