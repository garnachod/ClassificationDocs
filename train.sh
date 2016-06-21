#!/bin/bash
source /home/dani/classificationvenv/bin/activate
luigi --module LuigiTasks.TrainL train --local-scheduler