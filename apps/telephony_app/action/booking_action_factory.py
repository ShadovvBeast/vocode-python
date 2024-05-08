from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.action.factory import ActionFactory
from vocode.streaming.models.actions import (
    ActionConfig,
)
from available_slots import AvailableSlotsActionConfig, AvailableSlots


class BookingActionFactory(ActionFactory):
    def create_action(self, action_config: ActionConfig) -> BaseAction:
        if isinstance(action_config, AvailableSlotsActionConfig):
            return AvailableSlots(action_config, should_respond=True)
        else:
            raise Exception("Invalid action type")
