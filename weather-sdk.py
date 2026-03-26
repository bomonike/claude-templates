#!/usr/bin/env python3

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "anthropic",
#   "certifi",
#   "timezonefinder",
#   "geopy",
# ]
# ///
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file

"""weather-sdk.py to issue a simple message to ensure that it can be done.

from https://platform.claude.com/docs/en/home
Adapted for uv from https://platform.claude.com/docs/en/get-started
Described at https://bomonike.github.io/anthropic-certs
and https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

BEFORE RUNNING, on Terminal:
   # cd to a folder to receive
   git clone https://github.com/bomonike/claude-templates.git --depth 1
   cd claude-proj1
   python -m venv .venv   # creates bin, include, lib, pyvenv.cfg
   uv venv .venv  --clear
   source .venv/bin/activate
   uv add anthropic --frozen

   ruff check weather-sdk.py
   chmod +x weather-sdk.py
   uv run weather-sdk.py    # Terminal locks.
   # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate  # uv
    rm -rf .venv .pytest_cache __pycache__
"""

__last_change__ = "26-03-25 v001 new with time zone calc :weather-sdk.py"
__status__ = "WORKS on macOS Sequoia 15.6.1"

# TODO: https://platform.claude.com/docs/en/build-with-claude/working-with-messages

from datetime import datetime
import zoneinfo
import json
import os
import ssl
import sys

import certifi

from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import anthropic   # Anthropic Client SDK

client = anthropic.Anthropic()  # https://api.anthropic.com/v1/messages

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                }
            },
            "required": ["location"]
        }
    }
]

# TODO: Get & validate city name from program call parameter
my_city_name="San Francisco, CA"

# TODO: Get & validate my_model from program call parameter:
# my_model="claude-opus-4-6"    # most expensive
# my_model="claude-sonnet-4-6"
my_model="claude-haiku-4-5-20251001"   # least expensive


def get_city_time(city: str):
    # Geocode the city to lat/lon
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    geolocator = Nominatim(user_agent="city_time_app", ssl_context=ssl_context)
    location = geolocator.geocode(city)
    if not location:
        print(f"City '{city}' not found.")
        return

    # Find timezone from coordinates
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)
    if not timezone_str:
        print(f"Could not determine timezone for '{city}'.")
        return

    # Get local time
    tz = zoneinfo.ZoneInfo(timezone_str)
    local_time = datetime.now(tz)

    print(f"City     : {location.address}")
    print(f"Timezone : {timezone_str}")
    print(f"Time     : {local_time.strftime('%A, %B %d, %Y %I:%M:%S %p %Z')}")


def get_local_time(timezone: str = "America/Los_Angeles"):
    tz = zoneinfo.ZoneInfo(timezone)
    local_time = datetime.now(tz)
    print(f"Local time in time zone {local_time.strftime('%A, %B %d, %Y %I:%M:%S %p %Z')}")


def check_api_key():
    """Ensure that required API key has been set in OS environment."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set in environment variables.")
        # POLICY: DO NOT echo secret API_KEY to Terminal.
        sys.exit(1)
    else:
        return True


def get_weather(location: str) -> dict:
    """Get weather info."""
    print("From mock weather tool. TODO: Replace with a real API call (e.g. OpenWeatherMap)!")
    return {
        "location": location,
        "temperature": 68,
        "unit": "fahrenheit",
        "condition": "Partly cloudy",
        "humidity": 72,
        "wind_speed": 12
        # wind_direction
        # rainfall
        # uv
        # barometer
        # sunrise, sunset
        # time zone
        # See https://bomonike.github.io/weather-info about using Ambient Weather weather station.
    }

def run_weather_agent(location: str):
    messages = [
        {"role": "user", "content": f"What's the weather in {location}?"}
    ]

    # Using model {my_model}
    local_time=get_local_time()
    print(f"  local time: {local_time} ")

    # Turn 1: Claude decides to use the tool:
    response = client.messages.create(
        model=my_model,
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    # Agentic loop:
    while response.stop_reason == "tool_use":
        tool_uses = [b for b in response.content if b.type == "tool_use"]

        # Build tool results
        tool_results = []
        for tool_use in tool_uses:
            # import sys
            print(f"Calling {tool_use.name}(\"{tool_use.input}\") in {sys.modules['__main__'].__file__} " )
            #print(f"Calling tool: {sys.argv[0]}")

            if tool_use.name == "get_weather":
                result = get_weather(**tool_use.input)
            else:
                result = {"error": f"Unknown tool: {tool_use.name}"}

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": json.dumps(result)
            })

        # Turn 2: send tool results back to Claude:
        messages = [
            *messages,
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": tool_results}
        ]

        response = client.messages.create(
            model=my_model,
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

    # Final text response
    for block in response.content:
        if block.type == "text":
            print("\nClaude:", block.text)

    return response


def format_message(msg):
    """Format message."""
    lines = []
    lines.append(f"Message ID : {msg.id}")
    lines.append(f"Model      : {msg.model}")
    lines.append(f"Role       : {msg.role}")
    lines.append(f"Stop Reason: {msg.stop_reason}")
    lines.append(f"Type       : {msg.type}")

    lines.append("\nContent:")
    for block in msg.content:
        if block.type == "text":
            lines.append(f"  [Text] {block.text}")
        elif block.type == "tool_use":
            lines.append("  [Tool Use]")
            lines.append(f"    Name  : {block.name}")
            lines.append(f"    ID    : {block.id}")
            lines.append(f"    Input : {block.input}")

    u = msg.usage
    lines.append("\nUsage:")
    lines.append(f"  Input Tokens       : {u.input_tokens}")
    lines.append(f"  Output Tokens      : {u.output_tokens}")
    lines.append(f"  Cache Read Tokens  : {u.cache_read_input_tokens}")
    lines.append(f"  Cache Created      : {u.cache_creation_input_tokens}")
    lines.append(f"  Service Tier       : {u.service_tier}")
    lines.append(f"  Inference Geo      : {u.inference_geo}")

    return "\n".join(lines)

if my_city_name:
    get_city_time(my_city_name)
if check_api_key():
   run_weather_agent(my_city_name)
   
"""
Installed 16 packages in 21ms
Stop reason: tool_use
Calling get_weather("{'location': 'San Francisco, CA'}") in /Users/johndoe/bomonike/claude-proj1/weather-sdk.py 
Claude: Here's the current weather in **San Francisco, CA**:

- 🌤️ **Condition:** Partly cloudy
- 🌡️ **Temperature:** 68°F
- 💧 **Humidity:** 72%
- 💨 **Wind Speed:** 12 mph

It's a nice day with mild temperatures and some clouds. Let me know if you'd like to know anything else!
"""