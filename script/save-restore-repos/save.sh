#! /bin/bash

#
# Collective Knowledge (CK)
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#
# Developer: Anton Lokhmotov, anton@dividiti.com, 2018
#

# Check the source directory.
if [ -d "${CK_REPOS}" ]; then
  source_dir=${CK_REPOS}
elif [ -d "${HOME}/CK" ]; then
  source_dir=${CK_REPOS}/CK
elif [ -d "${HOME}/ck" ]; then
  source_dir=${CK_REPOS}/ck
else
  echo "Please specify the source directory via CK_REPOS!"
  exit
fi

# Check the target directory.
if [ -d "${CK_BACKUP}" ]; then
  target_dir=${CK_BACKUP}
else
  echo "Please specify the target directory via CK_BACKUP! (If it does not exist, please create it first.)"
  exit
fi

# Proceeed if both the source and target directories exist.
echo "Saving CK repositories in '${source_dir}/' to '${target_dir}/' ..."
echo

# for all files
for file in ${source_dir}/* ; do
  if [[ -d ${file} ]]; then
    # only for dirs
    dir=${file}
    repo=$(basename ${dir})
    arch=${target_dir}/${repo}.zip
    echo "- archiving '${repo}' into '${arch}':"
    # Use '--all' to save with .git information.
    ck zip repo:${repo} --archive_name=${arch} --all
    du -hs ${dir}
    du -hs ${arch}
    echo
    # Good place to break for testing (after the first archived repo).
    #break
  fi
done

# Report the total size of archived repos.
echo "Total size:"
du -hs ${target_dir}
echo
