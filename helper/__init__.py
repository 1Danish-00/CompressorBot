#    This file is part of the Compressor distribution.
#    Copyright (c) 2021 Danish_00
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    License can be found in < https://github.com/1Danish-00/CompressorBot/blob/main/License> .


import asyncio
import glob
import inspect
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime as dt
from logging import DEBUG, INFO, basicConfig, getLogger, warning
from pathlib import Path

import requests
import telethon.utils
from decouple import config
from html_telegraph_poster import TelegraphPoster
from telethon import Button, TelegramClient, errors, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ExportChatInviteRequest as cl
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_display_name

basicConfig(format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=INFO)
LOGS = getLogger(__name__)