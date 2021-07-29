from dataclasses import dataclass
from functools import cached_property
from typing import List, Dict

from .finders import find_marks
from .mark import Mark


@dataclass
class Pane:
    unwrapped_text: str
    text: str
    pane_current_path: str
    pane_left: int
    pane_right: int
    pane_top: int
    pane_bottom: int

    @cached_property
    def marks(self) -> List[Mark]:
        pane_marks: List[Mark] = []
        path_prefix = self.pane_current_path
        unwrapped_text = self.unwrapped_text
        running_character_total = 0

        for line in unwrapped_text.split('\n'):
            marks = find_marks(line, path_prefix)
            for mark in marks:
                mark.start += running_character_total

            running_character_total += len(line)
            pane_marks += marks

        # Concurrent map is actually _slower_ than a regular map.
        #
        # with futures.ThreadPoolExecutor() as executor:
        #     marks = compact(executor.map(lambda m: find_match(m, text, path_prefix), matches))

        return _unique_sorted_marks(pane_marks)


def _unique_sorted_marks(marks: List[Mark]) -> List[Mark]:
    index: Dict[str, Mark] = {}
    for mark in marks:
        index[mark.text] = mark

    return sorted(index.values(), key=lambda m: m.start)
