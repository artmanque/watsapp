import json,traceback
from ibm_watson import AssistantV2
from ibm_watson import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

version='2019-02-28'
apikey='fSPShoOagNLuq7iOliHlSHbwMinNgIJIVAy7uycnYbA0'
service_url='https://gateway-lon.watsonplatform.net/assistant/api'
assistant_id='446a1982-63d0-443b-926d-3acd2fc25f03'
# In your API endpoint use this to generate new bearer tokens
# iam_token_manager = IAMTokenManager(apikey=apikey)
# token = iam_token_manager.get_token()

authenticator = IAMAuthenticator(apikey)
assistant = AssistantV2(
    version=version,
    authenticator=authenticator
)
# assistant.set_detailed_response(True)
assistant.set_service_url(service_url)
# assistant.set_default_headers({'x-watson-learning-opt-out': "true"})

# Disabling SSL verification
# assistant.set_disable_ssl_verification(True)

def get_response(uid,messages):
	global sessions
	try:
		# Invoke a Watson Assistant method
		# response = assistant.methodName(parameters,headers=dict)
		# response is a DetailedResponse Object for the corresponding service-specific method
		try:
			session = sessions[uid]
		except KeyError:
			session = assistant.create_session(
				assistant_id=assistant_id
			).get_result()['session_id']
			sessions[uid] = session
			while True:
				try:
					with open("sessions.json","w+") as fopen:
						fopen.write(json.dumps(sessions))
						break
				except Exception as err:
					print(err)
					input('Error dumping sessions json. Kindly make sure sessions.json is accessible')
		# print(json.dumps(session, indent=2))
		responses = []
		for message in messages:
			resp = assistant.message(
				assistant_id,
				session,
				input={
					'text': message
				# }
				# ,context={
				# 	'metadata': {
				# 	'deployment': 'myDeployment'
				# }
			}).get_result()
			print(json.dumps(resp, indent=2))
			responses.append(resp['output']['generic'][0]['text'])
		return responses
		# resp = assistant.message(input={
		# 	'text': 'What\'s the weather like?'
		# }).get_result()
		# print(json.dumps(resp, indent=2))
		# assistant.delete_session(assistant_id, session['session_id']).get_result()
	except ApiException as e:
		# status = resp.get_status_code()
		print(traceback.format_exc())
		print("Method failed with status code " + str(e.code) + ": " + e.message)
