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
if [ -d "${CK_BACKUP}" ]; then
  source_dir=${CK_BACKUP}
else
  echo "Please specify the source directory via CK_BACKUP!"
  exit
fi

# Check the target directory.
if [ -d "${CK_REPOS}" ]; then
  target_dir=${CK_REPOS}
elif [ -d "${HOME}/CK" ]; then
  target_dir=${CK_REPOS}/CK
elif [ -d "${HOME}/ck" ]; then
  target_dir=${CK_REPOS}/ck
else
  echo "Please specify the target directory via CK_REPOS! (If it does not exist, please create it first.)"
  exit
fi

# Proceeed if both the source and target directories exist.
echo "Restoring CK repositories from '${source_dir}/' to '${target_dir}/' ..."
echo

# Iterate over all files in source dir.
for file in ${source_dir}/* ; do
  # Only process *.zip files.
  if [[ ${file} =~ \.zip$ ]]; then
    echo ""
    repo=$(basename ${file} .zip)
    # Never automatically restore 'repo:local'. (FIXME: Shouldn't save it in the first place?)
    if [[ ${repo} = "local" ]]; then
      echo "- skipping '${file}' ('repo:${repo}')"
      continue
    fi
    # Try to restore this repository.
    repo_dir=${CK_REPOS}/${repo}
    echo "- restoring '${file}' into '${repo_dir}':"
    # If the repository's directory already exists, check if the repository can be safely removed and restored from zip.
    if [[ -d ${repo_dir} ]]; then
      # FIXME: Do not change into the repository's directory.
      cd ${repo_dir}
      origin_hash=$(git rev-parse --short origin/HEAD)
      current_hash=$(git describe --match=NeVeRmAtCh --always --abbrev --dirty)
      cd ${CK_REPOS}
      if [[ ${origin_hash} != ${current_hash} ]]; then
        # This repository's directory is "dirty" and thus cannot be safely removed and restored from zip.
        echo "  - origin commit '${origin_hash}', current commit '${current_hash}' - skipping"
	continue
      else
	echo "  - removing 'repo:${repo}'"
	ck rm repo:${repo} --all --force
      fi
    fi
    # Restore the repository from zip.
    echo "  - adding 'repo:${repo}'"
    ck add repo --zip=${file} --quiet
    # Good place to break for testing (after the first restored repo).
#    break
  fi
done

# Report the return status of the last command.
echo
if [ "${?}" != "0" ] ; then
  echo "FAILURE!"
  exit 1
else
  echo "SUCCESS!"
  exit 0
fi
