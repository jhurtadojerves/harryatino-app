const elements = document.querySelectorAll('.transition-line');
elements.forEach(elem => {
    elem.addEventListener('click', event => {
        event.preventDefault();
        let sender = event.currentTarget
        let linePk = sender.dataset.pk
        console.log(linePk)
        let formId = `stateFormLine-${linePk}`
        console.log(formId)
        const form = document.getElementById(formId);
        form.querySelector('[name=transition]').value = sender.dataset.transition;
        let data = new FormData(form);
        KTApp.blockPage({
            overlayColor: '',
            state: 'primary',
            message: 'No cierres esta página, estamos actualizando el perfil...'
        });
        workflowChangeState(form.action, data).then(resonse => {
            Swal.fire({
                icon: "success",
                text: "Acción realizada con éxito",
                timer: 2000,
                timerProgressBar: true,
            }).then((result) => {
                if (result.isDismissed || result.isConfirmed) {
                    window.location.reload();
                }
            })
        }).catch(data => {
            toastr.error(data.message, 'Error', options = {
                "closeButton": true,
                "progressBar": true,
                "newestOnTop": true,
            });
        }).finally(() => {
            KTApp.unblockPage();
        })
    })
})
