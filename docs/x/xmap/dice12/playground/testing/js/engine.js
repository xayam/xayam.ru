/**
 * Simple Chess Engine for D12 Random Chess
 * Minimax with alpha-beta pruning
 */

class SimpleEngine {
  constructor(depth = 2) {
    this.depth = depth;
    this.pieceValues = { p: 100, n: 320, b: 330, r: 500, q: 900, k: 20000 };
    
    // Position tables for piece-square evaluation
    this.pawnTable = [
      [0,  0,  0,  0,  0,  0,  0,  0],
      [50, 50, 50, 50, 50, 50, 50, 50],
      [10, 10, 20, 30, 30, 20, 10, 10],
      [5,  5, 10, 25, 25, 10,  5,  5],
      [0,  0,  0, 20, 20,  0,  0,  0],
      [5, -5,-10,  0,  0,-10, -5,  5],
      [5, 10, 10,-20,-20, 10, 10,  5],
      [0,  0,  0,  0,  0,  0,  0,  0]
    ];
  }

  /**
   * Get best move using minimax
   */
  getBestMove(game, diceMoves, color) {
    let bestMove = null;
    let bestValue = color === 'w' ? -Infinity : Infinity;
    
    const allMoves = this._getValidMovesFromDice(game, diceMoves, color);
    
    for (let move of allMoves) {
      game.move(move);
      const value = this._minimax(game, this.depth - 1, -Infinity, Infinity, color === 'b');
      game.undo();
      
      if (color === 'w') {
        if (value > bestValue) {
          bestValue = value;
          bestMove = move;
        }
      } else {
        if (value < bestValue) {
          bestValue = value;
          bestMove = move;
        }
      }
    }
    
    return bestMove || allMoves[0];
  }

  /**
   * Minimax with alpha-beta pruning
   */
  _minimax(game, depth, alpha, beta, isMaximizing) {
    if (depth === 0 || this._isGameOver(game)) {
      return this._evaluatePosition(game);
    }
    
    const color = isMaximizing ? 'w' : 'b';
    const moves = game.moves({ verbose: true });
    
    if (isMaximizing) {
      let maxValue = -Infinity;
      for (let move of moves) {
        game.move(move);
        const value = this._minimax(game, depth - 1, alpha, beta, false);
        game.undo();
        maxValue = Math.max(maxValue, value);
        alpha = Math.max(alpha, value);
        if (beta <= alpha) break;
      }
      return maxValue;
    } else {
      let minValue = Infinity;
      for (let move of moves) {
        game.move(move);
        const value = this._minimax(game, depth - 1, alpha, beta, true);
        game.undo();
        minValue = Math.min(minValue, value);
        beta = Math.min(beta, value);
        if (beta <= alpha) break;
      }
      return minValue;
    }
  }

  /**
   * Evaluate board position
   */
  _evaluatePosition(game) {
    let score = 0;
    const board = game.board();
    
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const piece = board[row][col];
        if (piece) {
          const value = this.pieceValues[piece.type] || 0;
          const tableValue = this._getPositionValue(piece, row, col);
          
          if (piece.color === 'w') {
            score += value + tableValue;
          } else {
            score -= value + tableValue;
          }
        }
      }
    }
    
    // King safety bonus (simplified)
    if (!this._kingExists(game, 'w')) score -= 5000;
    if (!this._kingExists(game, 'b')) score += 5000;
    
    return score;
  }

  /**
   * Get position bonus from piece-square table
   */
  _getPositionValue(piece, row, col) {
    if (piece.type === 'p') {
      const tableRow = piece.color === 'w' ? row : 7 - row;
      return this.pawnTable[tableRow][col] * (piece.color === 'w' ? 1 : -1);
    }
    return 0; // Simplified: only pawns have position bonus
  }

  /**
   * Check if king exists on board
   */
  _kingExists(game, color) {
    const board = game.board();
    for (let row of board) {
      for (let square of row) {
        if (square && square.type === 'k' && square.color === color) {
          return true;
        }
      }
    }
    return false;
  }

  /**
   * Check basic game end conditions
   */
  _isGameOver(game) {
    return !this._kingExists(game, 'w') || !this._kingExists(game, 'b');
  }

  /**
   * Filter moves by dice results (simplified version)
   */
  _getValidMovesFromDice(game, diceMoves, color) {
    const allMoves = game.moves({ verbose: true });
    let result = [];
    
    // Add mandatory moves first
    diceMoves.mandatory?.forEach(item => {
      result.push(...allMoves.filter(m => 
        m.piece === item.type && m.color === color
      ));
    });
    
    // Add optional moves
    diceMoves.optional?.forEach(item => {
      result.push(...allMoves.filter(m => 
        m.piece === item.type && m.color !== color
      ));
    });
    
    return result;
  }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SimpleEngine;
}