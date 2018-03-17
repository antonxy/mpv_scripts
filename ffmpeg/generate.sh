#!/bin/bash
for i in {1..10}; do
    ffmpeg -i alans_dream.mp4 -vcodec copy -filter_complex "channelsplit[FL][FR];[FR]anullsink;[FL]volume=volume='if(lt(t, 102), ${i}/10, 1)':eval=frame[FL];[FL]asplit[SP][SN];[SN]pan=mono|c0=-1*c0[SN];[SP][SN]amerge" -y alans_dream_${i}.mkv;
done
