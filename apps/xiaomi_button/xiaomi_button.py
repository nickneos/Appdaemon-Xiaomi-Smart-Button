import appdaemon.plugins.hass.hassapi as hass

# default values
DEFAULT_SERVICE = "turn_on"
DEFAULT_DIM_STEP_VALUE = 3

SERVICE_OPTIONS = [
    "turn_on",
    "turn_off",
    "toggle",
    "dim_step"
]

class Button(hass.Hass):
    """ """

    def initialize(self):
        """ """
        self.buttons = self.args.get("buttons", [])
        self.actions = self.args.get("actions", [])
        
        for button in self.args["buttons"]:
            self.listen_event(self.cb_button_press, "xiaomi_aqara.click",
                              entity_id = button)

    def cb_button_press(self, event_name, data, kwargs):
        """ Callback function when button is pressed """
        event_click = data["click_type"]
        button = kwargs["entity_id"]
        
        for action in self.actions:
            if event_click == action["click_type"]:
                self.log(f"{button}: {action}")
                self.perform_action(action)
                break

    def perform_action(self, action):
        """ Perform action based on the service of the action """
        service = action.get("service", DEFAULT_SERVICE)
        dim_step_value = action.get("dim_step_value", DEFAULT_DIM_STEP_VALUE)
        tgt_devs = action.get("target_device", [])
        tgt_devs = tgt_devs if type(tgt_devs) is list else [tgt_devs]

        if service not in SERVICE_OPTIONS:
            self.log("Service not valid option")
            return

        for device in tgt_devs:
            if service == "turn_on":
                self.turn_on_service(device)
            elif service == "turn_off":
                self.turn_off_service(device)
            elif service == "toggle":
                self.toggle_service(device)
            elif service == "dim_step":
                self.dim_service(device, dim_step_value)

    def turn_on_service(self, device):
        """ turns on device """
        if self.get_state(device) == "on":
            self.log(f"{device} already on")
            return

        self.log(f"Turning on {device}")
        self.turn_on(device)

    def turn_off_service(self, device):
        """ turns off device """
        if self.get_state(device) == "off":
            self.log(f"{device} already off")
            return

        self.log(f"Turning off {device}")
        self.turn_off(device)

    def toggle_service(self, device):
        """ toggles device """
        self.log(f"Toggle {device}")
        self.toggle(device)
    
    def dim_service(self, light, dim_step):
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


    def bound_to_100(self, number):
        """
        Convert HomeAssistant-usable brightness level to something that is
        human readable
        """
        return round(int(float(number)) / 255 * 100)

