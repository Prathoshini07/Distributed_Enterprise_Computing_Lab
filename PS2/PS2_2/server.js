const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');
const fs = require('fs');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Load index.html
const indexHTML = fs.readFileSync(path.join(__dirname, 'public', 'index.html'), 'utf8');

// Serve the main page
app.get('/', (req, res) => {
  res.send(indexHTML);
});

// Store drawing history
let drawingHistory = [];

// Socket.IO connection handling
io.on('connection', (socket) => {
  console.log('A user connected');

  // Send existing drawing history to newly connected client
  socket.emit('drawing-history', drawingHistory);

  // Handle drawing events
  socket.on('draw', (drawData) => {
    // Broadcast drawing to all other clients
    socket.broadcast.emit('draw', drawData);

    // Store drawing in history
    drawingHistory.push(drawData);
  });

  // Handle clear canvas event
  socket.on('clear-canvas', () => {
    drawingHistory = [];
    io.emit('clear-canvas');
  });

  socket.on('disconnect', () => {
    console.log('A user disconnected');
  });
});

// Start the server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});