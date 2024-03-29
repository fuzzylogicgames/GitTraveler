# GitTraveler
GitTraveler aims to create more useable data when working with git. This allows developers to get more done and run less commands to find the data they need.

GitTraveler runs a series of git commands against any repository and aggrigates branch, tag and commit data into a single JSON formatted array. Sample below:

```
[
	{
		'hash': '76a80296ade0b91729a6687c343d0e415677a63d',
		'message': "Merge branch 'testbranch' into hotfix/bug2",
		'date': '2019-09-06 21:26:05 -0700',
		'author': 'author',
		'author_email': 'author@gmail.com',
		'branches': ['hotfix/bug2'],
		'tags': [{
			'commit_hash': '76a80296ade0b91729a6687c343d0e415677a63d',
			'tag': 'dev-tag',
			'ref': 'refs/tags/dev-tag',
			'type': 'commit'
		}, {
			'commit_hash': '76a80296ade0b91729a6687c343d0e415677a63d',
			'tag': 'v1.0.0',
			'ref': 'refs/tags/v1.0.0',
			'type': 'commit'
		}],
		'orphan': False
	}
]
```

The result will contain all tags (annotated and lightweight) attached to a commit, all branches the commit exists on as well as author, date and message information.

All results are "queryable" with GitTraveler's filtering system, every property is a field that can be filtered, allowing you to perform complex searches and only return the data you need.

## Requirements
Python 3.X

GitTraveler uses native python, no external libraries required.

## Using GitTraveler

#### Filters
GitTraveler provides a variety of filters to tailor your git log results to your specific needs. CLI filters and stop conditions are comma separated key value pairs.

##### Available Filters
- branch (string): Name of branch, all results will only exist on this branch.
- tag (string): Name of specific tag, all results will contain this tag.
- tag_present (boolean): Are tags present on commits, results will all contain tags.
- author (string): Username of the commit author, all results will be from this author name.
- author_email (string): E-mail address of the commit author, all results will be from this author name.
- date (string): Commit date, all results will be after the specified date. The date format is _Y-m-d H:m:s z_. EX: "2019-06-02 02:15:53 -0700".
- message (string): Substring match in commit message, all results will contain the word / phrase in this filter

#### Stop Conditions
GitTraveler provides conditions that will stop a search operation, currently supported conditions are limit and commit.

#### Available Stop Conditions
- limit (int): number of results to list starting from HEAD.
- commit (string): Any part of a commit hash starting from HEAD.

### Command line interface
#### Examples
To fetch entire git log:
```
python traveler --repo "<path_to_repo>"
```

To fetch all entries containing the author <author> and the string <message string> in the commit message
```
python traveler --repo "<path_to_repo>" --filters "author=<author>,message=<message string>"
```

To fetch all entries containing the author <author> and the string <message string> in the commit message, only search 30 entries
```
python traveler --repo "<path_to_repo>" --filters "author=<author>,message=<message string>" --stopcondition "limit=30"
```
  
### Importing as Python Module
Filters and stop conditions are dictionaries in this mode.

First you will need to import this module
```
from GitTraveler.GitTraveler import GitTravelerCore
gm = GitTravelerCore
```

#### Examples
To fetch entire git log:
```
gm.Walk("<path_to_repo>")
```

To fetch all entries containing the author <author> and the string <message string> in the commit message
```
gm.Walk("<path_to_repo>", {"author":"<author name>", "message":"<message string>"})
```

To fetch all entries containing the author <author> and the string <message string> in the commit message, only search 30 entries
```
gm.Walk("<path_to_repo>", {"author":"<author name>", "message":"<message string>"}, {"limit":30})
```
