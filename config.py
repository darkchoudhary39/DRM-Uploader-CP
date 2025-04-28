#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) ACE 

import os

class Config(object):
    # Get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7717267110:AAG1nwcTDra2i5yXEHbDPE6fJYkXp_yC2mc")
    API_ID = int(os.environ.get("API_ID", "25431437"))  # Retrieve API_ID with a default of 0
    API_HASH = os.environ.get("API_HASH", "3b6235f4375b77e9ce448ebc3111aa50")
    AUTH_USERS = os.environ.get("AUTH_USERS", "6434880730").split(",")  # Handle AUTH_USERS as a comma-separated string

    # Additional configuration options can be added here
