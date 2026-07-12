/**
 * D12 Dice Module for Random Chess
 * Each D12 has: 6 white pieces + 6 black pieces
 */

const D12_FACES = [
  { symbol: '♙', color: 'white', type: 'p' }, // Pawn
  { symbol: '♘', color: 'white', type: 'n' }, // Knight
  { symbol: '♗', color: 'white', type: 'b' }, // Bishop
  { symbol: '♖', color: 'white', type: 'r' }, // Rook
  { symbol: '♕', color: 'white', type: 'q' }, // Queen
  { symbol: '♔', color: 'white', type: 'k' }, // King
  { symbol: '♟', color: 'black', type: 'p' },
  { symbol: '♞', color: 'black', type: 'n' },
  { symbol: '♝', color: 'black', type: 'b' },
  { symbol: '♜', color: 'black', type: 'r' },
  { symbol: '♛', color: 'black', type: 'q' },
  { symbol: '♚', color: 'black', type: 'k' }
];

class D12Dice {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.dice = [];
    this.results = [];
  }

  /**
   * Roll all three D12 dice with animation
   * @returns {Promise<Array>} Array of 3 results
   */
  async roll() {
    this.results = [];
    const dieElements = this.container.querySelectorAll('.die');
    
    // Animation phase
    for (let i = 0; i < 3; i++) {
      dieElements[i].classList.add('rolling');
      dieElements[i].textContent = '?';
    }
    
    // Simulate rolling delay
    await this._delay(600);
    
    // Generate and display results
    for (let i = 0; i < 3; i++) {
      const result = this._rollSingle();
      this.results.push(result);
      dieElements[i].classList.remove('rolling');
      dieElements[i].textContent = result.symbol;
      dieElements[i].className = `die d12 ${result.color}-piece`;
      await this._delay(100);
    }
    
    return this.results;
  }

  /**
   * Roll a single D12 die
   * @returns {Object} Dice result
   */
  _rollSingle() {
    const index = Math.floor(Math.random() * D12_FACES.length);
    return { ...D12_FACES[index] };
  }

  /**
   * Helper: delay in ms
   */
  _delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Get results formatted for game logic
   * @param {string} currentPlayerColor - 'white' or 'black'
   * @returns {Object} { mandatory: [], optional: [] }
   */
  getMovesForPlayer(currentPlayerColor) {
    const mandatory = []; // Own color pieces - must move if possible
    const optional = [];  // Opponent pieces - can move optionally
    
    this.results.forEach(result => {
      if (result.color === currentPlayerColor) {
        mandatory.push(result.type);
      } else {
        optional.push(result.type);
      }
    });
    
    return { mandatory, optional };
  }

  /**
   * Reset dice display
   */
  reset() {
    const dieElements = this.container.querySelectorAll('.die');
    dieElements.forEach(die => {
      die.textContent = '?';
      die.className = 'die d12';
    });
    this.results = [];
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { D12Dice, D12_FACES };
}