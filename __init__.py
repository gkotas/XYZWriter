# Copyright (c) 2017 Jerry Kotas
# XYZWriter is released under the terms of the AGPLv3 or higher

from . import XYZWriter

from UM.i18n import i18nCatalog
catalog = i18nCatalog("xyzwriter")

def getMetaData():
    return {
        "plugin": {
            "name": catalog.i18nc("@label", "My GCode Writer"),
            "author": "Not Ultimaker",
            "version": "1.0",
            "description": catalog.i18nc("@info:whatsthis", "Writes GCode to a file."),
            "api": 3
        },

        "mesh_writer": {
            "output": [{
                "extension": "3w",
                "description": catalog.i18nc("XYZ Writer File Description", "3w File"),
                "mime_type": "application/3w"
            }]
        }
    }

def register(app):
    return { "mesh_writer": XYZWriter.XYZWriter() }
