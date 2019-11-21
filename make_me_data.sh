#!/bin/bash

for run in {1..2}
do
    source devel/setup.bash
    rm src/2019F_competition_student/enph353/enph353_gazebo/scripts/plates.csv
    python src/2019F_competition_student/enph353/enph353_gazebo/scripts/plate_generator.py
    bash src/2019F_competition_student/enph353/enph353_utils/scripts/run_sim.sh &
    cd src/robot_control/launch && sleep 10 && roslaunch robot_control start.launch &
    sleep 30 && killall -9 rosout roslaunch rosmaster gzserver nodelet robot_state_publisher gzclient
done


