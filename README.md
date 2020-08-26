# Xiaomi Smart Button
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs) [![homeassistant_community](https://img.shields.io/badge/HA%20community-forum-brightgreen)](https://community.home-assistant.io/) 

<a href="https://www.buymeacoffee.com/so3n" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

Customise what happens when you press a Xiaomi Wireless Button.

## Features
* Supports recoginising single click, double click and long click button presses for supported Xiaomi Buttons.
* Can perform a variety of actions as desired (eg. turing on/off a device, dimming lights, etc)

## Components Needed
* [Xiaomi Gateway](https://www.gearbest.com/living-appliances/pp_344667.html)
* [Xiaomi Wireless Button](https://www.gearbest.com/smart-home-controls/pp_009395405312.html?wid=1349303)

_Setting up in Home Assistant: [https://www.home-assistant.io/integrations/xiaomi_aqara/](https://www.home-assistant.io/integrations/xiaomi_aqara/)_

## Installing

Install via [HACS](https://hacs.xyz/). Alternatively, place the apps folder and its contents in your appdaemon folder.

## Configuration

### Main Config options

| Variable | Type           | Required | Default | Description                                                                                       |
| -------- | -------------- | -------- | ------- | ------------------------------------------------------------------------------------------------- |
| module   | string         | True     |         | Set to `xiaomi_button`                                                                            |
| class    | string         | True     |         | Set to `Button`                                                                                   |
| buttons  | string or list | True     |         | `entity_id` of the xiaomi button. Can include multiple entities in a list or just one as a string |
| actions  | list           | True     |         | List of actions. See Below                                                                        |

### `Actions` Config Options

| Variable       | Type    | Required | Default | Description                                                                                                                                                                                                        |
| -------------- | ------- | -------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| click_type     | string  | False    | single  | For buttons that support multiple click types (eg. single click, double click and long press) specify which one to trigger this action. Valid options are `single`, `double` and `long_click_press`                |
| target_device  | string  | True     |         | `entity_id` of the device that responds to button press. Alternatively can use the keywords `lights`, `all_lights` or `group.all_lights` to specify all light devices. Multiple entities can be provide in a list. |
| action_type    | string  | False    | toggle  | Valid options are `turn_on`, `turn_off`, `toggle` and `dim_step`                                                                                                                                                   |
| dim_step_value | integer | False    | 3       | For `dim_step` `action_type`, the number of steps to cycle through brightness increments. (eg. value of 3 will cycle through 33%, 66% and 100% brightness)                                                         |

### Example usage 1
Bedside buttons that perform the following actions:
* **on single press:** toggle bedroom light
* **on double click:** toggle bedroom TV
* **on long press:** turn off all lights and other devices in the house that might be on

```yaml
bedroom_buttons:
  module: xiaomi_button
  class: Button
  buttons:
    - binary_sensor.xiaomi_switch_1
    - binary_sensor.xiaomi_switch_2
  actions:
    - click_type: single
      target_device: light.bedroom
      action_type: toggle
    - click_type: double
      target_device: switch.bedroom_tv
      action_type: toggle
    - click_type: long_click_press
      target_device: 
        - lights
        - remote.living_room
        - climate.main
      action_type: turn_off
```

### Example usage 2
Button to control a light with the following actions:
* **on single press:** turn on light and increment the brightness with each press (at 4 steps: 25%, 50%, 75% and 100% brightness).
* **on long press:** turn off light

```yaml
lamp_button:
  module: xiaomi_button
  class: Button
  buttons: binary_sensor.xiaomi_switch_5
  actions:
    - click_type: single
      target_device: light.floor_lamp
      action_type: dim_step
      dim_step_value: 4
    - click_type: long_click_press
      target_device: light.floor_lamp
      action_type: turn_off
```

<hr/>

<a href="https://www.buymeacoffee.com/so3n" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
