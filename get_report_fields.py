from googleads import adwords
import easygui

report_type = 'KEYWORDS_PERFORMANCE_REPORT'

stored_cred = easygui.fileopenbox()

client = adwords.AdWordsClient.LoadFromStorage(stored_cred)

rep_def = client.GetService('ReportDefinitionService', version='v201409')

fields = rep_def.getReportFields(report_type)

print 'Report type \'%s\' contains the following fields:' % report_type
for field in fields:
	print ' - %s (%s)' % (field['fieldName'], field['fieldType'])
	if 'enumValues' in field:
		print '  := [%s]' % ', '.join(field['enumValues'])

f_name = report_type+".txt"
f = open(f_name,'w')

for field in fields:
	f.write(' - %s (%s) \n' % (field['fieldName'], field['fieldType']))
	if 'enumValues' in field:
		print '  := [%s] \n' % ', '.join(field['enumValues'])