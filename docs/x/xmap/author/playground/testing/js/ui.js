/**
 * UI Module for D12 Random Chess
 * Handles all user interface interactions and visual feedback
 */

class UIManager {
  constructor(game) {
    this.game = game;
    this.theme = 'dark';
    this.showHints = true;
    this.animationSpeed = 300;
  }

  /**
   * Initialize UI components
   */
  init() {
    this._setupThemeToggle();
    this._setupMoveSelection();
    this._setupModalHandlers();
    this._setupKeyboardShortcuts();
    this._updateTurnIndicator();
  }

  /**
   * Setup theme toggle (dark/light)
   */
  _setupThemeToggle() {
    const themeBtn = document.createElement('button');
    themeBtn.id = 'theme-toggle';
    themeBtn.className = 'btn-secondary';
    themeBtn.innerHTML = '🌓 Тема';
    themeBtn.style.marginTop = '0.5rem';
    
    const settingsSection = document.querySelector('.settings-section');
    settingsSection.appendChild(themeBtn);
    
    themeBtn.addEventListener('click', () => {
      this.toggleTheme();
    });
  }

  /**
   * Toggle between dark and light themes
   */
  toggleTheme() {
    this.theme = this.theme === 'dark' ? 'light' : 'dark';
    document.body.className = `${this.theme}-theme`;
    
    // Save preference
    localStorage.setItem('d12chess-theme', this.theme);
    
    // Update board colors if needed
    if (this.game.board) {
      this._refreshBoardColors();
    }
  }

  /**
   * Refresh board colors based on theme
   */
  _refreshBoardColors() {
    const colors = this.theme === 'dark' 
      ? { light: '#eeeed2', dark: '#769656' }
      : { light: '#f0d9b5', dark: '#b58863' };
    
    // Update chessboard.js configuration
    if (this.game.board) {
      this.game.board.destroy();
      this.game.board = Chessboard('chessboard', {
        position: this.game.game.fen(),
        pieceTheme: 'img/chesspieces/wikipedia/{piece}.png',
        squareColors: colors,
        onDragStart: this.game._onDragStart.bind(this.game),
        onDrop: this.game._onDrop.bind(this.game),
        onSnapEnd: this.game._onSnapEnd.bind(this.game)
      });
    }
  }

  /**
   * Setup move selection via chips
   */
  _setupMoveSelection() {
    const movesContainer = document.getElementById('available-moves');
    
    // Event delegation for dynamic chips
    movesContainer.addEventListener('click', (e) => {
      const chip = e.target.closest('.move-chip');
      if (!chip) return;
      
      const pieceType = chip.dataset.type;
      const isMandatory = chip.dataset.mandatory === 'true';
      
      this.game._highlightMovesForPiece(pieceType, isMandatory);
      
      // Visual feedback
      document.querySelectorAll('.move-chip').forEach(c => c.classList.remove('selected'));
      chip.classList.add('selected');
    });
  }

