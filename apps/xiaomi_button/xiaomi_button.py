"""
Customise what happens when you press a Xiaomi Wireless Button
https://github.com/nickneos/Appdaemon-Xiaomi-Smart-Button
"""

import appdaemon.plugins.hass.hassapi as hass

# default values
DEFAULT_ACTION_TYPE = "toggle"
DEFAULT_CLICK_TYPE = "single"
DEFAULT_DIM_STEP_VALUE = 3

ACTION_TYPE_OPTIONS = [
    "turn_on",
    "turn_off",
    "toggle",
    "dim_step",
    "cycle"
]
ALL_LIGHTS_NAME = [
    "lights",
    "all_lights",
    "group.all_lights"
]

class Button(hass.Hass):
    """Define a Xiaomi Switch base feature"""

    def initialize(self):
        """Initialize AppDaemon App"""

        # get config values
        self.buttons = self.args.get("buttons", [])
        self.actions = self.args.get("actions", [])

        # integer counter used for cycle function
        self.cycle_idx = -1
        
        # convert buttons to list
        if type(self.buttons) is not list:
            self.buttons = [self.buttons]


        for button in self.buttons:
            self.listen_event(self.cb_button_press, "xiaomi_aqara.click", entity_id = button)


    def cb_button_press(self, event_name, data, kwargs):
        """Callback function when button is pressed"""

        button_event = data["click_type"]
        
        for action in self.actions: 
            if button_event == action.get("click_type", DEFAULT_CLICK_TYPE):
                self.perform_action(action)
                break


    def perform_action(self, action):
        """ Perform action based on the type of the action """

        action_type = action.get("action_type", DEFAULT_ACTION_TYPE)
        dim_step_value = action.get("dim_step_value", DEFAULT_DIM_STEP_VALUE)
        tgt_devs = action.get("target_device", [])
        parameters = action.get("parameters", {})

        if action_type not in ACTION_TYPE_OPTIONS:
            self.log("Action Type not valid option", level="ERROR")
            return

        if type(tgt_devs) is not list:
            tgt_devs = [tgt_devs]

        for entity in tgt_devs:

            # handle dim_step action
            if action_type == "dim_step":
                self.dim_action(entity, dim_step_value)
                self.cycle_idx = -1
                return
            
            # handle cycle action
            if action_type == "cycle":
                parameters = [parameters] if type(parameters) is not list else parameters
                self.cycle_action(entity, parameters)
                return

            # reset index to -1 on turn_off
            if action_type == "turn_off":
                self.cycle_idx = -1

            # handle entity for all lights
            if entity in ALL_LIGHTS_NAME:
                self.call_service(
                    f"light/{action_type}", 
                    entity_id="all", 
                    **parameters
                )
                return

            # lets do this
            self.call_service(
                f"{entity.split('.')[0]}/{action_type}",
                entity_id=entity,
                **parameters
            )
    

    def dim_action(self, light, dim_step):
        """ increments brightness of light """
        
        if self.get_state(light) == "off":
            self.call_service("light/turn_on", entity_id = light)
        else:
            dim_step_pct = round(100 / dim_step)
            brightness = self.get_state(light, attribute = "brightness")
            if brightness:
                brightness = self.bound_to_100(brightness)
                brightness = brightness + dim_step_pct
                if brightness > 100:
                    brightness = dim_step_pct
                self.call_service("light/turn_on", entity_id = light, brightness_pct = brightness)


    def cycle_action(self, light, param_list):
        """Cycle through the parameter list with each button press"""

        # when index -1, turn on light with previous settings
        if self.cycle_idx == -1:
            parameters = {}
        # otherwise get paramaters from list using index value
        else:
            try:
                parameters = param_list[self.cycle_idx]
            except IndexError:
                self.cycle_idx = 0
                parameters = param_list[self.cycle_idx]

        # lets do this
        self.call_service(
            f"{light.split('.')[0]}/turn_on",
            entity_id=light,
            **parameters
        )

        # increment index for next button press
        self.cycle_idx += 1



    def bound_to_100(self, number):
        """
        Convert HomeAssistant-usable brightness level to something that is
        human readable
        """
        return round(int(float(number)) / 255 * 100)
