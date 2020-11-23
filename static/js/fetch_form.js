export default function fetch_form(content) {
    fetch(`${window.origin}/predict`, {
        method: "POST",
        body: content,
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
}
