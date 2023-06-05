# Help

## How do I use my stateless switches ?

You should be able to use the events `nexa_bridge_x_custom_event` for automation
where the `type` field contains the event from the device.

## Logs

The first thing you should do is to check the logs from Home Assistant.

> This can be viewed from `Settings -> System -> Logs -> LOAD FULL LOGS`.

For more verbose information from this integration, add the following
to your `configuration.yaml` file:

```yaml
logger:
  logs:
    custom_components.nexa_bridge_x: debug
```

## Device Compatibility

See [the device issue](https://github.com/andersevenrud/ha-nexa-bridge-x/issues/6)
for information.

## Bridge Compatibility

This project was developed using a bridge with firmware version `2.4.1`.

Assuming Nexa uses appropriate versioning, this integration *should* be compatible with any
firmware version starting with `2`.

> The legacy "Nexa Bridge" (non-X) with version `1` firmware is supported, but with limited functionality.

## I can't connect

Ensure that you're connecting to the correct IP and with the correct credentials.

> The factory login is `nexa` / `nexa`.

## I can't see my device

If you have registered a new device in the App/Web UI you have to reload the integration first.
This is done from the integration settings and the hamburger menu on the card shown on the page.
If it still does not show up, see [connection issues](#connection-issues);

## Connection issues

If you have general issues with connectivity (or crashes related) to the bridge or devices,
create a [new issue on github](https://github.com/andersevenrud/ha-nexa-bridge-x/issues/new)
with a description of the problem and copies of any errors from HA, and preferrably data
dumps from your bridge.

Providing data dumps can be done with utilities like [Postman](https://www.postman.com/downloads/).

The most critical data comes from `http://<bridge-ip-address>/api/info` and
`http://<bridge-ip-address>/api/nodes` and can be accessed using `nexa` as both username
and password.

**Some of this data can contain personal information (like location in the "info"), so make sure
to censor this before attaching to the issue.**
