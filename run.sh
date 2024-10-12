#!/bin/bash
if [ -d "./dev" ]; then    
    python3 ./dev/tasks.py &
    MAIN_PID=$!
    sleep 4
    if [ -d "./tests" ]; then 
        pytest ./tests/test.py
    else
        echo "No Test Directory Found.";
    fi
    wait $MAIN_PID
else 
    echo "No Dev Directory Found.";
fi
