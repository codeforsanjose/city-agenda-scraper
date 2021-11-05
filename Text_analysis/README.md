# Agenda Scraper Text Analysis

This folder is the text analysis portion of the agenda scraper.

## Structure

For each agenda PDF we do the following:

1. Extract text from PDF
2. Parse the agenda items and links to attachments into a structured format
3. Parse attachment pdfs and extract relevant information
   1. various topics
   2. zip codes
   3. keywords
   4. relevant office names
   5. generate short summary?

## Reference

Roland has shared the repo that he has demoed. A good chunk of the code on text extraction and cleanup can be used in our project. [aws-comp-nlp](https://github.com/shengxio/aws-comp-nlp.git)
