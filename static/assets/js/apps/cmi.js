const getCookieVanilla = name => {
  let cookieValueVanilla = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      cookieValueVanilla = null
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValueVanilla = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValueVanilla;
}


const payment_lines = [...document.getElementsByClassName("payment-line")]


payment_lines.map(line => {
  line.addEventListener("click", ev => {
    ev.preventDefault()
    let sender = ev.currentTarget
    blockPage()
    calculate(line, sender).then(data => {
      if (data.status_code === 200) {
        toastr.success(data.message, 'Realizado', options = {
          "closeButton": true, "progressBar": true, "newestOnTop": true,
        });
        window.location.reload();
      } else {
        Swal.fire("Se produjo un error", data.error, "error");
      }
    }).catch(data => {
      toastr.error(data.message, 'Error', options = {
        "closeButton": true, "progressBar": true, "newestOnTop": true,
      });
    }).finally(() => {
      KTApp.unblockPage();
    })
  })
})

const calculate = async (line, sender) => {
  const headers = new Headers({
    'X-CSRFToken': getCookieVanilla("csrftoken"),
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  })
  let formData = new FormData()
  formData.append("transition", sender.dataset.transition)
  let url = `/workflow/payments/monthpaymentline/${sender.dataset.pk}/change/`
  let response = await fetch(`${url}`, {
    method: 'POST',
    body: formData,
    headers: headers,
    credentials: "same-origin"
  })
  return await response.json()
}

const blockPage = (state = 'primary', overlayColor = '#000000', message = 'No cierres esta página, estamos procesando tu solicitud...') => {
  KTApp.blockPage({
    overlayColor,
    state,
    message
  });
}

