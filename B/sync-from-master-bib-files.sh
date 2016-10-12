#!/bin/sh


# Nobody runs this except Haryadi

if [ $# == 0 ]; then

    echo ""
    echo "  Nobody runs this except Haryadi"
    echo "  Please type:"
    echo "  ./sync-from-master-bib-files.sh yes"
    echo ""
    
    exit
fi


srcdir=/Users/haryadi/local/1/DIR-PUBLICATIONS/Bibliographies

cp -v $srcdir/*.bib .

