# Bastion menu-bar helper

This is intentionally a tiny native helper. It reads only the collector's
local `status.json`; it does not execute commands, approve actions, or claim
that the Mac is protected when the status file is absent or stale.

The read-only collector is invoked with `bastion scan`. The menu-bar helper
reads the status it writes. The launchd template runs a nightly scan at 03:00;
an installer will be added after the collector's permission and baseline flow
is accepted.

Build on Apple Silicon:

```bash
swiftc macos/BastionMenuBar.swift -o .bastion/BastionMenuBar -framework Cocoa
```

Run with an explicit status file and mascot sheet:

```bash
BASTION_STATUS_PATH="$PWD/.bastion/status.json" \
BASTION_MASCOT_SHEET="$PWD/assets/mascot/bastion-sprite-sheet.png" \
.bastion/BastionMenuBar
```

Expected status shape:

```json
{"state":"protected","message":"Last scan passed","updatedAt":"2026-09-14T02:00:00Z"}
```
