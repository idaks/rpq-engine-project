#!/usr/bin/env bash

# set directory variables
source ../settings.sh

export dbName='C3C4_facts.db'

rm -rf $FACTS_DIR
rm -rf $VIEWS_DIR
rm -rf $RESULTS_DIR
rm -rf $CSVS_DIR
rm -rf $dbName