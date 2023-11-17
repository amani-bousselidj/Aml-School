(function($){
    $(document).ready(function(){
        function updatePermissions() {
            var roleId = $('#id_name').val();
            if (roleId) {
                var url = '/admin/update_permissions/' + roleId + '/';
                $.get(url, function(data) {
                    $('#id_rolepermission_set-TOTAL_FORMS').val(data.forms);
                    $('#id_rolepermission_set-INITIAL_FORMS').val(data.forms);
                    $('#id_rolepermission_set-MIN_NUM_FORMS').val(data.forms);
                    $('#id_rolepermission_set-MAX_NUM_FORMS').val(data.forms);
                    $('#rolepermission_set-group').html(data.html);
                });
            }
        }

        $('#id_name').change(function() {
            updatePermissions();
        });

        updatePermissions();
    });
})(django.jQuery);
