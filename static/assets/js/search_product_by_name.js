const search = document.getElementById("name");
const search_form = document.getElementById("search_form");
if (search) {
    search.addEventListener("keydown", (ev) => {
        if (ev.code === "Enter") {
            search_form.submit();
        }
    });
}
