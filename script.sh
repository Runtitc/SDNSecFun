#!/bin/bash

echo "Running topology"
xterm -e sudo mn --custom project.py --topo mytopo --controller=remote,ip=127.0.0.1,port=6653 &
echo " Running Controller"
xterm -e sudo java -jar -Dlogback.configurationFile=logback.xml target/floodlight.jar &
echo "  Running skrypcik.py"
xterm -e sudo python scripts/skrypcik.py &
#ping localhost &
#ls