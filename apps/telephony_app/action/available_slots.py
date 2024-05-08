from typing import Optional, Type
from pydantic.v1 import BaseModel, Field
import requests
import json

from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.models.actions import (
    ActionConfig,
    ActionInput,
    ActionOutput,
    ActionType,
)


class AvailableSlotsActionConfig(ActionConfig, type='action_available_slots'):
    # todo ActionType.AVAILABLE_SLOTS didn't work, why?

    base_url: str


class AvailableSlotsParameters(BaseModel):
    postal_code: str = Field(..., description="The postal code of the address where the repair job is to be booked")
    appliance_type: str = Field(..., description="The appliance type can either be gas or electric. If not provided, "
                                                 "its electric by default")


class AvailableSlotsResponse(BaseModel):
    success: str


class AvailableSlots(
    BaseAction[
        AvailableSlotsActionConfig, AvailableSlotsParameters, AvailableSlotsResponse
    ]
):
    description: str = "Get available slots by dates for booking"
    parameters_type: Type[AvailableSlotsParameters] = AvailableSlotsParameters
    response_type: Type[AvailableSlotsResponse] = AvailableSlotsResponse

    async def run(
            self, action_input: ActionInput[AvailableSlotsParameters]
    ) -> ActionOutput[AvailableSlotsResponse]:

        params = {
            'targetAddress': 'Postal code: ' + action_input.params.postal_code,
            'filters': json.dumps({'category_id': 1}),
            'appliance_type': action_input.params.appliance_type if action_input.params.appliance_type else 'electric'}
        response = requests.get(self.action_config.base_url + '/api/bookings/availableDates', params=params,
                                headers={'Accept': 'application/json'}).json()

        if response['message'] == 'unknown address':
            return_val = 'The postal code ' + params['targetAddress'] + ' could not be found.'
        else:
            return_val = response['message']

        print('available_slots_response', return_val)

        return ActionOutput(
            action_type=self.action_config.type,
            response=AvailableSlotsResponse(success=return_val),
        )
