# Save/restore CK repositories

The `bash` scripts in this directory can be used to migrate all CK repositories from one machine to another one. While standard repositories (e.g. `ck-env`) can simply be pulled from GitHub, users often accumulate some local repositories (e.g. with experimental data). Moreover, even standard repositories can contain valuable local modifications which users might want to preserve.

## Save

To backup local CK repositories, please specify their location via the `CK_REPOS` environment variable (if it is not defined already). If `CK_REPOS` is not defined, the script tries `$HOME/CK` and $HOME/ck` (in this order).

Also, please specify the target directory via the `CK_BACKUP` environment variable. This directory must exist e.g.
```bash
$ export CK_BACKUP=$HOME/ck-backup
$ mkdir $CK_BACKUP
```

Run the save script:
```
$ cd `ck find ck-env:script:save-restore-repos`
$ ./save.sh
Archiving CK repositories in '/home/anton/CK_REPOS/' to '/home/anton/ck-backup/' ...
                                           
- archiving 'ck-analytics' into '/home/anton/ck-backup/ck-analytics.zip':
...
Total size:
24M     /home/anton/ck-backup
```

## Restore

**TODO**
