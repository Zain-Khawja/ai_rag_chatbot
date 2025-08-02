(function() {
  // Wait for config to be loaded
  function waitForConfig(cb) {
    if (window.AI_CHATBOT_CONFIG) return cb(window.AI_CHATBOT_CONFIG);
    setTimeout(() => waitForConfig(cb), 50);
  }

  waitForConfig(function(config) {
    // Inject full CSS from index.html, replacing selectors for widget
    var style = document.createElement('style');
    style.innerHTML = `
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
      :root {
        --primary-color: ${config.primaryColor};
        --primary-hover: ${config.primaryHover};
        --bg-color: ${config.bgColor};
        --text-color: ${config.textColor};
        --text-light: ${config.textLight};
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --border-radius: 12px;
        --transition: all 0.3s ease;
      }
      #ai-chat-widget {
        position: fixed;
        ${config.position === 'bottom-right' ? 'bottom: 24px; right: 24px;' : ''}
        ${config.position === 'bottom-left' ? 'bottom: 24px; left: 24px;' : ''}
        z-index: 9999;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        color: var(--text-color);
      }
      #ai-chat-button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 24px;
        cursor: pointer;
        box-shadow: var(--shadow-lg);
        transition: var(--transition);
        display: flex;
        align-items: center;
        justify-content: center;
        outline: none;
      }
      #ai-chat-button:hover {
        background-color: var(--primary-hover);
        transform: translateY(-2px);
      }
      #ai-chat-window {
        display: none;
        flex-direction: column;
        width: ${config.width}px;
        height: ${config.height}px;
        position: fixed;
        ${config.position === 'bottom-right' ? 'bottom: 90px; right: 24px;' : ''}
        ${config.position === 'bottom-left' ? 'bottom: 90px; left: 24px;' : ''}
        background: var(--bg-color);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        overflow: hidden;
        z-index: 10000;
        transition: var(--transition);
        animation: slideUp 0.3s ease;
      }
      @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
      }
      #ai-chat-header {
        background-color: var(--primary-color);
        color: white;
        padding: 16px 20px;
        font-weight: 600;
        font-size: 16px;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-top-left-radius: var(--border-radius);
        border-top-right-radius: var(--border-radius);
      }
      .header-title { flex: 1; }
      .close-button {
        background: transparent;
        border: none;
        color: white;
        cursor: pointer;
        font-size: 18px;
        padding: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        opacity: 0.8;
        transition: var(--transition);
      }
      .close-button:hover { opacity: 1; }
      #ai-chat-messages {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
        font-size: 14px;
        display: flex;
        flex-direction: column;
        gap: 16px;
        background-color: #F9FAFB;
      }
      .message {
        padding: 12px 16px;
        border-radius: 12px;
        max-width: 85%;
        word-wrap: break-word;
        line-height: 1.5;
        position: relative;
        animation: fadeIn 0.3s ease;
      }
      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }
      .message p { margin: 0 0 8px 0; }
      .message p:last-child { margin-bottom: 0; }
      .message pre {
        background: #F3F4F6;
        padding: 8px;
        border-radius: 6px;
        overflow-x: auto;
        font-size: 12px;
      }
      .message code {
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
        background: #F3F4F6;
        padding: 2px 4px;
        border-radius: 4px;
        font-size: 13px;
      }
      .user-message {
        background: var(--primary-color);
        color: white;
        align-self: flex-end;
        box-shadow: var(--shadow-sm);
        border-bottom-right-radius: 4px;
      }
      .bot-message {
        background: white;
        color: var(--text-color);
        align-self: flex-start;
        box-shadow: var(--shadow-sm);
        border-bottom-left-radius: 4px;
        border: 1px solid #E5E7EB;
      }
      .message-time {
        font-size: 10px;
        color: var(--text-light);
        margin-top: 4px;
        text-align: right;
        opacity: 0.8;
      }
      .user-message .message-time { color: white; }
      #ai-chat-input {
        display: flex;
        padding: 16px;
        border-top: 1px solid #E5E7EB;
        background-color: white;
        position: relative;
      }
      #ai-chat-input input {
        flex: 1;
        padding: 12px 16px;
        border: 1px solid #E5E7EB;
        border-radius: 24px;
        font-size: 14px;
        outline: none;
        transition: var(--transition);
        font-family: 'Inter', sans-serif;
      }
      #ai-chat-input input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1);
      }
      #ai-chat-input button {
        margin-left: 12px;
        padding: 0;
        width: 42px;
        height: 42px;
        border: none;
        background: var(--primary-color);
        color: white;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: var(--transition);
      }
      #ai-chat-input button:hover {
        background: var(--primary-hover);
        transform: translateY(-1px);
      }
      #ai-chat-input button:disabled {
        background: #A5B4FC;
        cursor: not-allowed;
        transform: none;
      }
      .loading {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        max-width: 60%;
        align-self: flex-start;
        background: white;
        border-radius: 12px;
        border-bottom-left-radius: 4px;
        box-shadow: var(--shadow-sm);
        border: 1px solid #E5E7EB;
        animation: pulse 1.5s infinite;
      }
      @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
      }
      .typing-dots {
        display: flex;
        align-items: center;
      }
      .dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #A5B4FC;
        margin: 0 2px;
        animation: bounce 1.4s infinite ease-in-out both;
      }
      .dot:nth-child(1) { animation-delay: -0.32s; }
      .dot:nth-child(2) { animation-delay: -0.16s; }
      @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
      }
      .welcome-message {
        font-size: 14px;
        text-align: center;
        padding: 16px;
        color: var(--text-light);
        background-color: white;
        border-radius: var(--border-radius);
        margin: 12px 0;
        border: 1px solid #E5E7EB;
      }
      .welcome-title {
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 8px;
        color: var(--text-color);
      }
      @media (max-width: 640px) {
        #ai-chat-window {
          width: calc(100% - 48px);
          height: 70vh;
          bottom: 80px;
          right: 24px;
          left: 24px;
        }
      }
      .ai-product-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
      }
      .ai-product-card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        transform: translateY(-2px);
        border-color: var(--primary-color);
      }
      .ai-product-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-color), #8B5CF6);
        opacity: 0;
        transition: opacity 0.3s ease;
      }
      .ai-product-card:hover::before {
        opacity: 1;
      }
      
      .product-header {
        margin-bottom: 12px;
      }
      
      .product-title {
        margin: 0 0 6px 0;
        font-size: 18px;
        font-weight: 600;
        line-height: 1.3;
      }
      
      .product-title a {
        color: var(--text-color);
        text-decoration: none;
        transition: color 0.2s ease;
      }
      
      .product-title a:hover {
        color: var(--primary-color);
      }
      
      .product-category {
        display: inline-block;
        background: #F3F4F6;
        color: #6B7280;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }
      
      .product-content {
        margin-bottom: 16px;
      }
      
      .product-description {
        margin: 0 0 12px 0;
        font-size: 14px;
        line-height: 1.6;
        color: #4B5563;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
        max-height: calc(1.6em * 4);
      }
      
      /* Fallback for browsers that don't support -webkit-line-clamp */
      @supports not (-webkit-line-clamp: 4) {
        .product-description {
          position: relative;
          max-height: calc(1.6em * 4);
          overflow: hidden;
        }
        
        .product-description::after {
          content: '...';
          position: absolute;
          bottom: 0;
          right: 0;
          background: white;
          padding-left: 4px;
          font-weight: bold;
        }
      }
      
      .product-specs {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 8px;
        margin-bottom: 16px;
      }
      
      .spec-item {
        display: flex;
        align-items: center;
        font-size: 12px;
        color: #6B7280;
        background: #F9FAFB;
        padding: 6px 10px;
        border-radius: 6px;
        border: 1px solid #E5E7EB;
      }
      
      .spec-item strong {
        color: #374151;
        margin-right: 4px;
        font-weight: 600;
      }
      
      .product-actions {
        display: flex;
        justify-content: flex-end;
      }
      
      .view-product-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        background: var(--primary-color);
        color: white;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 500;
        text-decoration: none;
        transition: all 0.2s ease;
        border: none;
        cursor: pointer;
      }
      
      .view-product-btn:hover {
        background: var(--primary-hover);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
      }
      
      .view-product-btn::after {
        content: '→';
        font-size: 14px;
        transition: transform 0.2s ease;
      }
      
      .view-product-btn:hover::after {
        transform: translateX(2px);
      }
      
      /* Stock status indicators */
      .spec-item.stock-instock {
        background: #F0FDF4;
        border-color: #BBF7D0;
        color: #166534;
      }
      
      .spec-item.stock-outofstock {
        background: #FEF2F2;
        border-color: #FECACA;
        color: #DC2626;
      }
      
      /* Responsive design */
      @media (max-width: 480px) {
        .ai-product-card {
          padding: 16px;
          margin-bottom: 12px;
        }
        
        .product-title {
          font-size: 16px;
        }
        
        .product-specs {
          grid-template-columns: 1fr;
          gap: 6px;
        }
        
        .spec-item {
          font-size: 11px;
          padding: 4px 8px;
        }
        
        .view-product-btn {
          padding: 6px 12px;
          font-size: 12px;
        }
      }
      
      /* Animation for new cards */
      .ai-product-card {
        animation: slideInUp 0.4s ease-out;
      }
      
      @keyframes slideInUp {
        from {
          opacity: 0;
          transform: translateY(20px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
      
      /* Loading state for cards */
      .ai-product-card.loading {
        opacity: 0.7;
        pointer-events: none;
      }
      
      /* Featured product styling */
      .ai-product-card.featured {
        border-color: #F59E0B;
        background: linear-gradient(135deg, #FFFBEB 0%, #FFFFFF 100%);
      }
      
      .ai-product-card.featured::before {
        background: linear-gradient(90deg, #F59E0B, #F97316);
      }
      
      /* Compact card variant */
      .ai-product-card.compact {
        padding: 12px;
      }
      
      .ai-product-card.compact .product-title {
        font-size: 14px;
        margin-bottom: 4px;
      }
      
      .ai-product-card.compact .product-description {
        font-size: 12px;
        margin-bottom: 8px;
      }
      
      .ai-product-card.compact .product-specs {
        margin-bottom: 8px;
      }
      
      .ai-product-card.compact .spec-item {
        font-size: 10px;
        padding: 3px 6px;
      }
      
      /* Optional: Product image styling */
      .product-image {
        width: 100%;
        height: 120px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 12px;
        background: #F3F4F6;
      }
      
      /* Optional: Price styling */
      .product-price {
        display: inline-block;
        background: #10B981;
        color: white;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 8px;
      }
      
      /* Optional: Rating styling */
      .product-rating {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 12px;
        color: #6B7280;
        margin-bottom: 8px;
      }
      
      /* Optional: Badge styling */
      .product-badge {
        display: inline-block;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 8px;
      }
      
      .product-badge.featured {
        background: #FEF3C7;
        color: #92400E;
      }
      
      .product-badge.new {
        background: #DBEAFE;
        color: #1E40AF;
      }
      
      .product-badge.sale {
        background: #FEE2E2;
        color: #DC2626;
      }
      
      /* Optional: Quick action buttons */
      .product-quick-actions {
        display: flex;
        gap: 8px;
        margin-top: 12px;
      }
      
      .quick-action-btn {
        flex: 1;
        padding: 6px 12px;
        border: 1px solid #E5E7EB;
        background: white;
        color: #6B7280;
        border-radius: 6px;
        font-size: 12px;
        text-decoration: none;
        text-align: center;
        transition: all 0.2s ease;
      }
      
      .quick-action-btn:hover {
        background: #F9FAFB;
        border-color: var(--primary-color);
        color: var(--primary-color);
      }
      
      /* Optional: Product comparison */
      .product-compare {
        position: absolute;
        top: 12px;
        right: 12px;
        width: 20px;
        height: 20px;
        border: 1px solid #E5E7EB;
        border-radius: 4px;
        background: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        transition: all 0.2s ease;
      }
      
      .product-compare:hover {
        border-color: var(--primary-color);
        color: var(--primary-color);
      }
      
      .product-compare.checked {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
      }

    `;
    document.head.appendChild(style);

    // Create widget container
    var widget = document.createElement('div');
    widget.id = 'ai-chat-widget';
    widget.innerHTML = `
      <button id="ai-chat-button">
        <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'></path></svg>
      </button>
      <div id="ai-chat-window">
        <div id="ai-chat-header" style="background: var(--primary-color); color: white; padding: 16px 20px; font-weight: 600; font-size: 16px; text-align: center; display: flex; align-items: center; justify-content: space-between; border-top-left-radius: var(--border-radius); border-top-right-radius: var(--border-radius);">
          <div class="header-title" style="flex:1;">${config.title}</div>
          <button class="close-button" id="ai-close-chat" style="background:transparent; border:none; color:white; cursor:pointer; font-size:18px; width:24px; height:24px; opacity:0.8;">×</button>
        </div>
        <div id="ai-chat-messages" style="flex:1; padding:20px; overflow-y:auto; font-size:14px; display:flex; flex-direction:column; gap:16px; background-color:#F9FAFB;">
          <div class="welcome-message" style="font-size:14px; text-align:center; padding:16px; color:var(--text-light); background-color:white; border-radius:var(--border-radius); margin:12px 0; border:1px solid #E5E7EB;">
            <div class="welcome-title" style="font-weight:600; font-size:16px; margin-bottom:8px; color:var(--text-color);">${config.welcomeTitle}</div>
            <p>${config.welcomeMessage}</p>
          </div>
        </div>
        <div id="ai-chat-input" style="display:flex; padding:16px; border-top:1px solid #E5E7EB; background-color:white; position:relative;">
          <input id="ai-chatText" type="text" placeholder="Type your message..." style="flex:1; padding:12px 16px; border:1px solid #E5E7EB; border-radius:24px; font-size:14px; outline:none; font-family:'Inter',sans-serif;" />
          <button id="ai-send-button" style="margin-left:12px; width:42px; height:42px; border:none; background:var(--primary-color); color:white; border-radius:50%; cursor:pointer; display:flex; align-items:center; justify-content:center;">
            <svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><line x1='22' y1='2' x2='11' y2='13'></line><polygon points='22 2 15 22 11 13 2 9 22 2'></polygon></svg>
          </button>
        </div>
      </div>
    `;
    document.body.appendChild(widget);

    // Load marked and DOMPurify if not present
    function loadScript(src, cb) {
      if (document.querySelector('script[src="'+src+'"]')) return cb();
      var s = document.createElement('script');
      s.src = src;
      s.onload = cb;
      document.head.appendChild(s);
    }
    loadScript('https://cdn.jsdelivr.net/npm/marked/marked.min.js', function() {
      loadScript('https://cdn.jsdelivr.net/npm/dompurify@3.0.5/dist/purify.min.js', function() {
        // Widget logic
        var button = document.getElementById('ai-chat-button');
        var windowEl = document.getElementById('ai-chat-window');
        var messages = document.getElementById('ai-chat-messages');
        var chatInput = document.getElementById('ai-chatText');
        var sendButton = document.getElementById('ai-send-button');
        var closeButton = document.getElementById('ai-close-chat');

        button.onclick = function() {
          windowEl.style.display = windowEl.style.display === 'none' ? 'flex' : 'none';
          if (windowEl.style.display === 'flex') chatInput.focus();
        };
        closeButton.onclick = function() {
          windowEl.style.display = 'none';
        };
        chatInput.addEventListener('keypress', function(e) {
          if (e.key === 'Enter') sendChat();
        });
        sendButton.addEventListener('click', sendChat);

        function getTimeString() {
          var now = new Date();
          return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }
        function appendMessage(text, isUser) {
          var msg = document.createElement('div');
          msg.className = 'message ' + (isUser ? 'user-message' : 'bot-message');
          var timeEl = document.createElement('div');
          timeEl.className = 'message-time';
          timeEl.textContent = getTimeString();
          
          if (!isUser) {
            var sanitizedHTML = DOMPurify.sanitize(marked.parse(text));
            msg.innerHTML = sanitizedHTML;
            
            // Enhanced product card handling
            setTimeout(() => {
              // Add stock status classes
              msg.querySelectorAll('.spec-item').forEach(spec => {
                if (spec.textContent.includes('Stock: instock')) {
                  spec.classList.add('stock-instock');
                } else if (spec.textContent.includes('Stock: outofstock')) {
                  spec.classList.add('stock-outofstock');
                }
              });
              
              // Add click tracking for product links
              msg.querySelectorAll('.ai-product-card a').forEach(link => {
                link.setAttribute('target', '_blank');
                link.addEventListener('click', function(e) {
                  console.log('🔗 Product link clicked:', this.href);
                  // You can add analytics tracking here
                });
              });
              
              // Add hover effects for product cards
              msg.querySelectorAll('.ai-product-card').forEach(card => {
                card.addEventListener('mouseenter', function() {
                  this.style.transform = 'translateY(-2px)';
                });
                
                card.addEventListener('mouseleave', function() {
                  this.style.transform = 'translateY(0)';
                });
              });
              
              // Add staggered animation for multiple cards
              const cards = msg.querySelectorAll('.ai-product-card');
              cards.forEach((card, index) => {
                card.style.animationDelay = (index * 0.1) + 's';
              });
              
            }, 100);
            
          } else {
            msg.textContent = text;
          }
          
          msg.appendChild(timeEl);
          messages.appendChild(msg);
          messages.scrollTop = messages.scrollHeight;
        }
        function showLoadingIndicator() {
          var loading = document.createElement('div');
          loading.className = 'loading';
          loading.id = 'ai-loading-indicator';
          var dots = document.createElement('div');
          dots.className = 'typing-dots';
          for (var i = 0; i < 3; i++) {
            var dot = document.createElement('div');
            dot.className = 'dot';
            dots.appendChild(dot);
          }
          loading.appendChild(dots);
          messages.appendChild(loading);
          messages.scrollTop = messages.scrollHeight;
        }
        function removeLoadingIndicator() {
          var loadingIndicator = document.getElementById('ai-loading-indicator');
          if (loadingIndicator) loadingIndicator.remove();
        }
        async function sendChat() {
          var input = document.getElementById('ai-chatText');
          var query = input.value.trim();
          if (!query) return;
          input.value = '';
          input.disabled = true;
          sendButton.disabled = true;
          appendMessage(query, true);
          showLoadingIndicator();
          try {
            var res = await fetch(config.apiUrl, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ query })
            });
            removeLoadingIndicator();
            if (!res.ok) throw new Error('Server responded with status: ' + res.status);
            var data = await res.json();
            console.log(data);
            appendMessage(data.response, false);
          } catch (err) {
            removeLoadingIndicator();
            appendMessage('❌ Error getting response. Please try again later.', false);
          } finally {
            input.disabled = false;
            sendButton.disabled = false;
            input.focus();
          }
        }
      });
    });
  });
})();
