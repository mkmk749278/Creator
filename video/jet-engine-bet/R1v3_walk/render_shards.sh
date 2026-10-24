#!/bin/bash
# render R1v3_walk as 4 sequential shards (copied to work/r1shards/run.sh when used) (a VM restart loses one shard, not the shot); skips finished shards
cd /home/user/Creator/video/jet-engine-bet; W=work/r1shards
for k in 0 1 2 3; do
  OFF=$(python3 -c "print([0,5.2,10.4,15.6][$k])"); DUR=5.2; OUTF=$PWD/$W/s$k.mp4
  if [ -f $OUTF ] && [ -f $W/s$k.ok ]; then continue; fi
  D=$W/p$k; rm -rf $D; cp -r R1v3_walk $D; rm -rf $D/snapshots
  sed -i "s#data-duration=\"20.8\"#data-duration=\"$DUR\"#; s#tl.to({}, { duration: 20.8 })#tl.to({}, { duration: $DUR })#; s#st.run((t) => {#st.run((t0) => { const t = t0 + $OFF;#" $D/index.html
  (cd $D && HYPERFRAMES_RENDER_DETACHED=1 npx hyperframes render --workers 4 --output $OUTF > ../s$k.log 2>&1) && touch $W/s$k.ok
  rm -rf $D
done
printf "file '%s'\n" s0.mp4 s1.mp4 s2.mp4 s3.mp4 > $W/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $W/list.txt -c copy work/R1v3_walk.mp4 && echo R1DONE >> $W/status
