#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) ACE 

import os

class Config(object):
    # Get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_ID = int(os.environ.get("API_ID", 0))  # Retrieve API_ID with a default of 0
    API_HASH = os.environ.get("API_HASH", "")
    AUTH_USERS = os.environ.get("AUTH_USERS", "").split(",")  # Handle AUTH_USERS as a comma-separated string

    # Additional configuration options can be added here
