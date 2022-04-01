from app import app, render_template, request, redirect, url_for, abort
from app.functions import *

dataPath=os.environ["BRAWL_COACH_DATAPATH"]
backPath=os.environ["BRAWL_COACH_BACKPATH"]
frontPath=os.environ["BRAWL_COACH_FRONTPATH"]
logPath=os.environ["BRAWL_COACH_LOGPATH"]
token=os.environ["BRAWL_COACH_TOKEN"]

@app.route("/")
def homepage():
	return render_template('home.html')

@app.route("/meta/<string:metaType>")
def team_picker(metaType):
	metaTypeAllowed = ["current", "championship"]
	if metaType in metaTypeAllowed:
		battleNumber={}
		bestTeams={}
		bestSolo={}
		progress={}
		remainTime={}
		hours={}
		minutes={}
		i=0
		current_events = readCurrentEvents(dataPath+"/events/current_events.json")
		current_events = current_events[metaType]

		for events in current_events:
			_, _, progress[i], remainTime[i]=computeEventTime(events)
			hours[i], minutes[i], _ = convert_timedelta(remainTime[i])
			try:
				bestTeamsRaw, battleNum =readEventsStats(events, "teams")
				bestSoloRaw, battleNum =readEventsStats(events, "solo")

				bestTeamsSorted = sorted(bestTeamsRaw, key=lambda d: d['teamStats']["pickRate"], reverse=True)
				bestSoloSorted = sorted(bestSoloRaw, key=lambda d: d['soloStats']["pickRate"], reverse=True)
				
				bestTeams[i]=bestTeamsSorted
				bestSolo[i]=bestSoloSorted

				battleNumber[i]=battleNum
			except:
				try:
					bestSoloRaw, battleNum =readEventsStats(events, "solo")
					bestSoloSorted = sorted(bestSoloRaw, key=lambda d: d['soloStats']["pickRate"], reverse=True)
					bestSolo[i]=bestSoloSorted
					battleNumber[i]=battleNum
				except:
					battleNumber[i]=0
					bestTeams[i]="N/A"
			i=i+1			
		return render_template('currentMeta.html', title="Meta", current_events=current_events, len=len(current_events), battleNumber=battleNumber, bestTeams=bestTeams, bestSolo=bestSolo, eventProgress=progress, hours=hours, minutes=minutes)
	else:
		abort(404)

@app.route("/meta/<string:events>")
def mode_map(events):
	current_events = readCurrentEvents(dataPath+"/events/current_events.json")
	current_event=current_events[int(events)]
	try:
		bestTeamsRaw, battleNum =readEventsStats(current_event, "teams")
		bestTeamsSorted = sorted(bestTeamsRaw, key=lambda d: d['teamStats']["pickRate"], reverse=True)
		if len(bestTeamsSorted)>50:
			lenTeams=50
		else:
			lenTeams=len(bestTeamsSorted)
	except:
		bestTeamsSorted="None"
		lenTeams=0
	
	bestSoloRaw, battleNum =readEventsStats(current_event, "solo")
	bestSoloSorted = sorted(bestSoloRaw, key=lambda d: d['soloStats']["pickRate"], reverse=True)
	lenSolo=len(bestSoloSorted)

	return render_template('currentMetaDetails.html', bestTeams=bestTeamsSorted, bestSolo=bestSoloSorted, lenTeams=lenTeams, lenSolo=lenSolo, mode=current_event["event"]["mode"], map=current_event["event"]["map"])


@app.route("/processTime.log")
def processTime():
	try:
		with open(logPath+path_separator+"timeLog.txt") as fp:
			timeLog = json.load(fp)
	except:
		timeLog=[]
	return {"items": timeLog}

@app.errorhandler(404)
def page_not_found(error):
   return render_template('notFound.html', title = '404'), 404


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000)
