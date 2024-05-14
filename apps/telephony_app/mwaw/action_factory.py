from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.action.factory import ActionFactory
from vocode.streaming.models.actions import ActionConfig
from .actions.available_slots import AvailableSlots, AvailableSlotsConfig


class MwawActionFactory(ActionFactory):
    def create_action(self, action_config: ActionConfig) -> BaseAction:
        if isinstance(action_config, AvailableSlotsConfig):
            return AvailableSlots(action_config, should_respond=True)
        else:
            raise Exception("Invalid action type")
