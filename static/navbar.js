const btnDropdown = document.getElementById('btn-dropdown')
const dropdownnBox = document.getElementById('dropdown-box')
const dropdown = document.getElementById('dropdown')

btnDropdown.addEventListener('click', () => {
    dropdown.classList.toggle('hidden')
    dropdown.classList.contains('hidden') ?
        btnDropdown.innerHTML = 'menu &nbsp; <i class="fa-solid fa-caret-down"></i>'
    :
        btnDropdown.innerHTML = 'menu &nbsp; <i class="fa-solid fa-xmark"></i>'
})

dropdownnBox.addEventListener('mouseleave', () => {
    dropdown.classList.add("hidden")
    btnDropdown.innerHTML = 'menu &nbsp; <i class="fa-solid fa-caret-down"></i>'
})