# Help

## Device Compatibility

See [the device issue](https://github.com/andersevenrud/ha-nexa-bridge-x/issues/6)
for information.

## Bridge Compatibility

This project was developed using a bridge with firmware version `2.4.1`.

Assuming Nexa uses appropriate versioning, this integration *should* be compatible with any
firmware version starting with `2`.

## I can't connect

Ensure that you're connecting to the correct IP and with the correct credentials.

> The factory login is `nexa` / `nexa`.

## I can't see my device

> If you have registered a new device in the App/Web UI you have to reload the integration first.
> This is done from the integration settings and the hamburger menu on the card shown on the page.
> If it still does not show up, proceed with instructions.

If you're having issues with a device or don't see a device you have connected to your bridge,
run the following commands:

```bash
curl --user nexa:nexa http://<ip-of-bridge>/v1/info -o bridge-information.txt
curl --user nexa:nexa http://<ip-of-bridge>/v1/nodes -o bridge-nodes.txt
```

> **Make sure to remove any personal information from the information file. This will contain
> location data.**

Then leave a [comment in the device issue](https://github.com/andersevenrud/ha-nexa-bridge-x/issues/6) with the files attached.

