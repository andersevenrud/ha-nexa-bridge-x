# Home Assistant - Nexa Bridge X Integration

This is a *unofficial* Home Assistant integration for the [Nexa Bridge X](https://nexa.se/nexa-bridge-x).

> The "Bridge X" has the product name Bridge2. Legacy "Bridge1" and latest "Bridge3" is also supported.

Makes it possible to view and control devices set up in the Nexa App/Web UI.

> This project depends on you! I don't have access to different types of firmware and limited access to smart
> devices supported by the bridge. Go to the [device support](https://github.com/andersevenrud/ha-nexa-bridge-x/issues/6)
> issue on github for more information or to report experience with your devices.

## Features

* Monitor energy use
* Monitor switch states
* Monitor dimmer levels
* Monitor sensors (temperatures, humidity, luminance, etc.)
* Monitor binary sensors (motion, contact, smoke, etc.)
* Control switches
* Control dimmer levels
* Control lights (Hue, Trådfri, Twinkly)
* Control media player (Sonos)

## Installation

### Managed

Installation is easiest using [HACS](https://hacs.xyz/):

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=andersevenrud&repository=ha-nexa-bridge-x).

### Manual

* [Download a release](https://github.com/andersevenrud/ha-nexa-bridge-x/releases)
* Create a `custom_components` directory inside of your HA configuration directory
* Unzip into the `custom_components` directory
* Restart HA

## Setup

Your bridge should be discovered automatically in the integrations list
under "devices & settings" in the settings page.
Just click the configure button and you should be ready to go!

> If it's not showing, just click the "add integration" button and search for
> "Nexa Bridge X",

All connected sensors etc. will be available as Entities inside Home Assistant.

> The names are taken from configurations in the App/Web UI.
> It is recommended that you name them something simple, i.e. if you have a switch
> in your connected to a power strip, lamp, etc. name it "Living Room".

## Documentation

* [Help for this integration](https://github.com/andersevenrud/ha-nexa-bridge-x/blob/main/HELP.md)
* [Nexa Bridge X API](https://nexa.se/docs/)
* [Misc documentation](https://gist.github.com/andersevenrud/e4637c0cbde665f72f864032e540aa5d)

Kudos to Nexa for providing developer documentation for this device!

## License

[MIT](https://github.com/andersevenrud/ha-nexa-bridge-x/blob/main/LICENSE)
