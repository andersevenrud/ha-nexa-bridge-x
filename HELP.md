# Help

This project was developed using a bridge with firmware version `2.4.1`. The legacy
non-X bridge is also supported but with limited functionality.

The bridges are codenamed:

* `Bridge1` with `1.6` firmware or lower (legacy)
* `Bridge2` with `1.7.3` formware or `2.x` (aka "X")

**Ensure that your firmware is up to date**. Some X bridges ship with old firmware.

## I can't connect

Ensure that you're connecting to the correct IP and with the correct credentials.

> The factory login is `nexa` / `nexa`.

## I don't see any sensor values

If you have registered a new device in the App/Web UI you have to reload the integration first.
This is done from the integration settings and the hamburger menu on the card shown on the page.
If it still does not show up, see [connection issues](#connection-issues);

Note that the Nexa Bridge in some cases does not expose all of your sensor values. It is not
a regular z-wave interface, but a custom API. There is an issue that tracks
[tested devices](https://github.com/andersevenrud/ha-nexa-bridge-x/issues/6).

## How do I use my stateless switches ?

You should be able to use the events `nexa_bridge_x_custom_event` for automation
where the `type` field contains the event from the device.

## I'm still having issues. Help!

Create a [new issue on github](https://github.com/andersevenrud/ha-nexa-bridge-x/issues/new)
with a description of the problem and copies of any errors from HA logs, and preferrably data
dumps from your bridge.

Providing data dumps can be done with utilities like [Postman](https://www.postman.com/downloads/).

The most critical data comes from `http://<bridge-ip-address>/api/info` and
`http://<bridge-ip-address>/api/nodes` and can be accessed using `nexa` as both username
and password with Digest Authentication enabled.

**Some of this data can contain personal information (like location in the "info"), so make sure
to censor this before attaching to the issue.**

### Enabling debug logs

This can be viewed from `Settings -> System -> Logs -> LOAD FULL LOGS`.

For more verbose information from this integration, add the following
to your `configuration.yaml` file:

```yaml
logger:
  logs:
    custom_components.nexa_bridge_x: debug
```
