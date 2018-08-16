# mark_sum
Mark_sum is a package that creates automatic webpage summaries.

Input: It takes a URL and a filename (Markdown .md file, for export) as command line arguments.
Output: It writes a markdown file to the current directory with the following information:

1. Title of article
2. Source
3. Featured image (first image after h1)
4. Summary (Three sentences)
5. Link to the article

## Usage

Typical usage in command line:
`$ python mark_sum.py urltosummarize.com export-filename.md`

## Requirements
* Python 3.6
* Modules as listed below:

## Modules Used
1. [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
2. [sumy](https://github.com/miso-belica/sumy)
3. [Markdown Generator](https://github.com/cmccandless/markdown-generator)


## Changelog
August 16, 2018 - v0.1 published 




