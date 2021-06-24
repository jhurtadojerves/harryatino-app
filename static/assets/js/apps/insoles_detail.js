const insoles_detail = () => {
    const get_data = async (url) => {
        let response = await fetch(url)
        return await response.json()
    }

    const render = (template, url) => {
        if (template.length <= 1) {
            window.location.href = url
        }
        const modal = document.getElementById('insoles-detail')
        modal.querySelector('.modal-body').innerHTML = '';
        modal.querySelector('.modal-body').insertAdjacentHTML('beforeend', template);
        $(modal).modal('show');
        initSelect2(modal);
        addListener()
    }

    const handleClick = (ev, element) => {
        ev.preventDefault()
        get_data(element.dataset.url).then(response => {
            let {template} = response
            render(template, element.dataset.originurl)
        }).catch(error => {
            console.log(error)
        })
    }

    const addListener = () => {
        const insole_details = [...document.getElementsByClassName("insoles-detail")]
        insole_details.map(detail => {
            detail.addEventListener("click", e => {
                handleClick(e, detail)
            })
        })
    }

    addListener()
}

insoles_detail()