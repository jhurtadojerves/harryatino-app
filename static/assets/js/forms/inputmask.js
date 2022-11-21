init_inputmask = selector => {
  let elem = selector ? $(selector) : $(document)
  elem.find(".input-mask").inputmask();

  document.querySelectorAll(".btn-today").forEach(btn => {
    console.log(btn)
    btn.addEventListener("click", event => {
      let date = new Date()
      let input = event.currentTarget.closest(".input-group").querySelector('.input-mask');
      let value = date.toLocaleDateString()
      let string_date = value.split("/")
      let day = parseInt(string_date[0])
      let month = parseInt(string_date[1])
      if (day < 10) {
        string_date[0] = `0${day}`
      }
      if (month < 10) {
        string_date[1] = `0${month}`
      }
      input.value = string_date.join("/")
    });
  });
}
init_inputmask();
