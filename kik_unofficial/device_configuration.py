import base64
import binascii
import re
from types import MappingProxyType

"""
Here we put all the device configuration that we emulate.
"""

# possible kik versions to emulate
# note that downgrading causes authentication to be lost
kik_version_11_info = {"kik_version": "11.1.1.12218", "classes_dex_sha1_digest": "aCDhFLsmALSyhwi007tvowZkUd0="}
kik_version_13_info = {"kik_version": "13.4.0.9614", "classes_dex_sha1_digest": "ETo70PFW30/jeFMKKY+CNanX2Fg="}
kik_version_14_info = {"kik_version": "14.0.0.11130", "classes_dex_sha1_digest": "9nPRnohIOTbby7wU1+IVDqDmQiQ="}
kik_version_14_5_info = {"kik_version": "14.5.0.13136", "classes_dex_sha1_digest": "LuYEjtvBu4mG2kBBG0wA3Ki1PSE="}
kik_version_15_21_info = {"kik_version": "15.21.0.22201", "classes_dex_sha1_digest": "MbZ+Zbjaz5uFXKFDM88CwFh7DAg="}
kik_version_15_49_info = {"kik_version": "15.49.0.27501", "classes_dex_sha1_digest": "5o61frOsakJJ2iCYafCoKHtyu7w="}
kik_version_15_57_info = {"kik_version": "15.57.2.29235", "classes_dex_sha1_digest": "hA77Y2jUTVbpHRB9LosnnunQ1PY="}
kik_version_15_60_info = {"kik_version": "15.60.1.29587", "classes_dex_sha1_digest": "FXxvP2QjSj+sXp+G1MqDdxz8Z51YjtqzFOQ7wlex0VM="}
kik_version_17_0_info = {"kik_version": "17.0.0.31357", "classes_dex_sha1_digest": "Rm2No4v27p+pIF4DVwXJvXVvdds="}

def validate_kik_version_info(info):
    """Validate profile shape; passing does not establish live Kik compatibility."""
    version = info.get("kik_version") if hasattr(info, "get") else None
    digest = info.get("classes_dex_sha1_digest") if hasattr(info, "get") else None
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+\.\d+", version):
        raise ValueError("client version must have four numeric components")
    try:
        decoded = base64.b64decode(digest, validate=True)
    except (TypeError, ValueError, binascii.Error) as exc:
        raise ValueError("classes.dex SHA-1 must be valid base64") from exc
    if len(decoded) != 20:
        raise ValueError("classes.dex SHA-1 must decode to exactly 20 bytes")
    return MappingProxyType({"kik_version": version, "classes_dex_sha1_digest": digest})


# Historical compatibility profile, not proof of current service support.
kik_version_info = validate_kik_version_info(kik_version_17_0_info)
