const input = document.querySelector('input[type="file');

input.addEventListener('change', function(event){
    console.log(input.files)
    const reader = new FileReader();

    reader.onload = function() {
        console.log(reader.result);
        const img = new Image();

        img.onload = function (){
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');

            context.drawImage(img, 0, 0, canvas.width, canvas.height);
            document.body.appendChild(canvas);
            canvas.toBlob(function (blob){
                const form = new FormData();
                form.append('image', blob, 'tmp_image.png');
                const xhr = new XMLHttpRequest();
                xhr.open('POST', '/upload', true);
                xhr.send(form);
            })
        }
        img.src = reader.result;
    }

    reader.readAsDataURL(input.files[0]);

}, false)