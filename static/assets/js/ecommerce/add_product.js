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

const checkout_counter = document.getElementById("checkout_counter")

let url = "/api/v1/purchase/line/"
const headers = new Headers({
    'X-CSRFToken': getCookieVanilla("csrftoken"),
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
})
const change_button = (product, line= {}) => {
    if (product.dataset.type === "add"){
        product.dataset.type = "delete"
        product.innerText = "Quitar del carrito"
        product.classList.remove("btn-primary")
        product.classList.add("btn-danger")
        product.dataset.line = `${line.id}`

    }
    else{
        product.dataset.type = "add"
        product.innerText = "Añadir al carrito"
        product.classList.remove("btn-danger")
        product.classList.add("btn-primary")
        product.dataset.line = ""

    }
    let stock = document.getElementById(`stock-${line.product.reference}`)
    if (stock)
        stock.innerText = `Stock Disponible: ${line.product.available_stock}`
    checkout_counter.innerText = line.lines
}

const init_checkout = purchase => {
    const products = [...document.getElementsByClassName("product-for-checkout")]
    products.map(product => {
        product.addEventListener("click", event => {
            event.preventDefault()
            handleCheckout(purchase, product)
        })
    })
}

const get_form_data = (product, purchase) => {
    let formData = new FormData();
    formData.append("product", product.dataset.reference)
    formData.append("purchase", purchase)
    return formData
}

const run_request = async (method, formData, url) => {
    let response = await fetch(`${url}`, {
        method: method,
        body: formData,
        headers: headers,
        credentials: "same-origin"
    })
    let data = await response.json()
    return {response, data}
}

const add_to_checkout = async (product, purchase) => {
    let formData = get_form_data(product, purchase)
    let {response, data} = await run_request("POST", formData, url)
    if (response.ok) {
        toastr.success(`El producto "${data.product.name} se añadió correctamente"`, "Producto Añadido")
        change_button(product, data)
    } else {
        for (let key in data) {
            toastr.error(data[key], 'Se produjo un error')
        }
    }

}

const remove_to_checkout = async (product, purchase) => {
    let formData = get_form_data(product, purchase)
    let {response, data} = await run_request("DELETE", formData, `${url}${product.dataset.line}/`)
    if (response.ok) {
        toastr.info(`El producto "${data.product.name} se eliminó correctamente del carrito"`, "Producto Eliminado")
        change_button(product, data)
    } else {
        for (let key in data) {
            toastr.error(data[key], 'Se produjo un error')
        }
    }
}

const handleCheckout = (purchase, product, reload) => {
    if (product.dataset.type === "add")
        add_to_checkout(product, purchase).then(() => {})
    else
        remove_to_checkout(product, purchase).then(() => {})
}