#!/system/bin/sh

### CPU freqs standard RN2: 403000, 806000, 1183000, 1326000, 1469000, 1625000, 1781000, 1950000
### CPU freqs PRIME RN2:    403000, 806000, 1183000, 1326000, 1482000, 1664000, 1885000, 2158000
### GPU freqs standard RN2: 253500, 299000, 390000, 442000, 546000
### GPU freqs PRIME RN2:    253500, 338000, 390000, 546000, 676000

# Stop running boot-time services (enable the lines for services you want to stop)
#stop sn                # USB serial number allocation
#stop wifi2agps         # WiFi assisted GPS (for fine location)
#stop agpsd             # Mobile Network assisted GPS (for fine locastion)
#stop emsvr_user        # Engineering Mode server
#stop PPLAgent          # Privacy Protection Lock
#stop mtkbt             # MTK Bluetooth
#stop batterywarning    # Battery warning service
#stop debuggerd64       # debug logging
#stop debuggerd         # debug logging
#stop logd              # logging
#stop autokd            # autotune for WiFi

#Set to permissive (enable this line if SE permissive mode is required)
# setenforce 0

# Tweak Interactive Governor (now set in boot.img - enable here to override values)
#echo 403000 > /sys/devices/system/cpu/cpufreq/interactive/hispeed_freq        # factory default 1183000
#echo 99 > /sys/devices/system/cpu/cpufreq/interactive/go_hispeed_load         # factory default 99
#echo 99 > /sys/devices/system/cpu/cpufreq/interactive/target_loads            # factory default 90
#echo 25000 > /sys/devices/system/cpu/cpufreq/interactive/timer_rate           # factory default 20000
#echo 10000 > /sys/devices/system/cpu/cpufreq/interactive/min_sample_time      # factory default 20000
#echo 5000 > /sys/devices/system/cpu/cpufreq/interactive/above_hispeed_delay   # factory default 20000
#echo 40000 > /sys/devices/system/cpu/cpufreq/interactive/timer_slack          # factory default 80000

# Limit CPU max freqs (To limit the maximum cpu freq, enable both of these lines. Select a valid freq for your device from table at start)
#echo 1781000 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq
#echo 1781000 > /proc/cpufreq/cpufreq_limited_max_freq_by_user

# Limit foreground CPU cores (set in boot.img - enable here to override values) 0-1 min, 0-7 max Example shows 5 cores (also needs to be set in Hotplug)
#echo 0-4 > /dev/cpuset/foreground/cpus

# Hotplug settings (set in boot.img - enable here to override values) Note: num_limit values are 1-8
#echo 5 > /proc/hps/num_limit_low_battery          # factory default 8
#echo 5 > /proc/hps/num_limit_power_serv           # factory default 8
#echo 5 > /proc/hps/num_limit_thermal              # factory default 8
#echo 5 > /proc/hps/num_limit_ultra_power_saving   # factory default 8
#echo 99 > /proc/hps/up_threshold                  # factory default 95
#echo 87 > /proc/hps/down_threshold                # factory default 85
#echo 0 > /proc/hps/rush_boost_enabled             # factory default 1
#echo 0 > /proc/hps/input_boost_enabled            # factory default 1

# Tweak GPU Settings (Look in /proc/gpufreq/gpufreq_power_dump for power usage at different freqs)
    # To disable GPU touch boost:
#echo 0 > /proc/gpufreq/gpufreq_input_boost        # factory default 1 (enabled)
    # To limit max GPU freq: (Select a valid freq for your device from table at start)
#echo 442000 > /proc/gpufreq/gpufreq_opp_max_freq  # factory default 0 (disabled) 

# Tweak VM (set in boot.img - enable here to override values)
#echo 300 > /proc/sys/vm/dirty_expire_centisecs    # factory default 200
#echo 500 > /proc/sys/vm/dirty_writeback_centisecs # factory default 300

# Tweak LMK (set in boot.img - enable here to override values) 18 37 56 75 93 112MB   # factory default 72 90 108 126 219 317MB (MB x 256 = value)
#echo 4608,9472,14336,19200,23808,28672 > /sys/module/lowmemorykiller/parameters/minfree

#Enable zram (no zram set by default, enable  first 4 lines if 1 zram required, all 7 lines if 2 zram required)
#echo 40 > /proc/sys/vm/swappiness
#echo 268435456 > /sys/block/zram0/disksize     # for single zram: 536870912 = 512MB (for non-prime version) 1073741824=1GB (for prime version)
#/system/xbin/busybox mkswap /dev/block/zram0
#/system/xbin/busybox swapon /dev/block/zram0
#echo 268435456 > /sys/block/zram1/disksize     # for 2 zrams: 268435456 = 256MB (for non-prime version) 536870912 = 512MB (for prime version)
#/system/xbin/busybox mkswap /dev/block/zram1
#/system/xbin/busybox swapon /dev/block/zram1

# Tweak IO Scheduler (set in boot.img - enable here to override values)
#echo deadline > /sys/block/mmcblk0/queue/scheduler    # factory default cfq (choice: noop deadline cfq)
#echo 128 > /sys/block/mmcblk0/queue/read_ahead_kb     # factory default 128 Choose between 128, 256, 512, 1024, 2048
#echo 0 > /sys/block/mmcblk0/queue/add_random          # factory default 1
#echo 0 > /sys/block/mmcblk0/queue/iostats             # factory default 1
#echo deadline > /sys/block/mmcblk1/queue/scheduler    # for ext sdcard (sdcard1)
#echo 2048 > /sys/block/mmcblk1/queue/read_ahead_kb     # for ext sdcard (sdcard1)
#echo 0 > /sys/block/mmcblk1/queue/add_random          # for ext sdcard (sdcard1)
#echo 0 > /sys/block/mmcblk1/queue/iostats             # for ext sdcard (sdcard1)

#Tweak Entropy (set in boot.img - enable here to override values)
#echo 384 > /proc/sys/kernel/random/read_wakeup_threshold    # factory default 64
#echo 448 > /proc/sys/kernel/random/write_wakeup_threshold   # factory default 128

#Tweak for wifi router connection issues
#echo 1 > /proc/sys/net/ipv6/conf/wlan0/disable_ipv6

# Disable debugging on some modules (set in boot.img - enable here to override values)
#echo 0 > /sys/module/alarm_dev/parameters/debug_mask;
#echo 0 > /sys/module/alarmtimer/parameters/debug_mask;
#echo 0 > /sys/module/binder/parameters/debug_mask;
#echo 0 > /sys/module/earlysuspend/parameters/debug_mask;
#echo 0 > /sys/module/sbsuspend/parameters/sbsuspend_debug_mask;
#echo 0 > /sys/module/snd/parameters/debug;
#echo 0 > /sys/module/pvrsrvkm/parameters/gPVRDebugLevel;
#echo 0 > /sys/module/musb_hdrc/parameters/debug_level;
#echo 0 > /sys/module/lowmemorykiller/parameters/debug_level;

