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

// xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
