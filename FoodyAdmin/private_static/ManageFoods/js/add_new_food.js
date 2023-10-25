const Img_Preview_Container = document.querySelector(".preview_food_image")
const FoodImageField = document.querySelector("#Images")

function if_have_img_preview_show() {
    img = FoodImageField.dataset.img
    if (img) {
        img = FoodImageField.dataset.img.split(",")
        img.forEach((each, index) => {
            let img_src = `/${getServerPath()}/Foods/` + each
            let size = `سایز فایل انتخابی:  NULL MB`
            let name_file = 'NULL'
            let name = `نام فایل انتخابی: ${name_file}`
            setTimeout(e => {
                create_img_preview_card(img_src, name, size)
            }, 300 * index)
        })
    }

}

if_have_img_preview_show()


FoodImageField.oninput = (e) => {
    Img_Preview_Container.innerHTML = ""
    for (let i = 0; i < FoodImageField.files.length; i++) {
        let img_file = FoodImageField.files[i]
        let img_src = URL.createObjectURL(img_file)
        let size = `سایز فایل انتخابی: ${(FoodImageField.files[i].size * 0.000001).toFixed(2)}MB`
        let name_file = new String(FoodImageField.files[i].name).length <= 15 ? e.target.files[i].name : e.target.files[i].name.slice(0, 15) + '...'
        let name = `نام فایل انتخابی: ${name_file}`
        setTimeout(e => {
            create_img_preview_card(img_src, name, size, i)
        }, 300 * i)

    }
}

function create_img_preview_card(img_src, name, size, delete_id) {
    const UpperParent = document.createElement("div")
    UpperParent.className = "col-lg-3 col-md-4 col-sm-6 col-12 my-2 fadeIn"

    const img_pre = document.createElement("img")
    img_pre.className = "img-fluid img-thumbnail"
    img_pre.src = img_src

    const parentDiv = document.createElement("div")
    parentDiv.className = ("card shadow")
    // parentDiv.style.zIndex = -1

    const CardHeader = document.createElement("div")
    const CardBody = document.createElement("div")
    const CardFooter = document.createElement("div")

    CardHeader.classList.add("card-header")
    CardHeader.innerText = name

    CardBody.className = ("card-body d-flex justify-content-center align-items-center")
    CardBody.style.Height = "480px"
    // CardBody.style.maxHeight = "500px"
    CardBody.appendChild(img_pre)

    CardFooter.classList.add("card-footer")
    const FoooterContainer = document.createElement("div")
    FoooterContainer.className = "d-flex justify-content-between align-items-center"
    const FooterSizeP = document.createElement("p")
    FooterSizeP.className = "p-0 m-0"
    FooterSizeP.innerText = size

    const delete_button = document.createElement("span")
    delete_button.className = "btn"
    const TrashIcon = document.createElement("i")
    TrashIcon.className = "bi bi-trash3-fill text-danger fs-3"
    delete_button.appendChild(TrashIcon)
    delete_button.setAttribute('data-delete', delete_id)
    delete_button.onclick = (e) => {
        const parentDiv = delete_button.parentElement.parentElement.parentElement.parentElement
        delete_card_preview_img(parentDiv, delete_button.dataset.delete)
    }

    FoooterContainer.appendChild(delete_button)
    FoooterContainer.appendChild(FooterSizeP)

    CardFooter.appendChild(FoooterContainer)

    parentDiv.appendChild(CardHeader)
    parentDiv.appendChild(CardBody)
    parentDiv.appendChild(CardFooter)
    UpperParent.appendChild(parentDiv)
    Img_Preview_Container.appendChild(UpperParent)
}


function delete_card_preview_img(parentDiv, imgIndex) {
    if (!imgIndex || imgIndex == 'undefined') {
        Swal.fire({
            text: "عکس پیش فرض را نمی توان حذف کرد",
            title: "خطا",
            icon: "warning"
        })
        return;
    }
    parentDiv.classList.add("hide_preview_img")

    FoodImageField.files[FoodImageField].value = ""

    setTimeout(parentDiv.remove(), 1000)
}
