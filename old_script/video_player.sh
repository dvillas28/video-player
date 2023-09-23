#!/bin/bash
pwd

kill_vlc () {
    # Check if VLC is running and kill it
    if pgrep -x "vlc" > /dev/null; then
        pkill -x "vlc"
        # Adding a small sleep to ensure VLC fully closes before trying to open a new instance.
        sleep 1
    fi
}

declare -A videos

# load video mappings from file
while IFS="=" read -r key path; do
    videos["$key"]="$path"
# done < <(grep '=' Desktop/scripts/video_mappings.txt)
done < <(grep '=' video_mappings2.txt)
# done < <(grep '=' $1.txt) # file as an argument

# echo the names
for key in "${!videos[@]}"; do
    video_path="${videos[$key]}"
    video_name="$(basename "$video_path")" # extract filename
    video_name_woutext="${video_name%.*}" # remove extension
    
    echo "> Key: $key, Video: $video_name_woutext"

done

echo ""
echo "> Press a key to play a video (options: ${!videos[@]})"
echo "> Press 'q' to quit the video" 
echo "> Press 'k' to close the program"

# main loop
while true; do
    # Read a single character of input
    read -s -n 1 key

    # If 'q' is pressed, exit the loop
    if [[ $key == "k" ]]; then
        echo "> Closing..."
        
        # Check if VLC is running and kill it
        kill_vlc

        break
    fi

    if [[ $key == "q" ]]; then
        
        # Check if VLC is running and kill it
        kill_vlc
    fi

    # if [[ $key == "p" ]]; then
        
    #     feh --fullscreen /home/pi/Desktop/photo.jpeg &
    # fi

    # Check if VLC is running and kill it
    kill_vlc

    # Check if the key is in the videos associative array
    if [[ ${videos[$key]} ]]; then
        # vlc --fullscreen ${videos[$key]} --play-and-exit >/dev/null 2>&1 &
        # vlc ${videos[$key]} --play-and-exit >/dev/null 2>&1 &
        vlc ${videos[$key]} --play-and-exit

        # go back to terminal (only for GUI)
        # sleep 1
        # xdotool key alt+Tab
    fi

done

