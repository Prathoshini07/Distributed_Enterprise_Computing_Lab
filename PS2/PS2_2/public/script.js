document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('drawing-board');
    const colorPicker = document.getElementById('color-picker');
    const brushSize = document.getElementById('brush-size');
    const clearBtn = document.getElementById('clear-btn');
 
 
    // Set canvas to full window size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
 
 
    const ctx = canvas.getContext('2d');
    const socket = io();
 
 
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;
 
 
    // Drawing function
    function draw(x, y, color, size, isLocal = true) {
        ctx.beginPath();
        ctx.strokeStyle = color;
        ctx.lineWidth = size;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
       
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.stroke();
       
        lastX = x;
        lastY = y;
 
 
        // If drawing is local, emit to server
        if (isLocal) {
            socket.emit('draw', {
                x,
                y,
                color,
                size,
                lastX: lastX,
                lastY: lastY
            });
        }
    }
 
 
    // Mouse events for drawing
    canvas.addEventListener('mousedown', (e) => {
        isDrawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
    });
 
 
    canvas.addEventListener('mousemove', (e) => {
        if (!isDrawing) return;
        draw(
            e.offsetX,
            e.offsetY,
            colorPicker.value,
            brushSize.value
        );
    });
 
 
    canvas.addEventListener('mouseup', () => {
        isDrawing = false;
    });
 
 
    canvas.addEventListener('mouseout', () => {
        isDrawing = false;
    });
 
 
    // Socket event for receiving drawing from other clients
    socket.on('draw', (drawData) => {
        const currentColor = ctx.strokeStyle;
        const currentLineWidth = ctx.lineWidth;
 
 
        ctx.beginPath();
        ctx.strokeStyle = drawData.color;
        ctx.lineWidth = drawData.size;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
       
        ctx.moveTo(drawData.lastX, drawData.lastY);
        ctx.lineTo(drawData.x, drawData.y);
        ctx.stroke();
 
 
        // Restore previous color and line width
        ctx.strokeStyle = currentColor;
        ctx.lineWidth = currentLineWidth;
    });
 
 
    // Clear canvas functionality
    clearBtn.addEventListener('click', () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        socket.emit('clear-canvas');
    });
 
 
    // Server-side clear canvas event
    socket.on('clear-canvas', () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    });
 
 
    // Restore drawing history when first connecting
    socket.on('drawing-history', (history) => {
        history.forEach(drawData => {
            const currentColor = ctx.strokeStyle;
            const currentLineWidth = ctx.lineWidth;
 
 
            ctx.beginPath();
            ctx.strokeStyle = drawData.color;
            ctx.lineWidth = drawData.size;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
           
            ctx.moveTo(drawData.lastX, drawData.lastY);
            ctx.lineTo(drawData.x, drawData.y);
            ctx.stroke();
 
 
            // Restore previous color and line width
            ctx.strokeStyle = currentColor;
            ctx.lineWidth = currentLineWidth;
        });
    });
 
 
    // Resize canvas when window is resized
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
 });
 