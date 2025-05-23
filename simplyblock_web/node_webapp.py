#!/usr/bin/env python
# encoding: utf-8
from simplyblock_core import utils as core_utils
logger = core_utils.get_logger(__name__)

import argparse

from flask import Flask

from simplyblock_web import utils
from simplyblock_core import constants


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/', methods=['GET'])
def status():
    return utils.get_response("Live")


MODES = [
    "caching_docker_node",
    "caching_kubernetes_node",
    "storage_node",
    "storage_node_k8s",
]

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=MODES)


if __name__ == '__main__':
    args = parser.parse_args()

    mode = args.mode
    if mode == "caching_docker_node":
        from simplyblock_web.blueprints import node_api_basic, node_api_caching_docker
        app.register_blueprint(node_api_basic.bp)
        app.register_blueprint(node_api_caching_docker.bp)

    if mode == "caching_kubernetes_node":
        from simplyblock_web.blueprints import node_api_basic, node_api_caching_ks
        app.register_blueprint(node_api_basic.bp)
        app.register_blueprint(node_api_caching_ks.bp)

    if mode == "storage_node":
        from simplyblock_web.blueprints import snode_ops
        app.register_blueprint(snode_ops.bp)

    if mode == "storage_node_k8s":
        from simplyblock_web.blueprints import snode_ops_k8s
        app.register_blueprint(snode_ops_k8s.bp)

    app.run(host='0.0.0.0', debug=constants.LOG_WEB_DEBUG)
