# Home Assistant - Nexa Bridge X Integration

This is a custom integration for Home Assistant that integrates with the [Nexa Bridge X](https://nexa.se/nexa-bridge-x).

Makes it possible to view and control devices set up in the Nexa App (or Admin Web UI).

## Features

> See [help](#help) below if you want to see support for more devices. I don't personally own every single type, and this bridge supports devices with different protocols.

* Monitor energy use
* Monitor switch states
* Monitor dimmer switch states
* Control switches
* Control dimmer switches
* Control lights

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

## Setup

Add the integration in HA settings and set up the correct connection credentials.

> The factory login is `nexa` / `nexa`.

All connected devices will appear automatically as entities with names based on features and configuration.

> Note that names are based on device configuration in the Nexa Admin UI. Rooms are not taken into account.

![example entity list](https://user-images.githubusercontent.com/161548/210004115-f69afac7-289b-47f5-801e-fc26a1f9ffb4.png)

## Documentation

* [Nexa Bridge X API](https://nexa.se/docs/)

## Help

If you're having issues with a device or don't see a device you have connected to your bridge,
run the following commands:

> If you have registered a new device in the app you have to reload the integration first.
> This is done from the integration settings and the hamburger menu on the card shown on the page.
> If it still does not show up, proceed with instructions.

```bash
curl --user nexa:nexa http://<ip-of-bridge>/v1/info -o bridge-information.txt
curl --user nexa:nexa http://<ip-of-bridge>/v1/nodes -o bridge-nodes.txt
```

> **Make sure to remove any personal information from the information file. This will contain
> location data.**

Then leave a [comment in the device issue](https://github.com/andersevenrud/ha-nexa-bridge-x/issues/6) with the files attached.

## Notes

This project was developed with a bridge with firmware version `2.4.1`.

## License

MIT
