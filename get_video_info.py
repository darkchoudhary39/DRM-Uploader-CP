#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) ACE 

import tempfile
from subprocess import getstatusoutput

def get_video_attributes(file: str):
    """Returns video duration, width, and height."""
    
    class FFprobeAttributesError(Exception):
        """Exception if ffmpeg fails to generate attributes."""
        pass

    # Command to extract video attributes using ffprobe
    cmd = (
        "ffprobe -v error -show_entries format=duration "
        "-of default=noprint_wrappers=1:nokey=1 "
        "-select_streams v:0 -show_entries stream=width,height "
        f"-of default=nw=1:nk=1 '{file}'"
    )<span class="cursor">█</span>
