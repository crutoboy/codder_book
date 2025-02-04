function hide_visible_password(password_field_obj, hide_visible_btn) {
    hide_visible_btn.addEventListener('click', (event) => {
        event.preventDefault()
        if(password_field_obj.getAttribute('type') == 'password'){        
        hide_visible_btn.setAttribute('uk-icon', 'icon: eye-slash')
        password_field_obj.setAttribute('type', 'text')
        } else {
        hide_visible_btn.setAttribute('uk-icon', 'icon: eye')
        password_field_obj.setAttribute('type', 'password')
        }
    })
}
