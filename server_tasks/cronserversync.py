from django_cron import CronJobBase, Schedule
import requests


class CronServerSync(CronJobBase):
	RUN_EVERY_MINS = 1
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = "server_tasks.cron_server_sync"

	def do(self):
		try:
			get_address = "http://localhost:8000/server_tasks/external_trigger_server_sync"
			server_response = requests.get(url=get_address)
			return "Server response status code: {}".format(
				server_response.status_code
			)
		except requests.exceptions.RequestException as e:
			return "Request failed: {}".format(e.args)

