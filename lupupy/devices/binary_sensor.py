"""Lupusec binary sensor device."""

from lupupy.devices import Device
import lupupy.constants as CONST


class BinarySensor(Device):
    """A binary sensor"""

    def refresh(self):
        for sensor in self._lupusec.fetch_sensors():
            if sensor["sid"] == self.id:
                self._data = sensor
                break

    @property
    def id(self):  # pylint: disable=C0103
        """Get the name of this device."""
        return self._data.get("sid")

    @property
    def name(self):
        """Get the name of this device."""
        return self._data.get("name") or self.type + " " + self.id

    @property
    def type(self):
        """Get the generic type of this device."""
        device_info = CONST.DEVICES[self._data.get("type")]

        if device_info is not None:
            return device_info.get("type")

        return "unknown"

    @property
    def status(self):
        """Shortcut to get the generic status of a device."""
        status = self._data.get("status")

        if status == "{WEB_MSG_DC_OPEN}":
            return "Open"

        if status == "{WEB_MSG_DC_CLOSE}":
            return "Closed"

        return "unknown"

    @property
    def is_on(self):
        """Get sensor state"""
        return self.status == "Open"

    def __repr__(self):
        """Get a short description of the device."""
        return "{0} (ID: {1}) - {2} - {3}".format(
            self.name, self.id, self.type, self.status
        )
