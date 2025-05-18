const initDetailProfile = () => {
    let originalDataBtn = document.getElementById("original-data-btn");
    let newDataBtn = document.getElementById("new-data-btn");
    let originalDataModal = document.getElementById("original-data-modal");
    let newDataModal = document.getElementById("new-data-modal");

    originalDataBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        $(originalDataModal).modal("show");
    });
    newDataBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        $(newDataModal).modal("show");
    });
};

initDetailProfile();
