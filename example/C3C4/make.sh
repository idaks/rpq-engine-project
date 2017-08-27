#!/usr/bin/env bash

# set variables
source ../settings.sh

PATH_TO_DB="./"
DB_NAME="C3C4_facts.db"

# create the database based on csv
bash run_db.sh

# list script inputs upstream of output data C3_fraction_data
QUERY="[C3_fraction_data](genby.used)+"
python ../../query_compiler.py "$PATH_TO_DB/$DB_NAME" rpq_table -c $QUERY 2>/dev/null | tr -s [:blank:] | cut -d ' ' -f 3 | tail -n +2 > $RESULTS_DIR/inputs_upstream_of_C3_fraction_data.txt

# list script inputs upstream of output data C4_fraction_data
QUERY="[C4_fraction_data](genby.used)+"
python ../../query_compiler.py "$PATH_TO_DB/$DB_NAME" rpq_table -c $QUERY 2>/dev/null | tr -s [:blank:] | cut -d ' ' -f 3 | tail -n +2 > $RESULTS_DIR/inputs_upstream_of_C4_fraction_data.txt

# list script inputs upstream of output data Grass_fraction_data
QUERY="[Grass_fraction_data](genby.used)+"
python ../../query_compiler.py "$PATH_TO_DB/$DB_NAME" rpq_table -c $QUERY 2>/dev/null | tr -s [:blank:] | cut -d ' ' -f 3 | tail -n +2 > $RESULTS_DIR/inputs_upstream_of_Grass_fraction_data.txt

##############
#   Q4_pro   #
##############


# list script outputs downstream of input data mean_airtemp
QUERY="[mean_airtemp](genby.used)+"
python ../../query_compiler.py "$PATH_TO_DB/$DB_NAME" rpq_table -c $QUERY 2>/dev/null | tr -s [:blank:] | cut -d ' ' -f 3 | tail -n +2 > $RESULTS_DIR/outputs_downstream_of_mean_airtemp.txt

# list script outputs downstream of input data mean_precip
QUERY="[mean_precip](genby.used)+"
python ../../query_compiler.py "$PATH_TO_DB/$DB_NAME" rpq_table -c $QUERY 2>/dev/null | tr -s [:blank:] | cut -d ' ' -f 3 | tail -n +2 > $RESULTS_DIR/outputs_downstream_of_mean_precip.txt

# list script outputs downstream of input data SYNMAP_land_cover_map_data
QUERY="[SYNMAP_land_cover_map_data](genby.used)+"
python ../../query_compiler.py "$PATH_TO_DB/$DB_NAME" rpq_table -c $QUERY 2>/dev/null | tr -s [:blank:] | cut -d ' ' -f 3 | tail -n +2 > $RESULTS_DIR/outputs_downstream_of_SYNMAP_land_cover_map_data.txt

