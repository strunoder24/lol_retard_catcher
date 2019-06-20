class AjaxForm {
    constructor(url, form_fields, success, error) {
        this.url = url;
        this.form_fields = form_fields;
        this.success = success;
        this.error = error
    }
    
    makeCall(){
        let self = this;
        
        $(document).on('submit', '#' + self.url, function (e) {
            e.preventDefault();
            const elements = e.target.elements;
            let fields = {};
            for (let i = 0; i < self.form_fields.length; i++) {
                const field_name = self.form_fields[i];
                fields[field_name] = elements[field_name].value
            }
    
            const save_button = e.target.querySelector('.btn-success');
            save_button.disabled = true;
            $.ajax({
                type: e.target.method.toUpperCase(),
                url: e.target.action,
                data: Object.assign({
                    csrfmiddlewaretoken: elements.csrfmiddlewaretoken.value
                }, fields),

                success: function (r) {
                    self.success(r)
                },
                error: function (e) {
                    const form = document.querySelector('#' + self.url);

                    let message = form.querySelector('#message');
                    let message_text = form.querySelector('#message-text');
                    message_text.innerHTML = e.responseJSON.message;
                    message.style.display = 'block';

                    //Если ошибка случилась сразу разблокируем кнопку сохранения
                    save_button.disabled = false;

                    //Если модалка была закрыта или открыта, то сразу отключай ошибки
                    $('#' + self.url + '_modal').on({
                        'hidden.bs.modal': function (e) {
                            message.style.display = 'none';
                        },
                        'show.bs.modal': function (e) {
                            message.style.display = 'none';
                        }
                    });
                }
            });
        });
    }
}


const add_account = new AjaxForm('add_account', ['username', 'region'],
    function (r) {
        document.location.reload()
    }, function (e) {});

const add_retard = new AjaxForm('add_retard', ['username', 'description', 'lol_account'],
    function () {
        document.location.reload()
    });


add_account.makeCall();
add_retard.makeCall();