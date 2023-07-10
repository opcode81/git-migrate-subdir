# Moving a directory in one repository to a new path in another repository 

This document explains how to move a subtree rooted at a given directory in one repository to a new path in another repository and ...

* maintain all the history,
* not require `--follow` for the history to work,
* not include any baggage, i.e. without superfluous commits that do not directly impinge upon the directory in question.

## Task

The following instructions assume that we want to move the contents of `./the/source/dir` in some source repository to `./new/dir` in some target repository. 

Note: These two paths and the source repository URL`<source-repo-url>`are the only variables that you will need to adapt in the instructions below.

## Steps to take in the source repository

From the source branch in the source repository, create a new branch that contains only the data to be moved:

    git subtree split -P the/source/dir -b temp-branch

This will cause data previously at `./the/source/dir/` in the source branch to be in `./` in the newly created branch `temp-branch`.

Since we want the data to end up in `new/dir` eventually, we rewrite the new branch’s history to move it there:

    git checkout temp-branch
    git filter-branch --prune-empty -f --tree-filter '
    git ls-tree --name-only -r $GIT_COMMIT | egrep -v "^new/dir/" | xargs -L1 dirname | xargs -I thedir mkdir -pv new/dir/thedir
    git ls-tree --name-only -r $GIT_COMMIT | egrep -v "^new/dir/" | xargs -I thepath mv -v thepath new/dir/thepath
    '

Note that there are four occurrences of `new/dir` in the above snippet. The **Python script** `moveToSubDir.py` serves to assist in the adaptation of the command and prints an adapted version for you.

## Steps to take in target repository

Add a remote for the source repository and merge the temporary branch we created.

    git remote add –f source-repo <source-repo-url>
    git merge source-repo/temp-branch --allow-unrelated-histories

Voila, you will have source-repo’s `./the/source/dir` at `./new/dir` in the target repository.

 