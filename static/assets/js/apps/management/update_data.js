const form = document.getElementById("insoles-form");
const modal = document.getElementById("insoles-forms");
let create_form = document.getElementById(`id_create_form`);
let load_data = document.getElementById(`load_data`);
let title_element = document.getElementById(`title`);
let set_url = "";

const params = new URLSearchParams(window.location.search);
const showModal = params.get("show_modal");

const fetchMethodPost = async (
    url,
    form_data,
    credentials = "include",
    headers = {},
) => {
    let response = await fetch(url, {
        method: "POST",
        body: form_data,
        headers: headers,
        credentials: credentials,
    });
    let data = await response.json();
    $(modal).modal("hide");
    if (data.status === 200) {
        toastr.success(
            data.message,
            "Realizado",
            (options = {
                closeButton: true,
                progressBar: true,
                newestOnTop: true,
            }),
        );
        setTimeout(() => {
            window.location.href = data.redirect_url;
        }, 1000);
    } else {
        Swal.fire({
            title: "Se produjo un error",
            text: data.message,
            icon: "error",
        });
    }
};

load_data.addEventListener("click", async (ev) => {
    let forum_id = document.getElementById(`id_forum_id`);
    if (form.checkValidity() && forum_id.value !== "") {
        const formData = new FormData(form);
        formData.delete("csrfmiddlewaretoken");
        const params = new URLSearchParams(formData);
        let url = `${create_form.dataset.url}/${create_form.dataset.formId}/?${params.toString()}`;
        let { create_url, template, title, history } =
            await fetchMethodGet(url);
        load_data.style = "display: none;";
        modal.querySelector("form").action = create_url;
        modal.querySelector("#render_form").innerHTML = "";
        form.dataset.history = history;
        create_form.dataset.forumId = forum_id.value;
        title_element.textContent = `${title}`;
        modal
            .querySelector("#render_form")
            .insertAdjacentHTML("beforeend", template);
        init_inputmask();
        $(".selectpicker").selectpicker("refresh");
    }
});

form.addEventListener("submit", (ev) => {
    ev.preventDefault();
    fetchMethodPost(
        `${create_form.dataset.url}/1/?${create_form.dataset.key}=${create_form.dataset.forumId}&history=${form.dataset.history}`,
        new FormData(form),
    );
});

create_form.addEventListener("click", async (e) => {
    modal.querySelector("#render_form").innerHTML = "";
    await getRenderForm(
        `${create_form.dataset.url}/${create_form.dataset.formIdInput}/`,
    );
    load_data.style = "";
    $(modal).modal("show");
});

const getRenderForm = async (url) => {
    title_element.textContent = "";
    let { create_url, template, history, title } = await fetchMethodGet(url);
    modal.querySelector("form").action = create_url;
    modal.querySelector("#render_form").innerHTML = "";
    form.dataset.history = history;
    title_element.textContent = `${title}`;
    modal
        .querySelector("#render_form")
        .insertAdjacentHTML("beforeend", template);
    init_inputmask();
    $(".selectpicker").selectpicker("refresh");
};

const fetchMethodGet = async (url) => {
    let response = await fetch(url);
    if (response.status !== 200) {
        toastr.error(
            "Los sentimos no se puede realizar esta acción.",
            "No autorizado",
        );
        return Promise.reject(new Error(response.statusText));
    }
    return await response.json();
};

if (showModal) {
    modal.querySelector("#render_form").innerHTML = "";
    create_form.dispatchEvent(new Event("click"));
}
