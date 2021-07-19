let initMessages = () => {
    let messages = document.querySelectorAll(".toast-message");
    messages.forEach(message => {  
        const tag = message.dataset.tags
        if (tag == "success") {
            toastr.success(message.dataset.message, "Acción satisfactoria")
        } else if (tag == "error") {
            toastr.error(message.dataset.message, "Resuelva el siguiete conflicto")
        } else if (tag == "info") {
            toastr.info(message.dataset.message, "Información")
        }
    });
}

document.addEventListener('DOMContentLoaded', event => {
    initMessages();
});