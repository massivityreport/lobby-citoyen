# filters.py
import flask
import json
import datetime

blueprint = flask.Blueprint('filters', __name__)

@blueprint.app_template_filter('status2label')
def status_to_label_filter(s):
    tr = {
        'success': 'success',
        'failure': 'danger',
        'running': 'info'
    }

    return tr.get(s, 'info')

@blueprint.app_template_filter('prettytime')
def pretty_time(s):
    s = int(s)

    hours = ""
    if s > 3600:
        h = s/3600
        hours = "%dh " % h
        s -= h * 3600

    minutes = ""
    if s > 60:
        m = s/60
        minutes = "%dm " % m
        s -= m * 60

    seconds = "%ds" % s

    return "%s%s%s" % (hours, minutes, seconds)

@blueprint.app_template_filter('prettycount')
def pretty_count(s):
    s = int(s)

    if s >= 1000000:
        return "%sM" % (s/1000000)

    if s >= 1000:
        return "%sk" % (s/1000)

    return "%s" % s

@blueprint.app_template_filter('prettyjson')
def pretty_json(s):
    return json.dumps(s, indent=4)

@blueprint.app_template_filter('isotime2date')
def time_to_date(s):
    date = datetime.datetime.strptime(s, '%Y%m%d%H%M%S')

    return date

@blueprint.app_template_filter('sorted')
def filter_sorted(s):
    if isinstance(s, dict):
        return sorted(s.iteritems(), key=lambda x: x[0])

    if isinstance(s, list):
        return sorted(s)

    return s
