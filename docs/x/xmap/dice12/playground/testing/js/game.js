/**
 * Main Game Logic for D12 Random Chess
 * Human vs Engine implementation
 */

class RandomChessD12 {
  constructor() {
    this.game = new Chess();
    this.board = null;
    this.dice = null;
    this.currentPlayer = 'w'; // 'w' or 'b'
    this.isHumanTurn = true;
    this.pendingMoves = [];   // Moves from dice roll
    this.executedMoves = [];  // Moves made this turn
    this.gameOver = false;
    this.aiDepth = 2;
    
    // Piece symbols mapping
    this.pieceSymbols = {
      'p': '♙', 'n': '♘', 'b': '♗', 'r': '♖', 'q': '♕', 'k': '♔',
      'P': '♟', 'N': '♞', 'B': '♝', 'R': '♜', 'Q': '♛', 'K': '♚'
    };
  }

  /**
   * Initialize the game
   */
  init() {
    this._setupBoard();
    this._setupDice();
    this._setupEventListeners();
    this._updateStatus('Бросьте кубики для начала хода');
  }

  /**
   * Setup chessboard with chessboard.js
   */
  _setupBoard() {
    const config = {
      position: 'start',
      pieceTheme: 'img/chesspieces/wikipedia/{piece}.png',
      onDragStart: this._onDragStart.bind(this),
      onDrop: this._onDrop.bind(this),
      onSnapEnd: this._onSnapEnd.bind(this)
    };
    
    this.board = Chessboard('chessboard', config);
  }

  /**
   * Setup dice roller
   */
  _setupDice() {
    this.dice = new D12Dice('dice-container');
  }

  /**
   * Setup UI event listeners
   */
  _setupEventListeners() {
    document.getElementById('roll-btn').addEventListener('click', () => {
      if (this.isHumanTurn && !this.gameOver) {
        this._handleRollDice();
      }
    });
    
    document.getElementById('new-game-btn').addEventListener('click', () => {
      this._newGame();
    });
    
    document.getElementById('flip-btn').addEventListener('click', () => {
      this.board.flip();
    });
    
    document.getElementById('ai-difficulty').addEventListener('change', (e) => {
      this.aiDepth = parseInt(e.target.value);
    });
  }

  /**
   * Handle dice roll action
   */
  async _handleRollDice() {
    if (this.pendingMoves.length > 0) {
      this._updateStatus('Сначала выполните доступные ходы');
      return;
    }

    const results = await this.dice.roll();
    const moves = this.dice.getMovesForPlayer(this.currentPlayer);
    
    this.pendingMoves = this._getValidMovesFromDice(moves);
    
    if (this.pendingMoves.mandatory.length === 0 && 
        this.pendingMoves.optional.length === 0) {
      this._updateStatus('Нет доступных ходов — ход переходит противнику');
      setTimeout(() => this._endTurn(), 1500);
      return;
    }
    
    this._displayAvailableMoves();
    this._updateStatus(`Выберите ход: ${this.pendingMoves.mandatory.length} обязательных, ${this.pendingMoves.optional.length} опциональных`);
  }

  /**
   * Get valid moves based on dice results
   */
  _getValidMovesFromDice(moves) {
    const result = { mandatory: [], optional: [] };
    const allMoves = this.game.moves({ verbose: true });
    
    // Process mandatory moves (own pieces)
    moves.mandatory.forEach(pieceType => {
      const pieceColor = this.currentPlayer === 'w' ? 'w' : 'b';
      const validMoves = allMoves.filter(m => 
        m.piece === pieceType && m.color === pieceColor
      );
      if (validMoves.length > 0) {
        result.mandatory.push({ type: pieceType, moves: validMoves });
      }
    });
    
    // Process optional moves (opponent pieces)
    moves.optional.forEach(pieceType => {
      const pieceColor = this.currentPlayer === 'w' ? 'b' : 'w';
      const validMoves = allMoves.filter(m => 
        m.piece === pieceType && m.color === pieceColor
      );
      if (validMoves.length > 0) {
        result.optional.push({ type: pieceType, moves: validMoves });
      }
    });
    
    return result;
  }

  /**
   * Display available moves in UI
   */
  _displayAvailableMoves() {
    const container = document.getElementById('available-moves');
    container.innerHTML = '';
    
    // Mandatory moves
    this.pendingMoves.mandatory.forEach(item => {
      const chip = document.createElement('div');
      chip.className = 'move-chip mandatory';
      chip.innerHTML = `<span>⚠️ ${this.pieceSymbols[item.type.toUpperCase()] || item.type}</span>`;
      chip.title = `Обязательный ход фигурой ${item.type}`;
      chip.dataset.type = item.type;
      chip.dataset.mandatory = 'true';
      container.appendChild(chip);
    });
    
    // Optional moves
    this.pendingMoves.optional.forEach(item => {
      const chip = document.createElement('div');
      chip.className = 'move-chip optional';
      chip.innerHTML = `<span>💡 ${this.pieceSymbols[item.type.toLowerCase()] || item.type}</span>`;
      chip.title = `Опциональный ход фигурой противника ${item.type}`;
      chip.dataset.type = item.type;
      chip.dataset.mandatory = 'false';
      container.appendChild(chip);
    });
    
    // Add click handlers
    container.querySelectorAll('.move-chip').forEach(chip => {
      chip.addEventListener('click', (e) => {
        const type = e.currentTarget.dataset.type;
        const isMandatory = e.currentTarget.dataset.mandatory === 'true';
        this._highlightMovesForPiece(type, isMandatory);
      });
    });
  }

