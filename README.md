# Home Assistant - Nexa Bridge X Integration

This is a custom Home Assistant integration for the [Nexa Bridge X](https://nexa.se/nexa-bridge-x).

Makes it possible to view and control devices set up in the Nexa App/Web UI.

> This project is a **unofficial** integration and not affiliated with Nexa in any way.

## Features

> This project depends on you! See the [help file](HELP.md) if you want to see support for more devices.
> I only have access to devices I'm personally using, and this bridge supports several protocols and gateways.

* Monitor energy use
* Monitor switch states
* Monitor dimmer switch states
* Control switches
* Control dimmer switches
* Control lights

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

Add the integration in HA settings and set up the correct connection credentials.

> The factory login is `nexa` / `nexa`.

All connected devices will appear automatically as entities with names based on features and configuration.

> The names configured in the App/Web UI defines the internal unique ID. Changing these
> will create new entities. Duplicate names will be suffixed with a number.

![example entity list](https://user-images.githubusercontent.com/161548/210004115-f69afac7-289b-47f5-801e-fc26a1f9ffb4.png)

## Documentation

See the [help file](HELP.md) if you're having issues with this integration.

Kudos to Nexa for providing developer documentation for this device!

* [Nexa Bridge X API](https://nexa.se/docs/)

## License

MIT
