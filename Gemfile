ruby source 'https://rubygems.org'
ruby "2.3.1"
require 'json'
require 'open-uri'
gem 'jekyll'
gem 'jekyll-watch'
gem 'rb-inotify'
versions = JSON.parse(open('https://pages.github.com/versions.json').read)
gem 'github-pages', versions['github-pages']
