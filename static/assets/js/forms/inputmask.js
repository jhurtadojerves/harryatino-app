const calendar_mask = () => {

  const init_inputmask = function (selector) {
    let elem = selector ? $(selector) : $(document);
    elem.find(".input-mask").inputmask();
  }


  document.addEventListener("DOMContentLoaded", () => {
    init_inputmask();
  });
}

calendar_mask()
const init_inputmask = function (selector) {
  let elem = selector ? $(selector) : $(document);
  elem.find(".input-mask").inputmask();
}