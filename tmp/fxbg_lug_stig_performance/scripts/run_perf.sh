#!/bin/bash

handler() {
	sudo kill $perf $vmstat
	exit 1
}

trap handler SIGINT SIGTERM

test=$1
if [[ -z $test ]]; then
	echo -n "Enter test name: "
	read test
fi

mkdir $test
pushd $test
vmstat -t 1 > ${test}_vmstat.log &
vmstat=$!
for concurrency in 1 2 4; do
	mkdir $concurrency;
	pushd $concurrency

	sudo bash -c 'echo 3 > /proc/sys/vm/drop_caches'
	sudo perf record -o perf.cp.data -F 47 -a -g sudo -u jeremy /bin/time -f 'seconds %e  system: %S  user: %U' bash -c "seq 1 $concurrency | xargs -P 0 -i cp -a ~/linux-6.7.2 ~/dest_{} 2> /dev/null"
#	sudo perf record -o perf.cp.data -F 47 -a -g &
#	perf=$!
#	sleep 3
#	/bin/time -f 'seconds %e  system: %S  user: %U' bash -c "seq 1 $concurrency | xargs -P 0 -i cp -a ~/linux-6.7.2 ~/dest_{} 2> /dev/null"
#	sleep 2
#	sudo kill -2 $perf
	sudo perf script -i perf.cp.data > perf.cp.data.script
	sudo perf report -i perf.cp.data --no-children --sort overhead,pid -F overhead,overhead_sys,overhead_us,pid  --max-stack=0 --stdio | tee perf-report.log
	sleep 5

	seq 1 $concurrency | xargs -P 0 -i rm -rf ~/dest_{}
	sleep 5

	popd
done
popd 
kill $vmstat
