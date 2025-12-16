# Copyright (C) 2025 Ash Hellwig <ahellwig.dev@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Main interface to mxtoolbox.com"s API."""

import json
import os
import requests

from dotenv import load_dotenv

from mxtools.util.logger import setup_logger


def api(api_key: str, domain: str, api_method: str, command: str):
    # Setup Logger.
    logger = setup_logger(log_file=None)

    # Load environment variables.
    logger.info("Loading environment variables...")
    load_dotenv()

    if os.getenv("MXTOOLBOX_API_KEY") is not None:
        logger.debug("Environment variables loaded!")

    # Construct API URL.
    url: str = (
            f"https://api.mxtoolbox.com/api/v1/{api_method}/"
            f"{command}/?argument={domain}"
    )

    headers = {"Authorization": api_key, "Accept": "application/json"}

    try:
        response = requests.get(url=url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        logger.info("Command: %s", data.get("Command"))
        logger.info("Domain: %s", data.get("CommandArgument"))

        if data.get("Failed"):
            logger.error("Status: Failed")
        else:
            logger.info("Status: Passed")

        # Display the details of passed items
        if data.get("Passed"):
            logger.info("Passed checks:")
            for item in data["Passed"]:
                logger.info("- %s: %s", item["Name"], item["Info"])

    # Display any warnings or failures
        if data.get("Warnings"):
            logger.info("Warnings:")
            for item in data["Warnings"]:
                logger.info("- %s: %s", item["Name"], item["Info"])

        if data.get("Failed"):
            logger.info("Failures:")
            for item in data["Failed"]:
                logger.info("- %s: %s", item["Name"], item["Info"])

    except requests.exceptions.RequestException as e:
        logger.error("An error occurred: %s", e)

    except json.JSONDecodeError:
        logger.error("Failed to decode JSON response.")
