import os, sys, subprocess, json, argparse, re

class GitMagicCore(object):

	_appLocalDirectory = os.path.abspath(os.path.dirname(__file__))

	def __init__(self, repoPath):
		self._walkLogs(repoPath)

	def _walkLogs(self, repoPath, filters={}, stopCondition={}):
		os.chdir(repoPath)

		commits = []
		tags = self._fetchTagData()

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
				print(tags[k]['commit_hash']+"===>"+r[0])
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

		os.chdir(self._appLocalDirectory)
		return commits
		

	def LocateCommit(self):
		pass

	def DiffAcrossBranches(self):
		pass

	def _fetchTagData(self):
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
				print("harvest true commit for annotated tag")
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
	gm = GitMagicCore()
	#gm.WalkLogs("D:/Toolbox/GitMagic/testrepo", {"commit":"f290d432f92235cedcf5253de755428eef871ec0"})
	gm.WalkLogs("D:/Toolbox/GitMagic/testrepo", {})
