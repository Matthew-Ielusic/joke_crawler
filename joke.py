from collections import namedtuple
import json
from dbco import * # this imports the db connection
from datetime import datetime

field_content = "content"
field_source = "source"
field_sourceURL = "sourceURL"
field_guid = "guid"
field_title = "title"
field_entities = "entities"
field_comments = "comments"
field_upvotes = "upvotes"
field_downvotes = "downvotes"
field_upvotes = "upvotes"
field_timestamp = "timestamp"
field_pubdate = "pubdate"

class Joke:

    def __init__(self, content, source, sourceURL, guid, pubdate=None, title=None, entities=None, comments=None, upvotes=None, downvotes=None, timestamp=None):
        self.content = content
        self.source = source
        self.sourceURL = sourceURL
        self.guid = guid
        self.pubdate = pubdate
        self.title = title
        self.entitites = entities
        self.comments = comments
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.upvotes = upvotes
        self.timestamp = timestamp

    def createJson(self):
        document = {}
        document[field_content] = self.content
        document[field_source] = self.source
        document[field_sourceURL] = self.sourceURL
        document[field_pubdate] = self.pubdate
        document[field_title] = self.title
        # document[field_entities] = self.entities
        # document[field_comments] = self.comments
        # document[field_upvotes] = self.upvotes
        # document[field_downvotes] = self.downvotes
        # document[field_upvotes] = self.upvotes
        document[field_timestamp] = self.timestamp

        return document

    def isValid(self):
        '''Returns true if content, source, sourceURL are all actual values and non-empty strings'''
        return all([self.content, self.source, self.sourceURL])

    def __str__(self):
        template = "Source: {}\tURL {}\nContent: {}"
        return template.format(self.source, self.sourceURL, self.content)
