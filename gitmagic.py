import os, sys, subprocess, json, argparse, re

class GitMagicCore(object):

	__appLocalDirectory = os.path.abspath(os.path.dirname(__file__))
	
	def __init__(self, cliMode=False):
		self._cliMode = cliMode

	# public use methods
	def Walk(self, repoPath, filters={}, stopCondition={}):
		return self.__walkLogs(repoPath, filters, stopCondition)

	# internals
	def __walkLogs(self, repoPath, filters={}, stopCondition={}):
		os.chdir(repoPath)

		commits = []
		tags = self.__fetchTagData()

		cmd = "git log --all --pretty=format:\"%H|||%an|||%ae|||%ai|||%s\" --decorate=full"
		result = self._runCommand(cmd).split('\n')
		for i in range(len(result)):
			# process stop conditions
			if 'limit' in stopCondition and i == stopCondition['limit']:
				break

			if 'commit' in stopCondition and stopCondition['commit'] in r[0]:
				break

			r = result[i].split("|||")
			commitData = {
				"hash":r[0],
				"message":r[4],
				"date":r[3],
				"author":r[1],
				"author_email":r[2],
				"branches":[],
				"tags":[],
				"orphan":False
			}
			
			# add tags to collection if connected to this hash and add to commit data
			for k in range(len(tags)):
				if tags[k]['commit_hash'] == r[0]:
					commitData["tags"].append(tags[k])
			
			# gather all branches this commit exists on and add to commit data
			cmd = "git branch --contains "+commitData['hash']
			branches = self._runCommand(cmd).split('\n')
			if len(branches) > 0:
				for j in range(len(branches)):
					b = branches[j].strip()
					if b == "":
						continue

					if b.startswith('*'):
						b = b[2:]

					commitData['branches'].append(b)
			else:
				# no branches attached to this commit
				commitData['orphan'] = True
				
			commits.append(commitData)

		# useful for debugging
		#print(json.dumps(commits))

		os.chdir(self.__appLocalDirectory)
		return commits
		
	def __applyFilters(self, filters={}):
		if filters == None:
			print("No filters defined")
			sys.exit(1)0

		filterTest = {
			"branch_name":""
		}

	def __fetchTagData(self):
		tagData = []

		cmd = "git show-ref --tags"
		tagresult = list(filter(None, self._runCommand(cmd).split("\n")))
		for i in range(len(tagresult)):
			if tagresult[i] == '{}':
				continue

			tagInfoType = "commit"
			tagInfo = tagresult[i].split(" ")[1]
			hashInfo = tagresult[i].split(" ")[0]

			cmd = "git cat-file -t "+tagInfo
			tagType = self._runCommand(cmd).strip()
			if tagType == "tag":
				tagInfoType = "annotated"

				# harvest true commit for annotated tag
				cmd = "git show-ref -d "+tagresult[i]
				annotatedTag = self._runCommand(cmd).strip().split('\n')
				for i in range(len(annotatedTag)):
					if '^{}' in annotatedTag[i]:
						hashInfo = annotatedTag[i].split(' ')[0]

			tagData.append({'commit_hash':hashInfo, 'tag':tagInfo, 'type':tagInfoType})

		return tagData

	def _runCommand(self, cmd):
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		output = p.communicate()[0]

		try:
			output = output.decode('utf-8')
		except Execption as err:
			print(err)

		return output

	def _exportResults(self, diffs=False, commitLogs=False):
		pass

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-r', '--repo', required=True, type=str, help='Repository path')
	parser.add_argument('-c', '--cli', action="store_true", help='Repository path')
	args = parser.parse_args()

	gm = GitMagicCore(args.cli)
	result = gm.Walk(args.repo)
	print(result)

	#gm.WalkLogs("D:/Toolbox/GitMagic/testrepo", {"commit":"f290d432f92235cedcf5253de755428eef871ec0"})
	#gm.WalkLogs("D:/Toolbox/GitMagic/testrepo", {})
