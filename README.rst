Python-BackType
===========================

A simple Python wrapper for the BackType API v1.


Using python-backtype
===========================

Here's some sample code to get you started::

	import backtype_api
	api = backtype_api.BackType(api_key='[YOUR_BACKTYPE_API_KEY]')
	comments_connect_stats = api.comments_connect_stats('http://blog.backtype.com/2009/03/backtweets-search-links-on-twitter/')
	comments_search = api.comments_search('backtype')
	url_comments = api.url_comments('http://blog.backtype.com')
	page_comments = api.page_comments('http://blog.backtype.com/2008/10/backtype-on-friendfeed/')
	user_profile = api.user_profile('backtype')
	backtype_image_url = api.fetch_image_url('33_77903','p')

