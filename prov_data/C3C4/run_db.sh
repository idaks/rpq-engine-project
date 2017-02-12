export dbName='C3C4_facts.db'

## set variables
source ../settings.sh

## create output directories
mkdir -p $FACTS_DIR
mkdir -p $VIEWS_DIR
mkdir -p $RESULTS_DIR
mkdir -p $CSVS_DIR

## export YW model facts as CSV files
$YW_CMD model $SCRIPT_DIR/C3_C4_map_present_NA_with_comments.m \
        -c extract.language=matlab \
	    -c extract.factsfile=$CSVS_DIR/yw_extract_facts \
	    -c model.factsfile=$CSVS_DIR/yw_model_facts \
        -c query.engine=csv

## import yw extract- and model- facts to sqlite db
for f in $CSVS_DIR/*.csv
do

 ## Get the file name by removeing everything until the last / (the path) from the file name
 str1="${f##*/}"
 ## Removes the string .csv from the end of it
 NAME=${str1%.csv}

 MESSAGE=".mode csv\n.import $f $NAME"
 echo -e $MESSAGE | sqlite3 $dbName
 # do something on $f
done

## create two views from C3C4_facts.db "yw_step_in" and "yw_step_out" 
yw_step_input__view_sql_parts=(
    "create view yw_step_input as "
    "select yw_model_facts_program.program_name, yw_model_facts_data.data_name "
    "from yw_model_facts_has_in_port, yw_model_facts_program, yw_model_facts_data,  yw_model_facts_port "
    "where yw_model_facts_has_in_port.block_id = yw_model_facts_program.program_id and "
    "yw_model_facts_port.port_id = yw_model_facts_has_in_port.port_id and  "
	" yw_model_facts_port.data_id = yw_model_facts_data.data_id ;"
	)

create_yw_step_input_view_statement=$(echo "${yw_step_input__view_sql_parts[*]}")

yw_step_output__view_sql_parts=(
    "create view yw_step_output as "
    "select yw_model_facts_program.program_name, yw_model_facts_data.data_name "
    "from yw_model_facts_has_out_port, yw_model_facts_program, yw_model_facts_data, yw_model_facts_port "
    "where  yw_model_facts_has_out_port.block_id = yw_model_facts_program.program_id and "
    "yw_model_facts_port.port_id = yw_model_facts_has_out_port.port_id and  "
	"yw_model_facts_port.data_id = yw_model_facts_data.data_id; "
	)
create_yw_step_output_view_statement=$(echo "${yw_step_output__view_sql_parts[*]}")
		
sqlite3 $dbName "$create_yw_step_input_view_statement"

sqlite3 $dbName "$create_yw_step_output_view_statement"


## create a rpq table (startNode, endNode, label)
create_rpq_statement='create table rpq_table(startNode text, endNode text, label text);'

sqlite3 $dbName "$create_rpq_statement"

## create labels table and add values "in" and "out"
create_labels_statement='create table labels(label text); ';
sqlite3 $dbName "$create_labels_statement"
sqlite3 $dbName "insert into labels(label) values('in');"
sqlite3 $dbName "insert into labels(label) values('out');"

## populate the rpq table with the yw_step_input table
populate_in_edge_sql_parts=(
     "insert into rpq_table(startNode, endNode, label) "
	 "select program_name, data_name, (select label from labels where labels.label='in') "
     "from yw_step_input; "
     )
populate_in_edge_sql_statement=$(echo "${populate_in_edge_sql_parts[*]}")

sqlite3 $dbName "$populate_in_edge_sql_statement"

## populate the rpq table with the yw_step_output table
populate_out_edge_sql_parts=(
     "insert into rpq_table(startNode, endNode, label) "
	 "select program_name, data_name, (select label from labels where labels.label='out') "
     "from yw_step_output; "
     )
populate_out_edge_sql_statement=$(echo "${populate_out_edge_sql_parts[*]}")

sqlite3 $dbName "$populate_out_edge_sql_statement"		 
		 