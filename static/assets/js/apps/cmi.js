const payment_lines = [...document.getElementsByClassName("payment-line")]


payment_lines.map(line => {
    line.addEventListener("click", ev => {
        ev.preventDefault()
        create_payment(line, ev)
    })
})

const create_payment = (line, ev) => {
    let url = line.dataset.url
    blockPage()
    createPost(url).then(data => {
        if (data.status_code === 200) {
            toastr.success(data.message, 'Realizado', options = {
                "closeButton": true, "progressBar": true, "newestOnTop": true,
            });
        } else {
            toastr.error(data.message, 'Error', options = {
                "closeButton": true, "progressBar": true, "newestOnTop": true,
            });
            let win = window.open(data.url, '_blank');
            win.focus();
        }

    }).catch(data => {
        toastr.error(data.message, 'Error', options = {
            "closeButton": true, "progressBar": true, "newestOnTop": true,
        });
    }).finally(() => {
        KTApp.unblockPage();
    })
}

const createPost = async (url) => {
    let response = await fetch(url)
    return await response.json()
}

const blockPage = (state = 'primary', overlayColor = '#000000', message = 'No cierres esta página, estamos procesando tu solicitud...') => {
    KTApp.blockPage({
        overlayColor,
        state,
        message
    });
}

