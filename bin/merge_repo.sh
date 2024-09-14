#!/bin/bash

# For more info see https://www.perplexity.ai/page/git-combine-repos-into-subdire-_zZCZecQRIiIHPbfgw4aTA

#Fail on any error
set -e

cd $HOME/src/AI_Comparison

export GIT_COMMITTER_NAME="Carl From InternetOfBugs" 
export GIT_COMMITTER_EMAIL="Carl@InternetOfBugs.com"  
export GIT_AUTHOR_NAME="Carl From InternetOfBugs" 
export GIT_AUTHOR_EMAIL="Carl@InternetOfBugs.com"  

rm -rf http-server-challenge-20240906 temp-repo.$$
mkdir http-server-challenge-20240906
cd http-server-challenge-20240906
git init
git config user.email "Carl@InternetOfBugs.com"
git config user.name "Carl From InternetOfBugs" 
cd ..


for repo in *-codecrafters-httpd-py-N?; do
	git clone "file://${PWD}/${repo}/.git" temp-repo.$$
	cd temp-repo.$$
	git filter-repo --to-subdirectory-filter "${repo}"
	cd ../http-server-challenge-20240906
	git remote add -f "${repo}" ../temp-repo.$$
	git merge --allow-unrelated-histories --no-edit "${repo}"/master
	git remote remove "${repo}"
	cd ..
	rm -rf temp-repo.$$
done

cd http-server-challenge-20240906
../bin/git-rebase-order-commits-by-author-date.sh --root --committer-date-is-author-date 
git rebase --committer-date-is-author-date -r --root --exec "env GIT_COMMITTER_DATE=\"$(git log -n 1 --format=%aD)\" git commit --amend --no-edit --reset-author --allow-empty --date=\"$(git log -n 1 --format=%aD)\""
mkdir bin
cp ../bin/* bin
git add bin
git commit -m "add repo merging scripts"
cd ..
