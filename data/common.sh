#!/bin/bash
# Some common shell stuff.

echo "Importing from common.sh"

DB=journals_db
USER=mirnaashour
CONNECT_STR="mongodb+srv://cluster0.o5mxzdg.mongodb.net/"
if [ -z $DATA_DIR ]
then
    DATA_DIR=/home/runner/work/ease-journal/ease-journal/data
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=/usr/bin/mongoexport
IMP=/usr/bin/mongoimport

if [ -z $MONGODB_PASSWORD ]
then
    echo "You must set MONGODB_PASSWORD in your env before running this script."
    exit 1
fi


declare -a JournalCollections=("categories" "journals" "users")