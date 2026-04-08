#!/bin/bash

# On-demand SSH tunnel script
# Usage: ./tunnel.sh start|stop

VPS_USER="root"
VPS_IP="191.101.70.190"
LOCAL_PORT=8888
REMOTE_PORT=8888

case $1 in
    start)
        echo "Starting tunnel..."
        ssh -N -R $REMOTE_PORT:localhost:$LOCAL_PORT $VPS_USER@$VPS_IP &
        echo $! > tunnel.pid
        echo "Tunnel started. PID: $(cat tunnel.pid)"
        ;;
    stop)
        if [ -f tunnel.pid ]; then
            kill $(cat tunnel.pid)
            rm tunnel.pid
            echo "Tunnel stopped."
        else
            echo "No tunnel running."
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        ;;
esac
