# Home Assistant - Nexa Bridge X Integration

This is a custom component for Home Assistant that integrates with the [Nexa Bridge X](https://nexa.se/nexa-bridge-x).

Features:

> See [help](#help) below if you want to see support for more devices. I don't personally own every single type, and this hub supports devices with different protocols.

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

All connected devices will appear automatically as entities with names based on features and configuration.

> Note that names are based on device configuration in the Nexa Admin UI. Rooms are not taken into account.

## Documentation

* [Nexa Bridge X API](https://nexa.se/docs/)

## Help

If you're having issues or don't see support for a device you have connected to your hub,
run the following commands and open an issue with the files attached:

```bash
# You might wanna look through this and remove any location and IP information
curl --user nexa:nexa http://<ip-of-hub>/v1/info -o hub-information.txt
```

```bash
curl --user nexa:nexa http://<ip-of-hub>/v1/nodes -o hub-nodes.txt
```

## Notes

This project was developed with a hub with firmware version `2.4.1`.

## License

MIT
