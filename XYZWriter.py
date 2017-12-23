# Copyright (c) 2017 Jerry Kotas
# XYZWriter is released under the terms of the AGPLv3 or higher.

import io
import subprocess
import os

from UM.Mesh.MeshWriter import MeshWriter
from UM.Logger import Logger
from UM.Application import Application
import UM.Platform

class XYZWriter(MeshWriter):
    def __init__(self):
        super().__init__()

    def write(self, stream, nodes, mode = MeshWriter.OutputMode.TextMode):
        """
        Write the 3w data to a stream.

        Inputs: stream - The stream to write to.
                nodes - Ignored.
                mode - Ignored.
        Output: Success or Failure
        """
        # Get the g-code.
        scene = Application.getInstance().getController().getScene()
        gcode_list = getattr(scene, "gcode_list")
        if not gcode_list:
            return False

        # Find an unused file name to temporarily write the g-code to.
        file_name = stream.name
        if not file_name: #Not a file stream.
            Logger.log("e", "XYZ writer can only write to local files.")
            return False
        # Save the tempfile next to the real output file.
        file_directory = os.path.dirname(os.path.realpath(file_name))
        i = 0
        temp_file = os.path.join(file_directory, "output" + str(i) + ".gcode")
        while os.path.isfile(temp_file):
            i += 1
            temp_file = os.path.join(file_directory, "output" + str(i) + ".gcode")

        # Write the g-code to the temporary file.
        try:
            with open(temp_file, "w", -1, "utf-8") as f:
                for gcode in gcode_list:
                    f.write(gcode)
        except:
            Logger.log("e", "Error writing temporary g-code file %s", temp_file)
            _removeTemporary(temp_file)
            return False

        # Check if threedub is callable
        try:
            subprocess.check_output(['threedub', '-h'])
        except Exception as e:
            Logger.log("e", "threedub could not be called: %s", str(e))
            _removeTemporary(temp_file)
            return False

        # Call the converter application to convert it to 3w.
        cmd = ['threedub', temp_file, file_name]
        try:
            subprocess.check_output(cmd)
        except Exception as e:
            Logger.log("e", "System call to threedub failed: %s", str(e))
            _removeTemporary(temp_file)
            return False

        # Clean Up
        _removeTemporary(temp_file)
        return True


def _removeTemporary(temp_file):
    """
    Removes the temporary g-code file that is an intermediary result.

    Inputs: temp_file - The URI of the temporary file.
    Output: None
    """
    try:
        os.remove(temp_file)
    except:
        Logger.log("w", "Couldn't remove temporary file %s", temp_file)
