/**
 * Secure Chat Module
 * Handles the client-side socket.io connections and messaging for both doctor and patient interfaces
 */

class SecureChat {
  constructor(options) {
      this.socket = io();
      this.userType = options.userType || 'unknown';
      this.userName = options.userName || 'Unknown User';
      this.userId = options.userId || '0';
      this.roomCode = options.roomCode || null;
      this.doctorId = options.doctorId || null;
      this.patientId = options.patientId || null;
      this.messageContainer = options.messageContainer || document.getElementById('messageContainer');
      this.messageForm = options.messageForm || document.getElementById('messageForm');
      this.messageInput = options.messageInput || document.getElementById('messageInput');
      this.onNewMessage = options.onNewMessage || null;
      this.onSystemMessage = options.onSystemMessage || null;
      this.onPatientConnected = options.onPatientConnected || null;
      
      this.setupSocketListeners();
      this.setupFormSubmit();
  }
  
  /**
   * Set up all socket.io event listeners
   */
  setupSocketListeners() {
      // Handle received messages
      this.socket.on('message', (data) => {
          this.handleIncomingMessage(data);
      });
      
      // Handle system messages
      this.socket.on('system', (data) => {
          this.handleSystemMessage(data);
      });
      
      // Special event for doctor interface - new patient connection
      if (this.userType === 'doctor') {
          this.socket.on('patient_connected', (data) => {
              if (typeof this.onPatientConnected === 'function') {
                  this.onPatientConnected(data);
              } else {
                  console.log('New patient connected:', data);
              }
          });
      }
      
      // Handle connection established
      this.socket.on('connect', () => {
          console.log('Connected to socket.io server');
          
          // If we have a room code, join it automatically
          if (this.roomCode) {
              this.joinRoom(this.roomCode);
          }
      });
      
      // Handle disconnection
      this.socket.on('disconnect', () => {
          console.log('Disconnected from socket.io server');
          this.addSystemMessage('Disconnected from server. Trying to reconnect...');
      });
  }
  
  /**
   * Set up message form submission
   */
  setupFormSubmit() {
      if (this.messageForm) {
          this.messageForm.addEventListener('submit', (e) => {
              e.preventDefault();
              this.sendMessage();
          });
      }
  }
  
  /**
   * Join a specific chat room
   * @param {string} roomCode - The room code to join
   * @param {Object} extraData - Any extra data to send with the join event
   */
  joinRoom(roomCode, extraData = {}) {
      this.roomCode = roomCode;
      
      const joinData = {
          room: roomCode,
          name: this.userName,
          userType: this.userType,
          ...extraData
      };
      
      this.socket.emit('join', joinData);
      console.log(`Joined room: ${roomCode}`);
      
      return this;
  }
  
  /**
   * Leave the current chat room
   */
  leaveRoom() {
      if (this.roomCode) {
          this.socket.emit('leave', { room: this.roomCode });
          console.log(`Left room: ${this.roomCode}`);
          this.roomCode = null;
      }
      
      return this;
  }
  
  /**
   * Send a message to the current room
   * @param {string} customText - Optional custom text (if not using the input field)
   */
  sendMessage(customText = null) {
      const text = customText || (this.messageInput ? this.messageInput.value.trim() : '');
      
      if (text !== '' && this.roomCode) {
          this.socket.emit('message', {
              room: this.roomCode,
              data: text,
              userType: this.userType,
              name: this.userName
          });
          
          // Clear input field if we're using one
          if (!customText && this.messageInput) {
              this.messageInput.value = '';
          }
          
          // Scroll down
          this.scrollToBottom();
      }
      
      return this;
  }
  
  /**
   * End the current chat session
   */
  endSession() {
      if (this.roomCode) {
          this.socket.emit('end_session', { room: this.roomCode });
          this.leaveRoom();
      }
      
      return this;
  }
  
  /**
   * Handle an incoming message
   * @param {Object} data - Message data from socket.io
   */
  handleIncomingMessage(data) {
      // Check if the message is for our current room
      if (data.room && data.room !== this.roomCode) {
          // Message is for a different room
          if (typeof this.onNewMessage === 'function') {
              this.onNewMessage(data);
          }
          return;
      }
      
      const sender = data.userType === this.userType ? this.userType : (data.userType === 'doctor' ? 'doctor' : 'patient');
      const senderName = data.userType === this.userType 
          ? 'You' 
          : (data.userType === 'doctor' ? `Dr. ${data.name}` : data.name);
      
      this.addMessage(data.message || data.data, sender, senderName);
      this.scrollToBottom();
      
      // Call callback if provided
      if (typeof this.onNewMessage === 'function') {
          this.onNewMessage(data);
      }
  }
  
  /**
   * Handle system messages
   * @param {Object} data - System message data from socket.io
   */
  handleSystemMessage(data) {
      // Check if the message is for our current room
      if (data.room && data.room !== this.roomCode) {
          // Message is for a different room
          if (typeof this.onSystemMessage === 'function') {
              this.onSystemMessage(data);
          }
          return;
      }
      
      this.addSystemMessage(data.message);
      this.scrollToBottom();
      
      // Call callback if provided
      if (typeof this.onSystemMessage === 'function') {
          this.onSystemMessage(data);
      }
  }
  
  /**
   * Add a message to the message container
   * @param {string} text - Message text
   * @param {string} sender - Sender type ('doctor', 'patient')
   * @param {string} name - Sender name
   */
  addMessage(text, sender, name) {
      if (!this.messageContainer) return;
      
      const now = new Date();
      const time = now.getHours() + ':' + String(now.getMinutes()).padStart(2, '0');
      
      const div = document.createElement('div');
      div.className = `message-item ${sender} mb-3`;
      div.innerHTML = `
          <div class="message-content">
              <div class="message-header">
                  <strong>${name}</strong>
                  <small class="text-muted">${time}</small>
              </div>
              <p class="mb-0">${text}</p>
          </div>
      `;
      
      this.messageContainer.appendChild(div);
  }
  
  /**
   * Add a system message to the message container
   * @param {string} text - System message text
   */
  addSystemMessage(text) {
      if (!this.messageContainer) return;
      
      const div = document.createElement('div');
      div.className = 'system-message text-center mb-3';
      div.innerHTML = `<small class="text-muted">--- ${text} ---</small>`;
      
      this.messageContainer.appendChild(div);
  }
  
  /**
   * Scroll the message container to the bottom
   */
  scrollToBottom() {
      if (this.messageContainer) {
          this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
      }
  }
  
  /**
   * Clear all messages from the container
   */
  clearMessages() {
      if (this.messageContainer) {
          this.messageContainer.innerHTML = '';
      }
      
      return this;
  }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
  module.exports = SecureChat;
} else {
  window.SecureChat = SecureChat;
}