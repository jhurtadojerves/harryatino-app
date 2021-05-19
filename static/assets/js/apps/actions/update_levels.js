let create_form = document.getElementById(`id_create_form`)

const fetchMethodGet = async (url) => {
    let response = await fetch(url)
    let data = await response.json()
    KTApp.unblockPage();
    if (data.status === 200) {
        toastr.success(data.message, 'Realizado', options = {
            "closeButton": true, "progressBar": true, "newestOnTop": true,
        });
    } else {
        toastr.error(data.message, 'Error', options = {
            "closeButton": true, "progressBar": true, "newestOnTop": true,
        });
    }
}

create_form.addEventListener("click", async (e) => {
    KTApp.blockPage({
        overlayColor: '#000000',
        state: 'primary',
        message: 'No cierres esta página, estamos procesando tu solicitud...'
    });
    fetchMethodGet(create_form.dataset.url).then(data => data).catch(error => {
        KTApp.unblockPage();
    })
})