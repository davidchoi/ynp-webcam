# YNP Webcam Scraper + Time Lapse Builder

Software/scripts for scraping webcam images from the NPS Yellowstone National Park website and assembling the collected images into a time-lapse video.

## Objective

Collect webcam pictures published on NPS website via cron/curl. At end of day, compile pictures into a time-lapse video using ffmpeg. 

## Methodology

1. Run webcam collection script:
    a. current implementation is to have fixed cron start/stop times server-side. therefore, first, determine if site is illuminated (mininmum twilight threshold [civil twilight?])
    b. if site is illuminated properly, download webcam pic and store in staging area
2. Dedupe collected pictures:
    a. run fdupes to remove duplicate pictures
        ```fdupes -rdN dir/```
    b. if total number of collected pictures does not meet threshold, do not run ffmpeg
3. Run ffmpeg to generate time-lapse video

```
ffmpeg -pattern_type glob -i "*.jpg" -c:v libx264 -pix_fmt yuv420p -movflags +faststart output.mp4
```