  /**
   * Highlight valid squares for selected piece type
   */
  _highlightMovesForPiece(pieceType, isMandatory) {
    const allMoves = this.game.moves({ verbose: true });
    const pieceColor = isMandatory ? this.currentPlayer : (this.currentPlayer === 'w' ? 'b' : 'w');
    
    const validMoves = allMoves.filter(m => 
      m.piece === pieceType && m.color === pieceColor
    );
    
    // Highlight squares
    validMoves.forEach(move => {
      const squareEl = document.querySelector(`.square-${move.to}`);
      if (squareEl) {
        squareEl.classList.add('highlight2-5bc79');
        squareEl.dataset.move = JSON.stringify(move);
        squareEl.onclick = (e) => this._handleSquareClick(move, e);
      }
    });
    
    // Store for cleanup
    this._highlightedSquares = validMoves.map(m => m.to);
  }

  /**
   * Handle click on highlighted square
   */
  _handleSquareClick(move, event) {
    event.stopPropagation();
    
    // Make the move
    const result = this.game.move(move);
    if (result) {
      this.board.position(this.game.fen());
      this.executedMoves.push(move);
      this._removeHighlights();
      this._updateHistory();
      this._checkGameEnd();
      
      if (!this.gameOver) {
        // Check if more moves needed this turn (max 3 per dice roll)
        if (this.executedMoves.length < 3 && this.pendingMoves.mandatory.length > 0) {
          this._displayAvailableMoves();
          this._updateStatus(`Ход выполнен. Осталось ходов: ${3 - this.executedMoves.length}`);
        } else {
          this._endTurn();
        }
      }
    }
  }

  /**
   * Remove square highlights
   */
  _removeHighlights() {
    if (this._highlightedSquares) {
      this._highlightedSquares.forEach(square => {
        const el = document.querySelector(`.square-${square}`);
        if (el) {
          el.classList.remove('highlight2-5bc79');
          el.onclick = null;
          delete el.dataset.move;
        }
      });
    }
  }

  /**
   * End current player's turn
   */
  _endTurn() {
    this._removeHighlights();
    this.pendingMoves = [];
    this.executedMoves = [];
    this.dice.reset();
    
    // Switch player
    this.currentPlayer = this.currentPlayer === 'w' ? 'b' : 'w';
    this.isHumanTurn = this.currentPlayer === 'w'; // Human plays white
    
    this._updateStatus(this.isHumanTurn ? 'Ваш ход — бросьте кубики' : 'Ход компьютера...');
    
    if (!this.isHumanTurn && !this.gameOver) {
      setTimeout(() => this._aiMove(), 800);
    }
  }

  /**
   * AI move logic (simplified minimax)
   */
  async _aiMove() {
    if (this.gameOver) return;
    
    // Roll dice for AI
    await this.dice.roll();
    const moves = this.dice.getMovesForPlayer(this.currentPlayer);
    const validMoves = this._getValidMovesFromDice(moves);
    
    // Collect all possible moves
    let allPossibleMoves = [];
    validMoves.mandatory.forEach(item => {
      item.moves.forEach(m => allPossibleMoves.push({ move: m, priority: 2 }));
    });
    validMoves.optional.forEach(item => {
      item.moves.forEach(m => allPossibleMoves.push({ move: m, priority: 1 }));
    });
    
    if (allPossibleMoves.length === 0) {
      this._endTurn();
      return;
    }
    
    // Simple evaluation: prefer captures, then center control
    allPossibleMoves.sort((a, b) => {
      const scoreA = this._evaluateMove(a.move);
      const scoreB = this._evaluateMove(b.move);
      return scoreB - scoreA;
    });
    
    // Make best move
    const bestMove = allPossibleMoves[0].move;
    this.game.move(bestMove);
    this.board.position(this.game.fen());
    this._updateHistory();
    this._checkGameEnd();
    
    if (!this.gameOver) {
      setTimeout(() => this._endTurn(), 600);
    }
  }

