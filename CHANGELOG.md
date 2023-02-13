# Changelog

## [v1.1.2] - 2023-02-13
### :recycle: Refactors
- [`9bb9375`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/9bb93752f2e927de682460ba68d3165277cbc6fe) - don't mutate local state on switch/dimmer actions *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`8b78359`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/8b783596e707325fc3a250f93b1e9c1a93982ec3) - **nexa**: decrease log level for coordinator ready state *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v1.1.1] - 2023-02-13
### :bug: Bug Fixes
- [`d9f8918`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/d9f89183592d1db669781591f254595f6acbdec7) - **nexa**: hotfix because no config migration *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v1.1.0] - 2023-02-13
### :sparkles: New Features
- [`b940de2`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/b940de25b4c8135d360be6dd3344dd2fe5eb7bcd) - basic legacy api support *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`4538226`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/4538226bb76ba9ef2bed25737fc2a793ec66568f) - **const**: add configuration for level/switch sensor *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`cc2ab8d`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/cc2ab8db7a521390e99e290eeedb7c75981a7c38) - **const**: bump polling timings *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`a7e9692`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/a7e96925b8950d17d101fa2a71c3fedef640992a) - add method call timeout value *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v1.0.5] - 2023-02-12
### :bug: Bug Fixes
- [`f7c6fad`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/f7c6fadaeaa286fc5e9f03c1fa088080d341c2dd) - **const**: current kwh invalid unit *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v1.0.4] - 2023-02-12
### :bug: Bug Fixes
- [`52f4f9e`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/52f4f9ed56f89dfbb072d9b5943e350f34b40969) - **const**: current kwh invalid device *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :recycle: Refactors
- [`e93d09b`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/e93d09b960eb264a05859acb976e26b7db5acc3e) - move default credentials to const *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`275fbb3`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/275fbb33850c31ae0883d5e8c1d6488fcd2cdde8) - **config_flow**: add default login credentials *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v1.0.3] - 2023-02-05
### :bug: Bug Fixes
- [`e031387`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/e031387e297d2a6e870350e85827955730531c11) - **nexa**: incorrect password lookup *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v1.0.2] - 2023-01-04
### :bug: Bug Fixes
- [`c11a4e4`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/c11a4e4d6fbeacb3619f5a756e41bdea406cc159) - wrong label on humidity sensor *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v1.0.1] - 2023-01-03
### :bug: Bug Fixes
- [`8136e36`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/8136e3699366c486962c9d5e44034cb6f59b41c0) - correctly set nested names *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v1.0.0] - 2023-01-03
### :boom: BREAKING CHANGES
- due to [`a97edf2`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/a97edf2d61d2681f8875de5e7eab694e4fafeb74) - nest devices with devices *(commit by [@andersevenrud](https://github.com/andersevenrud))*:

  nest devices with devices


### :sparkles: New Features
- [`a97edf2`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/a97edf2d61d2681f8875de5e7eab694e4fafeb74) - nest devices with devices *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.15.0] - 2023-01-03
### :sparkles: New Features
- [`758470e`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/758470e3075d23f221d439a173bb2e19d235eaa4) - syncronize values with timestamps *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.14.0] - 2023-01-02
### :sparkles: New Features
- [`7debb71`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/7debb71f2c1e102fe90948ba85391451d0f0eb71) - also show switches as binary sensor *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.13.0] - 2023-01-02
### :sparkles: New Features
- [`b01759f`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/b01759f7300abc14869ca68c4ede539823177134) - listen on websocket for updates *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.12.0] - 2023-01-02
### :sparkles: New Features
- [`59d7bc7`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/59d7bc72cf81a063a52c9a0e5b1f51c3be84a0dc) - battery level sensor support *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :bug: Bug Fixes
- [`ca2ee03`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/ca2ee038df1c322d3d193e81be48e8d381628181) - correctly detect binary switches *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.11.0] - 2023-01-01
### :sparkles: New Features
- [`2d70ac2`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/2d70ac2a80ad12762a34124a559198833af9cdfd) - add zeroconf to dependencies *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :recycle: Refactors
- [`1f50161`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/1f5016177abf8f96bf9266faf951c59447453ebd) - direct api calls from entities *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.10.2] - 2023-01-01
### :bug: Bug Fixes
- [`d599ba6`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/d599ba6a0cc7e95e14c8a44fb0afa5a65a10fd09) - **ci**: change commit tag for manifest version bump *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.10.1] - 2023-01-01
### :bug: Bug Fixes
- [`4b3a6b6`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/4b3a6b689824fc29e5018f54a76bd5cf1967b2f6) - always use api state for dimmer entity *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.10.0] - 2023-01-01
### :sparkles: New Features
- [`a866d54`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/a866d549f52e724f4d982016879a5551545d9115) - **nexa**: improved connection check *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`3a67d1f`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/3a67d1f12572d0cb959415b99ed3fec96b44e9c4) - use name from bridge as added integration name *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.9.0] - 2022-12-31
### :sparkles: New Features
- [`fa0629c`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/fa0629cf3a14b3720f647a73f221cdad9ed7ab04) - zeroconf auto discovery *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :bug: Bug Fixes
- [`844ccad`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/844ccad7f3517c908bb02db1b6172c1cb243f7e4) - **config_flow**: missing return after discovery *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :memo: Documentation Changes
- [`0ae1e1d`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/0ae1e1d244713c6d711b43a25b5e801a57f03741) - **changelog**: add v0.8.1 release info *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`4024149`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/4024149744de113fcfe2029232c29ffdfe004eb9) - **readme**: update with auto discovery information *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`4663b65`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/4663b658329da364803f47fac6267424f731ba32) - **manifest**: bump version *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.8.1] - 2022-12-31
### :recycle: Refactors
- [`e7b0d56`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/e7b0d56acc7fcd87bf7b1316bc54473105b7edd9) - more idiomatic python syntax *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :memo: Documentation Changes
- [`74d755b`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/74d755b2a1f4e4421fa29e89813a870974a20f68) - **changelog**: add v0.8.0 release info *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`0465cf0`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/0465cf09e7926401f1e5c41c61653053db44abe0) - **manifest**: bump version *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.8.0] - 2022-12-31
### :sparkles: New Features
- [`7a3db97`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/7a3db9702214ef41cecc79cd103c31d76bc4f126) - media player support *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :recycle: Refactors
- [`849c6a2`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/849c6a29473e4a0e631b8d6ef031bcd731b5da88) - stick to double quotes *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :memo: Documentation Changes
- [`5cd8804`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/5cd8804a7eb8600779a0f2cd9cecb66096e0f221) - **changelog**: add v0.7.0 release info *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`04e760f`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/04e760f4c9120dfdac8462cf4869155f25ee2d06) - **readme**: update features *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`45e5d87`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/45e5d87bbf8ba8a9531bfdb2ea29109f08cfa5b4) - **readme**: update features *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`c8afbac`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/c8afbac9f25dd7cf7ae27c394ed2310587c7f682) - **manifest**: bump version *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.7.0] - 2022-12-31
### :sparkles: New Features
- [`8e9b5b7`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/8e9b5b7cbc8aae19e023a3c424ed4913f0ec0ecf) - temperature/humidity/luminance sensor support *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :memo: Documentation Changes
- [`104e1a7`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/104e1a77837bb6807b55779fa8d9a12eb3f624d7) - **changelog**: add v0.6.0 release info *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`f8d75db`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/f8d75db5dee7a4cc1723875d67008cd3bac4cb99) - **manifest**: bump version *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.6.0] - 2022-12-31
### :sparkles: New Features
- [`43b22bc`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/43b22bc96aa2958f10da1f834b1cb39ab8f43a67) - add nexa notification sensor support *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :memo: Documentation Changes
- [`4a028fd`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/4a028fdc10cc52c1df1a5998cd7e38b7941bc6d3) - **changelog**: add v0.5.0 release info *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`473b3c8`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/473b3c80307693666996819c80a5c21ae5de24a7) - **readme**: update features *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`1d407e0`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/1d407e0400ec06a71ec14e3890e71d55637a1cc9) - **manifest**: bump version *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.5.0] - 2022-12-31
### :sparkles: New Features
- [`002a691`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/002a691c12b7e6f6a2ac96795f88acdc8a296561) - distinguish binary sensors *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :memo: Documentation Changes
- [`c48d048`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/c48d048f7c46514e6d2dddb44b262b44894caa51) - **changelog**: add v0.4.0 release info *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`711b2fc`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/711b2fc948ce1ba2d7f5f06b6c05d43474e8106c) - **readme**: update naming information *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`95f31f0`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/95f31f0b48002e7fea40efa985f135c8aeffe2a4) - **manifest**: bump version *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.4.0] - 2022-12-31
### :sparkles: New Features
- [`fe493d2`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/fe493d26df5761f19272265be95a941ea0579afa) - change friendly name order *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :memo: Documentation Changes
- [`f70cd9f`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/f70cd9f4179131b9eb5d166fca0b99cb6d91cae0) - **changelog**: add v0.3.0 release info *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`70ef2cc`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/70ef2cc36dd75d82802df0d1744bdde3986775cf) - **readme**: remove screenshot *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`0d2cf43`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/0d2cf43e5c79b8801e09e3e68f27ad892893168d) - **readme**: add naming tips *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`e0045cc`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/e0045cc72e15d90d71e50309fa9e4f18d33edd64) - **manifest**: bump version *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.3.0] - 2022-12-30
### :sparkles: New Features
- [`c789c09`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/c789c09de5bab2f456dc80d6af6a347c8aa82777) - expose more device information *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :recycle: Refactors
- [`2625f8c`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/2625f8ccc4aa471d8b8af2527f370df8236cdf91) - don't show dimmers as switches *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :memo: Documentation Changes
- [`287550e`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/287550e9bf9761473da5c0e4acff18308a3761c8) - **changelog**: add v0.2.0 release info *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`a0462aa`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/a0462aac528765a972d0c3d708cf68efcd5b7338) - update source headers *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`703a4b6`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/703a4b6af83febfea0b2d4243e7c2187db7188dd) - **manifest**: bump version *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.2.0] - 2022-12-30
### :sparkles: New Features
- [`0491db3`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/0491db3ba98c23b8e0efbd6a58496bcce5e63151) - add device service entity *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :recycle: Refactors
- [`412de2f`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/412de2f3125070c2a809cd2cbb25d466b1cb32b7) - respect lsp formatting reports *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`30bf2e0`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/30bf2e08ced7d55395312e2af2cfe0cec21d2340) - use built in type for list annotation *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :memo: Documentation Changes
- [`04b644f`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/04b644ff03ecc3b82c11f9b468be46011e69dd6f) - **changelog**: add v0.1.3 release info *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`f3200dd`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/f3200ddb2e9069642c288c417cb89b678846884d) - **readme**: update installation instructions *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`c200b95`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/c200b95fb2622a5de0fb1d30206e7f6104951be2) - **manifest**: bump version *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.1.3] - 2022-12-30
### :recycle: Refactors
- [`270ff15`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/270ff1550301f37c53c22cb3c59fad66bd349171) - **nexta**: remove redundant arguments *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :memo: Documentation Changes
- [`6a608a4`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/6a608a4ef616bbd478b6d201ac67c14471863700) - **changelog**: add v0.1.2 release info *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`596b32a`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/596b32a08c404f557d21b447defea3c486562ed3) - **changelog**: fill the blanks for releases *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`5e92b67`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/5e92b67397e77353853190597169ab442cd0a091) - **readme**: release install instructions *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`982a58d`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/982a58d3c183ec2e6496b0c39a208978c5c00f63) - **manifest**: bump version *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`ae06fa5`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/ae06fa598d081c15017ee5e4b771a38ad2e16991) - add some missing typing *(commit by [@andersevenrud](https://github.com/andersevenrud))*


## [v0.1.2] - 2022-12-30
### :recycle: Refactors
- [`63b8f70`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/63b8f70bb091e8b597b63aad05cf02abc6fefb39) - move nexa platform class *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`1aed3fa`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/1aed3fa9809215febacd80220118291dc7cbb756) - move entity constants *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`0b947e7`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/0b947e7ad61c3a1f1177c9e86017534adb2b7f6e) - move poll interval to a constant *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`ce2f277`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/ce2f2775a94a0452210617eb33f4cea2eacd08c7) - move poll timeout to constant *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`578d986`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/578d986ac32942a479f785ba4e2836cd7c7b6cb6) - add state classes to const *(commit by [@andersevenrud](https://github.com/andersevenrud))*

### :wrench: Chores
- [`df142a9`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/df142a92ce2cfff4695f87e102b1029c8a1fa91b) - remove some todo markers *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`3fd4f68`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/3fd4f6829ad04341e848763afe3c01b0da58b0e3) - add module documentation headers *(commit by [@andersevenrud](https://github.com/andersevenrud))*
- [`6b28c7f`](https://github.com/andersevenrud/ha-nexa-bridge-x/commit/6b28c7f25c918937934fc0e0b51b65860539c984) - add brand icon sources *(commit by [@andersevenrud](https://github.com/andersevenrud))*

## v0.1.0

* docs(changelog): first release docs
* docs(readme): add more help
* chore: replace 'hub' with 'bridge'
* docs(readme): more detailed description
* docs(readme): update help
* refactor: cleanup and lint pass
* docs(readme): screenshot of example entities
* docs(readme): add notes
* feat(nexa): basic api validation check
* docs(readme): improve instructions
* fix(entities): correct state class for energy sensor
* fix(entities): correct state class for sensor
* fix(entities): correct percentage value for switch level sensor
* fix(entities): simulated switch on value
* docs(readme): add installation instructions
* build: add hacs json
* chore(entities): update labels
* fix(entities): correct binary sensor state attribute
* fix(entities): improve light brightness state handling
* fix(entities): correct device class
* refactor: combine api file
* fix(config_flow): default device name
* refactor: rename component path
* fix(manifest): correct links
* feat(nexa): parallel api calls
* fix: set default energy values to none
* refactor: minor cleanup
* chore(api): update default log level
* chore: initial commit

[v0.1.2]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.1.1...v0.1.2

[v0.1.3]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.1.2...v0.1.3
[v0.2.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.1.3...v0.2.0
[v0.3.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.2.0...v0.3.0
[v0.4.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.3.0...v0.4.0
[v0.5.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.4.0...v0.5.0
[v0.6.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.5.0...v0.6.0
[v0.7.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.6.0...v0.7.0
[v0.8.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.7.0...v0.8.0
[v0.8.1]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.8.0...v0.8.1
[v0.9.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.8.1...v0.9.0
[v0.10.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.9.0...v0.10.0
[v0.10.1]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.10.0...v0.10.1
[v0.10.2]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.10.1...v0.10.2
[v0.11.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.10.2...v0.11.0
[v0.12.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.11.0...v0.12.0
[v0.13.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.12.0...v0.13.0
[v0.14.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.13.0...v0.14.0
[v0.15.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.14.0...v0.15.0
[v1.0.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v0.15.0...v1.0.0
[v1.0.1]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v1.0.0...v1.0.1
[v1.0.2]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v1.0.1...v1.0.2
[v1.0.3]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v1.0.2...v1.0.3
[v1.0.4]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v1.0.3...v1.0.4
[v1.0.5]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v1.0.4...v1.0.5
[v1.1.0]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v1.0.5...v1.1.0
[v1.1.1]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v1.1.0...v1.1.1
[v1.1.2]: https://github.com/andersevenrud/ha-nexa-bridge-x/compare/v1.1.1...v1.1.2