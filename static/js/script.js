document.getElementById('file_upload').onchange = function () {
    document.getElementById('file_name').value = this.value.slice(12,100);
};

