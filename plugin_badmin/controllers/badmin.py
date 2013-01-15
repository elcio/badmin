# -*- encoding: utf-8 -*- 
'''Badmin controllers'''

import math

### Default table data ###
if not 'badmin_tables' in globals():
  badmin_tables={}
if not 'badmin_exclude_tables' in globals():
  badmin_exclude_tables=[]

for table in db.tables:
  if not (table.startswith('_') or table in badmin_tables):
    if db[table] and not table in badmin_exclude_tables:
      if isinstance(db[table],db.Table):
        badmin_tables[table]={
          'columns':db[table].fields[:],
          'filters':[],
        }

### Divide tables in categories ###
for table,data in badmin_tables.iteritems():
  if not 'category' in data:
    if '_' in table:
      data['category']=table.split('_')[0]
    else:
      data['category']='othertables'
  if not 'columns' in data:
    data['columns']=db[table].fields[:]

def mkfilter(table,column):
  '''Build filter HTML elements for the given column'''

  if table[column].type=='string' or table[column].type=='text':
    return DIV(
      LABEL('%s: ' % table[column].label,_for=column),
      DIV(INPUT(_name=column,_id=column,_class='xxlarge'),_class='input'),
    _class='clearfix')

  if table[column].type=='integer':
    return DIV(
        LABEL('%s:' % table[column].label),
        DIV(
          'de ',
          INPUT(_name='from_'+column,_class='integer'),
          ' até ',
          INPUT(_name='to_'+column,_class='integer')
        ,_class='input')
      ,_class='clearfix')

  if table[column].type=='boolean':
    return DIV(
        LABEL('%s: ' % table[column].label,_for=column),
        DIV(SELECT(
          OPTION('Indiferente',_value=''),
          OPTION('Sim',_value='True'),
          OPTION('Não',_value='False'),
        _name=column,_id=column),_class='input'),
      _class='clearfix')

  if str(table[column].type).startswith('reference'):
    s=SELECT(
      *[OPTION(b,_value=a) for a,b in table[column].requires.options()],
      _name=column,_id=column)
    return DIV(
        LABEL('%s: ' % table[column].label,_for=column),
        DIV(s,_class='input'),
      _class='clearfix')

def deleteRecords(dbtable,d):
  db(dbtable.id.belongs(d)).delete()
  return T("Deleted successfully!")

@auth.requires_membership('badmin')
def index():
  '''List table'''

  tables=badmin_tables
  if not request.args:
    return redirect(URL(f='index',args=tables.keys()[0]))

  page=1
  if 'page' in request.vars:
    page=int(request.vars.page)

  table=request.args[0]
  columns=tables[table]['columns']
  dbtable=db[table]
  actions='actions' in tables[table] and tables[table]['actions'] or []
  actions.append((str(T('delete')),deleteRecords,'danger',T('Are you shure?')))

  if 'rid' in request.vars:
    d=request.vars.rid
    if not isinstance(d,list):
      d=[d]
    for a in actions:
      if a[0]==request.vars.action:
        response.flash=a[1](dbtable,d)

  q=dbtable.id>0

  for f in tables[table]['filters']:
    if dbtable[f].type=='string':
      if f in request.vars and request.vars[f]:
        q &= dbtable[f].like('%%%s%%' % request.vars[f])
    if dbtable[f].type=='integer':
      if 'from_'+f in request.vars and request.vars['from_'+f]:
        q &= dbtable[f]>=request.vars['from_'+f]
      if 'to_'+f in request.vars and request.vars['to_'+f]:
        q &= dbtable[f]<=request.vars['to_'+f]
    if dbtable[f].type=='boolean':
      if f in request.vars and request.vars[f]=='True':
        q &= dbtable[f]==True
      elif f in request.vars and request.vars[f]=='False':
        q &= (dbtable[f]==False)|(dbtable[f]==None)
    if dbtable[f].type.startswith('reference'):
      if f in request.vars and request.vars[f]:
        q &= dbtable[f]==int(request.vars[f])

  o='id'
  if 'orderby' in request.vars:
    o=request.vars.orderby

  data=db(q).select(*([dbtable.id]+[dbtable[f] for f in columns]),orderby=o,limitby=((page-1)*50,page*50))
  pages=int(math.ceil(db(q).count()/50.0))

  if tables[table]['filters']:
    filters=FORM(
      FIELDSET(
        LEGEND(T('Filter')),
        DIV(*[
            mkfilter(dbtable,f) for f in tables[table]['filters']
          ]),
        INPUT(_type='hidden',_name='orderby',_id='orderby',_value=request.vars.orderby),
        INPUT(_type='hidden',_name='page',_id='page',_value=page),
        DIV(
          INPUT(_type='submit',_value=T('Filter'),_class='btn primary'),
          _class='actions',
        ),
      ),
    _method='GET',_id='filter',_class='form-stacked')
    filters.accepts(request.vars,None,keepvalues=True)
  else:
    filters=FORM(
      INPUT(_type='hidden',_name='orderby',_id='orderby',_value=request.vars.orderby),
      INPUT(_type='hidden',_name='page',_id='page',_value=page),
      _method='GET',_id='filter'
    )

  return locals()

@auth.requires_membership('badmin')
def edit():
  '''Add/edit register'''
  tables=badmin_tables
  table=request.args[0]

  if request.args[1:]:
    id=request.args[1]
    actions='actions' in tables[table] and tables[table]['actions'] or []
    if 'action' in request.vars:
      for a in actions:
        if a[0]==request.vars.action:
          session.flash=a[1](db[table],[request.args[1]])
          return redirect(URL(f='index',args=[table]))
  else:
    id=None
    actions=[]

  f=SQLFORM(db[table],id,submit_button=T('Save'))
  if f.accepts(request.vars,session,keepvalues=True):
    session.flash='%s saved' % table
    return redirect(URL(f='index',args=[table]))

  return locals()


