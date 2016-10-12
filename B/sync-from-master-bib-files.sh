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


srcdir=$DIRPAPERS/bibs

cp -v $srcdir/*.bib .

