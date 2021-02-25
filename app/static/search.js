$('#searchModal').on('shown.bs.modal', (function () {
    bootstrapValidate('#gr', 'numeric:Please only enter numeric characters!', function (isValid) {
   if (isValid) {
       $('#submit').attr('disabled', false);
   } else {
       $('#submit').attr('disabled', true);
   }
});
}));
