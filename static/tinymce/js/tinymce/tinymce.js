tinymce.init({
    selector: 'textarea',  // change this value according to your HTML
    images_upload_url: 'http://127.0.0.1:8000/upload_question/upload_image/', // Image upload address in Django route
    height: 500,
    plugins: [
        'advlist autolink lists link image charmap print preview anchor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime media table paste code help wordcount'
    ],
    menubar: 'favs file edit view insert format tools table help',
    toolbar: 'undo redo | formatselect | ' +
        'bold italic backcolor | alignleft aligncenter ' +
        'alignright alignjustify | bullist numlist outdent indent | ' +
        'code image | ' +
        'removeformat | help',
    language: 'zh_CN',
});