  /**
   * Simple move evaluation for AI
   */
  _evaluateMove(move) {
    let score = 0;
    
    // Capture bonus
    if (move.captured) {
      const values = { p: 1, n: 3, b: 3, r: 5, q: 9, k: 100 };
      score += values[move.captured] * 10;
      
      // King capture = instant win
      if (move.captured === 'k') score += 1000;
    }
    
    // Center control bonus
    const centerSquares = ['d4', 'd5', 'e4', 'e5'];
    if (centerSquares.includes(move.to)) score += 2;
    
    // Development bonus for early game
    if (move.piece === 'n' || move.piece === 'b') {
      if (this.game.moveNumber() < 10) score += 1;
    }
    
    return score;
  }

  /**
   * Check for game end conditions
   */
  _checkGameEnd() {
    // Check if king is captured (main win condition)
    const board = this.game.board();
    let whiteKing = false, blackKing = false;
    
    for (let row of board) {
      for (let square of row) {
        if (square && square.type === 'k') {
          if (square.color === 'w') whiteKing = true;
          else blackKing = true;
        }
      }
    }
    
    if (!whiteKing || !blackKing) {
      this._endGame(!whiteKing ? 'black' : 'white');
      return true;
    }
    
    // Fallback: stalemate or insufficient material
    if (this.game.in_draw() || this.game.insufficient_material()) {
      this._endGame('draw');
      return true;
    }
    
    return false;
  }

  /**
   * End game and show result
   */
  _endGame(winner) {
    this.gameOver = true;
    
    const modal = document.getElementById('game-over-modal');
    const resultEl = document.getElementById('game-result');
    const messageEl = document.getElementById('game-message');
    
    if (winner === 'draw') {
      resultEl.textContent = '🤝 Ничья';
      messageEl.textContent = 'Партия завершилась вничью';
    } else {
      resultEl.textContent = winner === 'white' ? '🏆 Победа!' : '💀 Поражение';
      resultEl.style.color = winner === 'white' ? 'var(--success)' : 'var(--accent)';
      messageEl.textContent = winner === 'white' 
        ? 'Вы взяли короля противника!' 
        : 'Ваш король взят компьютером';
    }
    
    modal.classList.remove('hidden');
  }

  /**
   * Update status message
   */
  _updateStatus(message) {
    document.getElementById('status-message').textContent = message;
  }

  /**
   * Update move history display
   */
  _updateHistory() {
    const history = this.game.history({ verbose: true });
    const container = document.getElementById('move-history');
    container.innerHTML = '';
    
    history.forEach((move, index) => {
      const entry = document.createElement('div');
      entry.className = `move-entry ${move.color}-move`;
      const moveNum = Math.floor(index / 2) + 1;
      const notation = move.san;
      entry.textContent = `${moveNum}. ${notation}`;
      container.appendChild(entry);
    });
    
    // Auto-scroll to bottom
    container.scrollTop = container.scrollHeight;
  }

  /**
   * Start new game
   */
  _newGame() {
    this.game.reset();
    this.board.start();
    this.currentPlayer = 'w';
    this.isHumanTurn = true;
    this.gameOver = false;
    this.pendingMoves = [];
    this.executedMoves = [];
    
    document.getElementById('game-over-modal').classList.add('hidden');
    this.dice.reset();
    this._updateStatus('Новая игра — бросьте кубики');
    document.getElementById('available-moves').innerHTML = 
      '<p class="hint">После броска здесь появятся фигуры для хода</p>';
  }

  // ===== Chessboard.js callbacks =====
  
  _onDragStart(source, piece, position, orientation) {
    if (this.gameOver || !this.isHumanTurn) return false;
    if (this.pendingMoves.mandatory.length === 0) return false;
    
    // Only allow dragging pieces that match dice results
    const pieceType = piece[1].toLowerCase();
    const isOwnPiece = piece[0] === this.currentPlayer;
    
    const canMove = isOwnPiece 
      ? this.pendingMoves.mandatory.some(m => m.type === pieceType)
      : this.pendingMoves.optional.some(m => m.type === pieceType);
    
    return canMove;
  }

  _onDrop(source, target) {
    // Try move
    const move = this.game.move({
      from: source,
      to: target,
      promotion: 'q' // Always promote to queen for simplicity
    });
    
    // Illegal move
    if (move === null) return 'snapback';
    
    this._updateHistory();
    this._checkGameEnd();
    
    if (!this.gameOver) {
      this._endTurn();
    }
  }

  _onSnapEnd() {
    this.board.position(this.game.fen());
  }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.game = new RandomChessD12();
  window.game.init();
});

document.addEventListener('DOMContentLoaded', () => {
  window.game = new RandomChessD12();
  window.game.init();
  
  // Инициализация UI
  window.ui = new UIManager(window.game);
  window.ui.loadPreferences();
  window.ui.init();
  
  // Сохранение настроек при изменении
  document.getElementById('show-hints').addEventListener('change', (e) => {
    window.ui.showHints = e.target.checked;
    window.ui.savePreferences();
  });
  
  document.getElementById('ai-difficulty').addEventListener('change', (e) => {
    window.game.aiDepth = parseInt(e.target.value);
    window.ui.savePreferences();
  });
});