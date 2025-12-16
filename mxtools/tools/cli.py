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
"""Collects the required tools in this module to expose to the app interface."""

import click

from mxtools.tools.hello import hello
from mxtools.tools.api import api


@click.command()
def cli_hello():
    hello()


@click.command()
@click.option("--api-key", envvar=["MXTOOLBOX_API_KEY"])
@click.option("--domain")
@click.option("--command")
def cli_api(api_key: str, domain: str, command: str):
    api(api_key=api_key, domain=domain, command=command)
