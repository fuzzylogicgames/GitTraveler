# GitMagic
Simplify the complicated stuff

## Requirements
Python 3.X

GitMagic uses native python, no external libraries required.

## Using GitMagic

#### Filters
GitMagic provides a variety of filters to taylor your git log results to fit the specific need. CLI filters are comma separated key value pairs.

##### Available Filters
- branch (string): Name of branch, all results will only exist on this branch.
- tag (string): Name of specific tag, all results will contain this tag.
- tag_present (boolean): Are tags present on commits, results will all contain tags.
- author (string): Username of the commit author, all results will be from this author name.
- author_email (string): E-mail address of the commit author, all results will be from this author name.
- date (string): Commit date, all results will be after the specified date. The date format is _Y-m-d H:m:s z_. EX: "2019-06-02 02:15:53 -0700".
- message (string): Substring match in commit message, all results will contain the word / phrase in this filter

#### Stop Conditions
GitMagic provides conditions that will stop a search operation, currently supported conditions are limit and commit.

#### Available Stop Conditions
- limit (int): number of results to list starting from HEAD.
- commit (string): Any part of a commit hash starting from HEAD.

### Command line interface
#### Examples
To fetch entire git log:
python gitmagic --repo "<path_to_repo>"

To fetch all entries containing the author <author> and the string <message string> in the commit message
python gitmagic --repo "<path_to_repo>" --filters "author=<author>,message=<message string>"

To fetch all entries containing the author <author> and the string <message string> in the commit message, only search 30 entries
python gitmagic --repo "<path_to_repo>" --filters "author=<author>,message=<message string>" --stopcondition "limit=30"
  
### Imported Python Module
First you will need to import this module
from GitMagic.gitmagic import GitMagicCore

#### Examples
To fetch entire git log:
~~~python gitmagic --repo "<path_to_repo>"

To fetch all entries containing the author <author> and the string <message string> in the commit message
python gitmagic --repo "<path_to_repo>" --filters "author=<author>,message=<message string>"

To fetch all entries containing the author <author> and the string <message string> in the commit message, only search 30 entries
python gitmagic --repo "<path_to_repo>" --filters "author=<author>,message=<message string>" --stopcondition "limit=30"
