const product = document.getElementById("product");
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

keyDownEvent(product);
keyDownEvent(buyer);
keyDownEvent(forum_id);