  /**
   * Setup modal event handlers
   */
  _setupModalHandlers() {
    const modal = document.getElementById('game-over-modal');
    const playAgainBtn = document.getElementById('play-again-btn');
    
    // Close modal on outside click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.add('hidden');
      }
    });
    
    // Play again button
    playAgainBtn.addEventListener('click', () => {
      modal.classList.add('hidden');
      this.game._newGame();
    });
    
    // Keyboard: Enter to play again
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !modal.classList.contains('hidden')) {
        modal.classList.add('hidden');
        this.game._newGame();
      }
    });
  }

  /**
   * Setup keyboard shortcuts
   */
  _setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Ignore if typing in input
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      
      switch(e.key.toLowerCase()) {
        case 'r':
          // Roll dice
          if (this.game.isHumanTurn && !this.game.gameOver) {
            e.preventDefault();
            document.getElementById('roll-btn').click();
          }
          break;
          
        case 'z':
          // Undo (if implemented)
          if (e.ctrlKey || e.metaKey) {
            e.preventDefault();
            this._handleUndo();
          }
          break;
          
        case 'f':
          // Flip board
          if (e.ctrlKey || e.metaKey) {
            e.preventDefault();
            document.getElementById('flip-btn').click();
          }
          break;
          
        case 'n':
          // New game
          if (e.ctrlKey || e.metaKey) {
            e.preventDefault();
            if (confirm('Начать новую партию?')) {
              this.game._newGame();
            }
          }
          break;
          
        case 'h':
          // Toggle hints
          if (e.ctrlKey || e.metaKey) {
            e.preventDefault();
            this.toggleHints();
          }
          break;
      }
    });
  }

  /**
   * Handle undo action
   */
  _handleUndo() {
    if (!this.game.executedMoves.length) return;
    
    // Undo last move
    this.game.game.undo();
    this.game.executedMoves.pop();
    this.game.board.position(this.game.game.fen());
    this._updateHistory();
    
    // Re-highlight if needed
    if (this.game.pendingMoves.mandatory.length > 0) {
      this._displayAvailableMoves();
    }
    
    this._updateStatus('Ход отменён');
  }

  /**
   * Toggle move hints visibility
   */
  toggleHints() {
    this.showHints = !this.showHints;
    document.getElementById('show-hints').checked = this.showHints;
    
    if (!this.showHints) {
      this.game._removeHighlights();
    }
    
    this._updateStatus(`Подсказки ${this.showHints ? 'включены' : 'выключены'}`);
  }

  /**
   * Update turn indicator in header
   */
  _updateTurnIndicator() {
    const indicator = document.getElementById('turn-indicator');
    const color = this.game.currentPlayer === 'w' ? 'Белые' : 'Чёрные';
    const player = this.game.isHumanTurn ? 'Вы' : 'Компьютер';
    
    indicator.textContent = `Ход: ${player} (${color})`;
    indicator.className = this.game.currentPlayer === 'w' ? 'white-turn' : 'black-turn';
  }

  /**
   * Update status message with animation
   */
  _updateStatus(message, type = 'info') {
    const statusEl = document.getElementById('status-message');
    
    // Animation: fade out/in
    statusEl.style.opacity = '0';
    
    setTimeout(() => {
      statusEl.textContent = message;
      statusEl.className = `status-${type}`;
      statusEl.style.opacity = '1';
    }, 150);
  }

  /**
   * Display available moves with visual chips
   */
  _displayAvailableMoves() {
    const container = document.getElementById('available-moves');
    container.innerHTML = '';
    
    const { mandatory, optional } = this.game.pendingMoves;
    
    if (mandatory.length === 0 && optional.length === 0) {
      container.innerHTML = '<p class="hint">Нет доступных ходов</p>';
      return;
    }
    
    // Helper to create chip
    const createChip = (item, isMandatory) => {
      const chip = document.createElement('div');
      chip.className = `move-chip ${isMandatory ? 'mandatory' : 'optional'}`;
      
      const symbol = this.game.pieceSymbols[
        isMandatory ? item.type.toUpperCase() : item.type.toLowerCase()
      ] || item.type;
      
      const count = item.moves.length;
      chip.innerHTML = `
        <span class="piece-icon">${symbol}</span>
        <span class="move-count">${count}</span>
      `;
      chip.title = `${isMandatory ? 'Обязательный' : 'Опциональный'} ход: ${count} вариантов`;
      chip.dataset.type = item.type;
      chip.dataset.mandatory = isMandatory;
      
      return chip;
    };
    
    // Add mandatory chips first
    mandatory.forEach(item => {
      container.appendChild(createChip(item, true));
    });
    
    // Add optional chips
    optional.forEach(item => {
      container.appendChild(createChip(item, false));
    });
  }

  /**
   * Update move history panel
   */
  _updateHistory() {
    const history = this.game.game.history({ verbose: true });
    const container = document.getElementById('move-history');
    
    // Group moves by pair (white + black)
    let html = '';
    for (let i = 0; i < history.length; i += 2) {
      const moveNum = Math.floor(i / 2) + 1;
      const whiteMove = history[i];
      const blackMove = history[i + 1];
      
      html += `<div class="move-row">
        <span class="move-number">${moveNum}.</span>
        ${whiteMove ? `<span class="move white">${whiteMove.san}</span>` : ''}
        ${blackMove ? `<span class="move black">${blackMove.san}</span>` : ''}
      </div>`;
    }
    
    container.innerHTML = html || '<p class="hint">История пуста</p>';
    
    // Auto-scroll to latest
    container.scrollTop = container.scrollHeight;
  }

  /**
   * Update captured pieces display
   */
  _updateCapturedPieces() {
    // Get captured pieces from chess.js history
    const history = this.game.game.history({ verbose: true });
    const whiteCaptured = [];
    const blackCaptured = [];
    
    history.forEach(move => {
      if (move.captured) {
        const symbol = this.game.pieceSymbols[move.captured.toUpperCase()];
        if (move.color === 'w') {
          blackCaptured.push(symbol); // White captured black piece
        } else {
          whiteCaptured.push(symbol); // Black captured white piece
        }
      }
    });
    
    // Render
    const renderCaptures = (containerId, pieces) => {
      const container = document.getElementById(containerId);
      container.innerHTML = pieces.length 
        ? pieces.map(p => `<span class="piece-icon">${p}</span>`).join('')
        : '<span class="empty">—</span>';
    };
    
    renderCaptures('white-captured', whiteCaptured);
    renderCaptures('black-captured', blackCaptured);
  }

  /**
   * Animate dice roll result
   */
  animateDiceResult(results) {
    const diceEls = document.querySelectorAll('.die');
    
    results.forEach((result, index) => {
      const die = diceEls[index];
      
      // Quick shuffle animation
      let shuffles = 0;
      const shuffleInterval = setInterval(() => {
        const randomFace = D12_FACES[Math.floor(Math.random() * D12_FACES.length)];
        die.textContent = randomFace.symbol;
        die.className = `die d12 ${randomFace.color}-piece`;
        shuffles++;
        
        if (shuffles >= 8) {
          clearInterval(shuffleInterval);
          // Final result
          die.textContent = result.symbol;
          die.className = `die d12 ${result.color}-piece rolling`;
          
          // Remove rolling class after animation
          setTimeout(() => die.classList.remove('rolling'), 600);
        }
      }, 75);
    });
  }

  /**
   * Highlight king if under attack (visual hint only)
   */
  highlightKingUnderAttack() {
    if (!this.showHints) return;
    
    const board = this.game.game.board();
    const kingPos = this._findKingPosition(board, this.game.currentPlayer);
    
    if (kingPos && this._isSquareAttacked(kingPos, this.game.currentPlayer)) {
      const squareEl = document.querySelector(`.square-${kingPos}`);
      if (squareEl) {
        squareEl.classList.add('highlight-32417');
        squareEl.title = 'Король под угрозой!';
      }
    }
  }

  /**
   * Find king position on board
   */
  _findKingPosition(board, color) {
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const piece = board[row][col];
        if (piece && piece.type === 'k' && piece.color === color) {
          // Convert to algebraic notation
          return String.fromCharCode(97 + col) + (8 - row);
        }
      }
    }
    return null;
  }

  /**
   * Check if square is attacked by opponent
   */
  _isSquareAttacked(square, defenderColor) {
    // Simplified: use chess.js attack detection
    const opponentColor = defenderColor === 'w' ? 'b' : 'w';
    const moves = this.game.game.moves({ square, verbose: true });
    return moves.some(m => m.color === opponentColor);
  }

  /**
   * Show move preview on hover
   */
  showMovePreview(move) {
    if (!this.showHints) return;
    
    // Highlight source and destination
    const sourceEl = document.querySelector(`.square-${move.from}`);
    const targetEl = document.querySelector(`.square-${move.to}`);
    
    if (sourceEl) sourceEl.classList.add('preview-source');
    if (targetEl) {
      targetEl.classList.add('preview-target');
      if (move.captured) targetEl.classList.add('capture-preview');
    }
  }

  /**
   * Clear move preview
   */
  clearMovePreview(move) {
    const sourceEl = document.querySelector(`.square-${move.from}`);
    const targetEl = document.querySelector(`.square-${move.to}`);
    
    if (sourceEl) sourceEl.classList.remove('preview-source');
    if (targetEl) {
      targetEl.classList.remove('preview-target', 'capture-preview');
    }
  }

  /**
   * Pulse animation for important notifications
   */
  pulseNotification(elementId, duration = 1000) {
    const el = document.getElementById(elementId);
    if (!el) return;
    
    el.style.animation = 'pulse 0.3s ease-in-out 3';
    setTimeout(() => {
      el.style.animation = '';
    }, duration);
  }

  /**
   * Load saved preferences
   */
  loadPreferences() {
    // Theme
    const savedTheme = localStorage.getItem('d12chess-theme');
    if (savedTheme && savedTheme !== this.theme) {
      this.theme = savedTheme;
      document.body.className = `${this.theme}-theme`;
    }
    
    // Hints
    const savedHints = localStorage.getItem('d12chess-hints');
    if (savedHints !== null) {
      this.showHints = savedHints === 'true';
      document.getElementById('show-hints').checked = this.showHints;
    }
    
    // AI difficulty
    const savedDifficulty = localStorage.getItem('d12chess-difficulty');
    if (savedDifficulty) {
      document.getElementById('ai-difficulty').value = savedDifficulty;
      this.game.aiDepth = parseInt(savedDifficulty);
    }
  }

  /**
   * Save preferences
   */
  savePreferences() {
    localStorage.setItem('d12chess-theme', this.theme);
    localStorage.setItem('d12chess-hints', this.showHints);
    localStorage.setItem('d12chess-difficulty', this.game.aiDepth);
  }
}

// ===== CSS Animations (add to style.css) =====
/*
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.status-info { color: var(--text-secondary); }
.status-warning { color: var(--warning); }
.status-success { color: var(--success); }
.status-error { color: var(--accent); }

.move-chip.selected {
  background: var(--accent) !important;
  color: white;
  transform: scale(1.1);
}

.preview-source {
  box-shadow: inset 0 0 0 3px var(--warning) !important;
}

.preview-target {
  box-shadow: inset 0 0 0 3px var(--success) !important;
}

.capture-preview {
  box-shadow: inset 0 0 0 3px var(--accent) !important;
}

.move-row {
  display: flex;
  gap: 0.5rem;
  padding: 0.2rem 0;
  border-bottom: 1px dashed var(--bg-secondary);
}

.move-number {
  color: var(--text-secondary);
  min-width: 1.5rem;
}

.move.white { color: #fff; }
.move.black { color: #aaa; }

.white-turn { color: #fff; }
.black-turn { color: #aaa; }
*/

// ===== Initialize UI when game is ready =====
if (typeof module !== 'undefined' && module.exports) {
  module.exports = UIManager;
}