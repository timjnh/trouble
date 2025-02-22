from .action import Action

class NoneAction(Action):
    def is_applicable(self) -> bool:
        return True

    def apply(self):
        pass