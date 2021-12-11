#!/bin/bash
# display command line options

count=1
for param in "$@"; do
<<<<<<< HEAD
<<<<<<< HEAD
=======
   
>>>>>>> 79198f9 (git-rebase 1)
=======
    echo "Next parameter: $param"
>>>>>>> 925c881 (git-rebase 2)
    count=$(( $count + 1 ))
done

echo "====="