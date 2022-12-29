# Home Assistant - Nexa Bridge X Integration

This is a custom component for Home Assistant that integrates with the [Nexa Bridge X](https://nexa.se/nexa-bridge-x).

> The Nexa is a hub that collects data from various devices and represents it with a REST API and Websocket.

Features:

* Monitor energy use
* Monitor switch states
* Minitor dimmer states
* Control switches
* Control dimmers/lights

## Installation

### Automatic

* Install and open https://hacs.xyz/
* Click on download button
* Search for "Nexa Bridge X" and download
* Restart HA

If for some reason the search comes up empty, select the hamburger menu and add a custom
repository with the URL to this repo and select the integration type.

### Manual

* In your HA installation ensure that a folder named `custom_components` exists in your configuration directory
* Download this repository
* Place `custom_components/nexa_bridge_x` inside your `custom_components` folder.

## Usage

Add the integration in HA settings and set up the correct connection credentials.

All connected devices will appear automatically as entities with names based on features.

## Documentation

* [Nexa Bridge X API](https://nexa.se/docs/)

## License

MIT
