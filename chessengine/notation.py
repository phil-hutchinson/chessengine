from typing import Union


class Notation:
    file_naming: dict[int, str] = {
        1: 'A',
        2: 'B',
        3: 'C',
        4: 'D',
        5: 'E',
        6: 'F',
        7: 'G',
        8: 'H',
    }

    @staticmethod
    def build_notation(start_pos: tuple[int, int], end_pos: tuple[int, int], promotion: Union[str, None] = None) -> str:
        start_notation = Notation.file_naming[start_pos[0]] + str(start_pos[1])
        end_notation = Notation.file_naming[end_pos[0]] + str(end_pos[1])
        promotion_notation = ' ' + promotion if isinstance(promotion, str) else ''
        return start_notation + end_notation + promotion_notation
        
        

