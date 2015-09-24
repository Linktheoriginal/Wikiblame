from django.shortcuts import render
from simplemediawiki import MediaWiki
# Create your views here.

# test view
def index(request):
	item_list = ['test', 'test2']
	pagetitle = 'Index'
	context = {
		'item_list': item_list,
		'pagetitle': pagetitle,
	}
	return render(request, 'blame/index.html', context)

# initial view, form for queries.  This sends info to 'finger' view.
def point(request):
	return render(request, 'blame/point.html')

# looks through wiki for adds/removes of text, then renders a list.
def finger(request):
	change_list = []
	foundtext = False

	# PUT IN CONNECTION VALUES HERE
	wiki = MediaWiki('set_your_api_url')
	wiki.login('set_username', 'set_password')

	tokendoc = wiki.call({'action': 'tokens'})
	edittoken = tokendoc.get("tokens").get('edittoken')

	foundtext = False
	searchtext = request.GET['text'].strip()
	searchpage = request.GET['page'].strip()
	
	if searchtext == '' or searchpage == '':
		context = {
			'message': 'Missing either search text or page to search!',
		}
		return render(request, 'blame/error.html', context)
	
	queryresult = wiki.call({'action': 'query', 'prop': 'revisions', 'rvprop': 'ids|user', 'rvdir': 'newer', 'rvlimit': '5000', 'format': 'jsonfm', 'titles': searchpage})
	#print(str(queryresult))

	if ('-1' in list(queryresult['query']['pages'].keys())):
		context = {
			'message': 'The page you requested was not found!  Please check your capitalization, namespace, and spelling!',
		}
		return render(request, 'blame/error.html', context)
	
	revisions = (list(queryresult['query']['pages'][list(queryresult['query']['pages'].keys())[0]]['revisions']))
	
	for revision in revisions:
		revisiondata = wiki.call({'action': 'query', 'prop': 'revisions', 'revids': revision['revid'], 'rvprop': 'content', 'format': 'jsonfm'})
		
		revisiontext = revisiondata['query']['pages'][list(queryresult['query']['pages'].keys())[0]]['revisions'][0]['*']
		if not foundtext and searchtext in revisiontext:
			# PUT IN URL VALUE HERE
			change_list.append({'changetype': 'Added', 'revision': revision['revid'], 'user': revision['user'], 'link': 'set_your_website_url?title=' + searchpage + '&oldid=' + str(revision['revid'])})
			foundtext = True
		elif foundtext and not searchtext in revisiontext:
			# PUT IN URL VALUE HERE
			change_list.append({'changetype': 'Removed', 'revision': revision['revid'], 'user': revision['user'], 'link': 'set_your_website_url?title=' + searchpage + '&oldid=' + str(revision['revid'])})
			foundtext = False

	context = {
		'change_list': change_list,
	}
	return render(request, 'blame/finger.html', context)
	
	