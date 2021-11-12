#   Copyright 2020 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
"""network provides the network operations for a Podman service"""
import json

from podman import errors


def create(api, name, network):
    """create a network"""
    if not isinstance(network, str):
        data = json.dumps(network)
    else:
        data = network
    path = f'/networks/create?name={api.quote(name)}'
    response = api.post(path, params=data, headers={'content-type': 'application/json'})
    return json.loads(str(response.read(), 'utf-8'))


def inspect(api, name):
    """inspect a network"""
    try:
        response = api.get(f'/networks/{api.quote(name)}/json')
    except errors.NotFoundError as e:
        api.raise_not_found(e, e.response, errors.NetworkNotFound)
    return json.loads(str(response.read(), 'utf-8'))


def list_networks(api, filters=None):
    """list networks using filters"""
    filters_param = {}
    if filters:
        filters_param = {'filter': filters}
    response = api.get('/networks/json', filters_param)
    return json.loads(str(response.read(), 'utf-8'))


def remove(api, name, force=None):
    """remove a named network"""
    params = {}
    path = f'/networks/{api.quote(name)}'
    if force is not None:
        params = {'force': force}
    try:
        response = api.delete(path, params)
    except errors.NotFoundError as e:
        api.raise_not_found(e, e.response, errors.NetworkNotFound)
    return json.loads(str(response.read(), 'utf-8'))


def prune(api):
    """prune unused networks"""
    path = '/networks/prune'
    response = api.post(path, headers={'content-type': 'application/json'})
    return json.loads(str(response.read(), 'utf-8'))


__all__ = [
    "create",
    "inspect",
    "list_networks",
    "remove",
    "prune",
]
