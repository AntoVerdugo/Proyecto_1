// static/js/chat_polling.js (CÓDIGO COMPLETO)

// Envolvemos el código en una función autoejecutable para un scope seguro
(function() {
    
    // 🛑 1. Leer la variable global 'room_id' (inyectada desde room.html)
    const currentRoomId = typeof room_id !== 'undefined' ? room_id : null; 
    
    if (!currentRoomId) {
        console.error("ERROR FATAL: La ID de la sala no está disponible. No se puede iniciar el polling.");
        return;
    }

    // 2. Función principal que llama a la vista AJAX (Recarga el fragmento de mensajes)
    function recargarMensajes() {
        var url_ajax = `/room/${currentRoomId}/messages/`;
        var $box = $('#BoxMessage');

        // Calcular si el usuario está cerca del final (para scroll automático)
        var currentScroll = $box.scrollTop() + $box.outerHeight();
        var isScrolledToBottom = currentScroll >= $box[0].scrollHeight - 50; 

        $.ajax({
            url: url_ajax,
            type: 'GET',
            success: function(data) {
                // Si el contenido ha cambiado, actualiza el DOM
                if ($box.html() !== data) {
                    $box.html(data);
                    
                    // Si el usuario estaba abajo, fuerza el scroll al nuevo mensaje
                    if (isScrolledToBottom) {
                        $box.scrollTop($box[0].scrollHeight);
                    }
                }
            },
            error: function(xhr, status, error) {
                console.error("Fallo al obtener mensajes:", error);
            }
        });
    }

    // 🛑 3. INICIALIZACIÓN: Ejecutar el polling inmediatamente y con el temporizador
    // Inicia la recarga inmediatamente y luego cada 3 segundos.
    recargarMensajes();
    setInterval(recargarMensajes, 3000); 

    // 4. Asegurar el scroll inicial al final (al cargar la página)
    $(document).ready(function() {
        $('#BoxMessage').scrollTop($('#BoxMessage')[0].scrollHeight); 
    });
    
})();