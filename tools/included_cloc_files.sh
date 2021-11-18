WORKING_DIR=$(mktemp -d)
function delete_tempdir {
    rm -r $WORKING_DIR
}
trap delete_tempdir EXIT


cloc --exclude-list-file=tools/cloc_exclude_dir_list.txt . --found $WORKING_DIR/available_files.txt --ignored $WORKING_DIR/ignored_files.txt > /dev/null

sort < $WORKING_DIR/available_files.txt > $WORKING_DIR/available_files_sorted.txt
cut -d : -f 1  < $WORKING_DIR/ignored_files.txt | sort > $WORKING_DIR/ignored_files_cleaned.txt

diff $WORKING_DIR/available_files_sorted.txt $WORKING_DIR/ignored_files_cleaned.txt | grep '<' | cut -d '<' -f 2
