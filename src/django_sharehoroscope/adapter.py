from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.shortcuts import resolve_url, render, render_to_response, RequestContext
from datetime import datetime, timedelta

class AccountAdapter(DefaultAccountAdapter):

	def get_login_redirect_url(self, request):
		threshold = 25 #seconds
    
		assert request.user.is_authenticated()
		if (request.user.last_login - request.user.date_joined).seconds < threshold:
			url = '/thank-you/'
		else:
			url = '/user-page/'
		return resolve_url(url)