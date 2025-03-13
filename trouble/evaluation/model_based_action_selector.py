import numpy
from dataclasses import dataclass

from typing import List, Dict

from trouble.gameplay import ActionSelector, SelectedAction
from trouble.gameplay import Board, Color, Peg
from trouble.gameplay.actions import Action, MoveToBoardAction, MoveAction, NoneAction
from trouble.training import Model, EncodedTurnState

@dataclass
class EvaluatedAction:
    action: Action
    peg: Peg
    prediction: numpy.float32

    def __str__(self):
        return f"{self.prediction:.2f} - {self.action.__class__.__name__} for peg {self.peg.id}"

class ModelBasedActionSelector(ActionSelector):
    def __init__(self, model: Model, color_turns: int):
        self._model = model
        self._color_turns = color_turns

    def select_action(self, color: Color, board: Board, die_roll: int) -> SelectedAction:
        evaluated_actions = self.evaluate_possible_actions(color, board, die_roll)

        if len(evaluated_actions) != 0:
            best_action = evaluated_actions[0]
            return SelectedAction(best_action.action, best_action.peg)

        return SelectedAction(NoneAction(), None)
    
    def evaluate_possible_actions(self, color: Color, board: Board, die_roll: int) -> List[EvaluatedAction]:
        possible_actions: List[Action] = [
            MoveToBoardAction(die_roll, color),
            MoveAction(die_roll, color)
        ]

        evaluated_actions = []
        for action in possible_actions:
            pegs = action.get_applicable_pegs(board)
            for peg in pegs:
                evaluated_action = self._evaluate_action(action, peg, board)
                evaluated_actions.append(evaluated_action)
        
        return sorted(evaluated_actions, key=lambda x: x.prediction, reverse=True)
    
    def _evaluate_action(self, action: Action, peg: Peg, board: Board) -> EvaluatedAction:
        updated_board = action.apply(peg, board.copy())

        track_positions_by_color: Dict[Color, List[int]] = {}
        for color in Color:
            track_positions = []
            for p in updated_board.get_pegs_by_color(color):
                track_position = updated_board.get_track_position_for_peg(p)
                track_positions.append(-1 if track_position is None else track_position)
            track_positions_by_color[color] = track_positions

        turn = EncodedTurnState.encode(peg.color, self._color_turns, track_positions_by_color)
        prediction = self._model.predict(turn)

        return EvaluatedAction(action, peg, prediction)