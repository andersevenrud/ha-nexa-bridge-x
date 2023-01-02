# Home Assistant - Nexa Bridge X Integration

This is a custom Home Assistant integration for the [Nexa Bridge X](https://nexa.se/nexa-bridge-x).

Makes it possible to view and control devices set up in the Nexa App/Web UI.

> This project is a **unofficial** integration and not affiliated with Nexa in any way.

## Features

> This project depends on you! I don't have access to all the devices supported
> by this bridge. Go to the [device support](https://github.com/andersevenrud/ha-nexa-bridge-x/issues/6)
> issue on github for more information or to report experience with your devices.

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

* Install and open [HACS](https://hacs.xyz/)
* Click on download button
* Search for "Nexa Bridge X" and download
* Restart HA

> If for some reason the search comes up empty, select the hamburger menu and add a custom
> repository with the URL to this repo and select the integration type.

### Manual

* [Download a release](https://github.com/andersevenrud/ha-nexa-bridge-x/releases)
* Create a `custom_components` directory inside of your HA `config` directory
* Unzip into the `custom_components` directory
* Restart HA

## Setup

Your bridge should be discovered automatically. Just click the configure button
and you should be ready to go!

> If it's not showing, just click the "add integration" button and search for
> "Nexa Bridge X" to manually add it. This requires entering login information.
> The factory login is `nexa` / `nexa`.

All connected devices will appear automatically as a device with entities using
names based on features and configuration.

> The names configured in the App/Web UI defines the internal unique ID. Changing these
> will create new entities. Duplicate names will be suffixed with a number.
> It is recommended that you name them something simple, i.e. if you have a switch
> in your connected to a power strip, lamp, etc. name it "Living Room". All devices
> gets suffixed in HA with the type of device.

## Documentation

* [Help for this integration](https://github.com/andersevenrud/ha-nexa-bridge-x/blob/main/HELP.md)
* [Nexa Bridge X API](https://nexa.se/docs/)
* [Misc documentation](https://gist.github.com/andersevenrud/e4637c0cbde665f72f864032e540aa5d)

Kudos to Nexa for providing developer documentation for this device!

## License

MIT
