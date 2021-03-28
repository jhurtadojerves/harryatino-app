const nick = document.getElementById("nick");
const buyer = document.getElementById("buyer");
const forum_id = document.getElementById("forum_id");
const search_form = document.getElementById("search_form");
const page = document.getElementById("page");

const keyDownEvent = (element) => {
  element.addEventListener("keydown", (ev) => {
    if (ev.code === "Enter" && ev.target.value !== "") {
      search_form.submit();
    }
  });
};

const clearOnFocus = (element) => {
  element.addEventListener("focus", (ev) => {
    [...search_form.elements].map((el) => {
      if (el.id != "page" && el.id != element.id) {
        el.value = "";
      }
    });
  });
};

keyDownEvent(nick);
keyDownEvent(buyer);
keyDownEvent(forum_id);

clearOnFocus(nick);
clearOnFocus(buyer);
clearOnFocus(forum_id);
