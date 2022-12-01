#!/bin/sh
CMD=vmstat
$CMD
while :
do
    $CMD >> output.txt | tail -n 1
    sleep 0.1
done
