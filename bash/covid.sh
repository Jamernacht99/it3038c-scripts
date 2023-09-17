#!/bin/bash
# This script downloads covid data and displays it

DATA=$(curl https://api.covidtracking.com/v1/us/current.json)
POSITIVE=$(echo $DATA | jq '.[0].positive')
TODAY=$(date)
HOSPITALIZED_C=$(echo $DATA | jq '.[0].hospitalizedCurrently')
ICU_C=$(echo $DATA | jq '.[0].inIcuCurrently')
VENTILATED_C=$(echo $DATA | jq '.[0].onVentilatorCurrently')

echo "On $TODAY, there were $POSITIVE positive COVID cases, with $HOSPITALIZED_C currently hosptalized, $ICU_C currently in ICU, and $VENTILATED_C currently on ventilators."
