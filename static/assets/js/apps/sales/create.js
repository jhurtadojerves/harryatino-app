const product = $("#id_product")
const id_available = document.getElementById("id_available")

const URL = "/api/v1/product/"


const get_product = async product => {
    let response = await fetch(`${URL}${product}`)
    let data = await response.json()
    return data.available_by_default
}

product.on('change', function (e){
    get_product(product.val()).then(checked => {
        id_available.checked = checked
    })
})