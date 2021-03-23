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


import os
import re
import io
import sys
import math
import glob
import time
import json
import shutil
import asyncio
import inspect
import requests
import traceback
import subprocess
import telethon.utils
from pathlib import Path
from decouple import config
from datetime import datetime as dt

from telethon.sessions import StringSession
from telethon.utils import get_display_name
from telethon.tl.functions.users import GetFullUserRequest
from logging import basicConfig, getLogger, INFO, DEBUG, warning
from telethon.tl.functions.messages import ExportChatInviteRequest as cl
from telethon import TelegramClient, events, Button, errors, functions, types
