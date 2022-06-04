for file in **/*.out
do
    cut -f 2-3 $file > ${file/.out/.rescd}
done