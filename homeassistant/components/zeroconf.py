"""
This module exposes Home Assistant via Zeroconf.

Zeroconf is also known as Bonjour, Avahi or Multicast DNS (mDNS).

For more details about Zeroconf, please refer to the documentation at
https://home-assistant.io/components/zeroconf/
"""
import logging
import socket

from homeassistant.const import (EVENT_HOMEASSISTANT_STOP, __version__)

REQUIREMENTS = ["zeroconf==0.17.5"]

_LOGGER = logging.getLogger(__name__)

DOMAIN = "zeroconf"

ZEROCONF_TYPE = "_home-assistant._tcp.local."

DEPENDENCIES = ["http"]


def setup(hass, config):
    """Set up Zeroconf and make Home Assistant discoverable."""
    from zeroconf import Zeroconf, ServiceInfo

    zeroconf = Zeroconf()

    zeroconf_name = "{}.{}".format(hass.config.location_name,
                                   ZEROCONF_TYPE)

    params = {"version": __version__, "base_url": hass.http.base_url,
              "needs_auth": (hass.http.api_password != "")}

    info = ServiceInfo(ZEROCONF_TYPE, zeroconf_name,
                       socket.inet_aton(hass.http.routable_address),
                       hass.http.server_address[1], 0, 0, params)

    zeroconf.register_service(info)

    def stop_zeroconf(event):
        """Stop Zeroconf."""
        zeroconf.unregister_service(info)

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, stop_zeroconf)

    return True
