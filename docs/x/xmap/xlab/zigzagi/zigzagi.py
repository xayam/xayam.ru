import numpy as np

# Константы ценности фигур для примитивной оценки
# Если фигура съедена (маска == 0), ее ценность не учитывается
PIECE_VALUES = {
    "K": 10000, "Q": 900, "R": 500, "B": 330, "N": 320, "P": 100
}
# Индексы фигур в нашей матрице 32х64 (для примера)
# 0-15: Белые, 16-31: Черные. 0: Белый Король, 16: Черный Король
WHITE_KING_IDX = 0
BLACK_KING_IDX = 16

class QuantumSearchEngine:
    def __init__(self):
        pass

    def evaluate_board(self, board_matrix):
        """
        Примитивная функция оценки.
        Считает сумму выживших полей (битов) для каждой фигуры, умноженную на их ценность.
        Если короля нет ни в одной из веток (маска == 0) — это мат.
        """
        # Если маска белого короля полностью занулилась во всех ветках суперпозиции
        if board_matrix[WHITE_KING_IDX] == 0:
            return -200000  # Черные поставили мат
        # Если занулилась маска черного короля
        if board_matrix[BLACK_KING_IDX] == 0:
            return 200000   # Белые поставили мат

        score = 0
        # Белые фигуры (0-15)
        for i in range(16):
            if board_matrix[i] > 0:
                # bin(x).count('1') показывает, в скольких параллельных мирах фигура еще жива
                score += bin(board_matrix[i]).count('1') * 10  # базовый вес суперпозиции
                
        # Черные фигуры (16-31)
        for i in range(16, 32):
            if board_matrix[i] > 0:
                score -= bin(board_matrix[i]).count('1') * 10
                
        return score

    def generate_all_quantum_moves(self, board_matrix, is_white):
        """
        Генератор ходов. Возвращает список возможных квантовых ходов.
        Каждый ход — это (piece_idx, new_quantum_mask)
        В реальности здесь будет шахматная логика. Для примера генерируем гипотетические маски.
        """
        moves = []
        start_idx, end_idx = (0, 16) if is_white else (16, 32)
        
        for piece_idx in range(start_idx, end_idx):
            current_mask = board_matrix[piece_idx]
            if current_mask == 0: 
                continue  # Фигура полностью съедена во всех мирах, пропускаем
                
            # Моделируем суперпозицию: фигура может пойти на два поля одновременно
            # Создаем несколько вариантов квантовых масок (суперпозиций ходов)
            # В реальном движке эти маски вычисляются по правилам (например, маска ходов коня)
            if piece_idx == 1: # Допустим, это Белый Конь
                # Вариант хода А: прыгнуть на поля с индексами 18 и 22 одновременно
                mask_A = (1 << 18) | (1 << 22)
                moves.append((piece_idx, mask_A))
            else:
                # Для остальных фигур просто сдвигаем их текущую суперпозицию (для теста)
                mask_generic = current_mask << 1 | current_mask << 2
                moves.append((piece_idx, mask_generic))
                
        return moves

    def apply_move(self, board_matrix, piece_idx, new_mask):
        """
        Применяет квантовый ход к матрице доски и обрабатывает запутанные взятия.
        Возвращает копию новой доски.
        """
        next_board = np.copy(board_matrix)
        
        # 1. Сверхпозиционный ход фигуры
        next_board[piece_idx] = new_mask
        
        # 2. АВТОМАТИЧЕСКАЯ ЗАПУТАННОСТЬ И ВЗЯТИЯ:
        # Проверяем, пересекается ли новая маска фигуры с фигурами противника
        # Если пересекается, противник уничтожается ТОЛЬКО на этих полях
        is_white = piece_idx < 16
        enemy_start, enemy_end = (16, 32) if is_white else (0, 16)
        
        for enemy_idx in range(enemy_start, enemy_end):
            # Побитовое И находит точки пересечения в суперпозиции
            intersection = next_board[enemy_idx] & new_mask
            if intersection > 0:
                # Зануляем биты противника только там, где наступила атакующая фигура
                # На остальных полях в параллельных мирах фигура противника остается жива!
                next_board[enemy_idx] &= ~intersection
                
        return next_board

    def quantum_search(self, board_matrix, depth, alpha, beta, is_white_turn):
        """
        Общий квантовый алгоритм поиска (основа Minimax).
        Просчитывает параллельные состояния доски вглубь.
        """
        # Базовый случай: достигли дна поиска или одна из сторон полностью проиграла (мат)
        if depth == 0 or board_matrix[WHITE_KING_IDX] == 0 or board_matrix[BLACK_KING_IDX] == 0:
            return self.evaluate_board(board_matrix), None

        possible_moves = self.generate_all_quantum_moves(board_matrix, is_white_turn)
        if not possible_moves:
            return self.evaluate_board(board_matrix), None  # Пат / Нет ходов

        best_move = None

        if is_white_turn:
            max_eval = -float('inf')
            for piece_idx, new_mask in possible_moves:
                # Делаем ход сразу во всей суперпозиции
                next_board = self.apply_move(board_matrix, piece_idx, new_mask)
                
                # Рекурсивно уходим вглубь за черных
                evaluation, _ = self.quantum_search(next_board, depth - 1, alpha, beta, False)
                
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = (piece_idx, new_mask)
                    
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break  # Альфа-бета отсечение
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for piece_idx, new_mask in possible_moves:
                next_board = self.apply_move(board_matrix, piece_idx, new_mask)
                evaluation, _ = self.quantum_search(next_board, depth - 1, alpha, beta, True)
                
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = (piece_idx, new_mask)
                    
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval, best_move

# --- ДЕМОНСТРАЦИЯ РАБОТЫ ДВИЖКА ---
if __name__ == "__main__":
    engine = QuantumSearchEngine()
    
    # Создаем пустую квантовую доску 32х64
    initial_board = np.zeros(32, dtype=np.uint64)
    
    # Ставим белого короля на e1 (индекс клетки 4) -> 1 << 4 = 16
    initial_board[WHITE_KING_IDX] = np.uint64(1 << 4)
    # Ставим черного короля на e8 (индекс клетки 60) -> 1 << 60
    initial_board[BLACK_KING_IDX] = np.uint64(1 << 60)
    # Ставим белого коня на b1 (индекс клетки 1) -> 1 << 1 = 2
    initial_board[1] = np.uint64(1 << 1)
    
    print("Запуск квантового поиска на глубину 3...")
    best_score, best_quantum_move = engine.quantum_search(
        initial_board, depth=3, alpha=-float('inf'), beta=float('inf'), is_white_turn=True
    )
    
    print(f"Поиск завершен!")
    print(f"Лучшая оценка суперпозиции: {best_score}")
    print(f"ID лучшей фигуры для хода: {best_quantum_move[0]} (Маска новой суперпозиции: {bin(best_quantum_move[1])})")
