from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from config import Config
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

#from flaskr.db import get_db

bp = Blueprint('explorer', __name__)

@bp.route('/')
def index():
    #db
    rpc = AuthServiceProxy(Config.BITCOIN_RPC_URI)
    block_count = rpc.getblockcount()
    commands = [ [ "getblockhash", height] for height in range(block_count,block_count-10,-1) ] #retrocede 10 bloques
    block_hashes = rpc.batch_(commands)
    latest_blocks = rpc.batch_([ [ "getblock", h ] for h in block_hashes ])
    #block_times = [ block["time"] for block in blocks ]
    return render_template('explorer/index.html', blocks=latest_blocks)

@bp.route('/block/<int:height>')
def block(height):
    #db = get_db()
    rpc = AuthServiceProxy(Config.BITCOIN_RPC_URI)
    block = rpc.getblock(rpc.getblockhash(height))

    if block is None:
        abort(404, "El bloque {0} no existe.".format(height))
    
    return render_template('explorer/block.html', block=block)

@bp.route('/network')
def network():
    rpc = AuthServiceProxy(Config.BITCOIN_RPC_URI)
    peer_count = rpc.getconnectioncount()
    peers = rpc.getpeerinfo()
    return render_template('explorer/block.html', count=peer_count, peers=peers)