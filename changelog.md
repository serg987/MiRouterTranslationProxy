v.0.3.3
- add more translations
- add support for cross-platform docker building and pushing to registry
- translation utility for source filed is changed to make translation semi automated
- tested on Orange Pi R1 plus RTS (arm64)

v.0.3.2
- add more translations based on Redmi AC2100 ROM v.1.0.14 and wireless relay mode
- fix some translations
- fixed bug introduced in v.0.3.1 - malformed tracking links (antitracking replacement is separated now)

v.0.3.1
- due to high number of lines, timezones translations moved to a separate file
- add more translations based on web ui sources
- fix some translations
- add small util for analyzing source files
- not translated intentionally (due to big volume):
  - License
  - Privacy policy
  - User Experience Improvement Program
  - Help

v.0.3
- add missed translations
- change `lang="zh"` to `lang="{actual_languge}"` for better compatibility
- speed up translation:
  - do not process images and html/js files without unicodes
  - do not translate commented lines (start from `//`) or lines without unicodes. For some pages translation 
sped up to 6 times

v.0.2.1
- Optimize Docker image

v.0.2
- Add support for mobile browsers
- Fix some translations

v.0.1 
- First working version
- Supports desktop browsers
- Docker config
